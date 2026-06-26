#!/usr/bin/env node
/**
 * 微博正文回填「内容解析」（纯 Node 版本）
 *
 * - 过滤：来源渠道 == "新浪微博"
 * - 读取：原文 URL（候选字段：获取原文URL/原文 URL/原文URL/原文url/doc_url）
 * - 抓取：m.weibo.cn/statuses/show?id={weiboId}
 * - 写回：内容解析（默认只写空值）
 */

const { buildAnalysis } = require("./build-content-analysis");

function env(key, defaultValue = "") {
  const v = process.env[key] ?? process.env[`INPUT_${String(key).toUpperCase()}`];
  return String(v ?? defaultValue).trim();
}

const APP_ID = env("APP_ID");
const APP_SECRET = env("APP_SECRET");
const BITABLE_URL = env("BITABLE_URL");

const SOURCE_CHANNEL_FIELD = env("SOURCE_CHANNEL_FIELD", "来源渠道");
const CONTENT_ANALYSIS_FIELD = env("CONTENT_ANALYSIS_FIELD", "内容解析");
const LINK_STATUS_FIELD = env("LINK_STATUS_FIELD", "链接是否有效");
const HAS_IMAGE_FIELD = env("HAS_IMAGE_FIELD", "是否包含图片");
const HAS_VIDEO_FIELD = env("HAS_VIDEO_FIELD", "是否包含视频");

const ONLY_EMPTY = ["1", "true", "yes"].includes(env("ONLY_EMPTY", "1").toLowerCase());
const MAX_TARGETS = parseInt(env("LIMIT", "50"), 10);
const PAGE_SIZE = parseInt(env("PAGE_SIZE", "200"), 10);
const MAX_CHARS = parseInt(env("MAX_CHARS", "100"), 10);
const WORKERS = parseInt(env("WORKERS", "4"), 10);

const HTTP_TIMEOUT_MS = parseInt(env("HTTP_TIMEOUT_MS", "15000"), 10);
const HTTP_RETRY_TIMES = parseInt(env("HTTP_RETRY_TIMES", "1"), 10);

const UA_COMMON =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

const ORIGINAL_URL_CANDIDATES = [
  // 兼容 Clawhub 输入：original_url_field
  env("ORIGINAL_URL_FIELD") || env("WEIBO_ORIGINAL_URL_FIELD"),
  "获取原文URL",
  "原文 URL",
  "原文URL",
  "原文url",
  "doc_url",
].filter(Boolean);

const TARGET_SOURCE_CHANNEL = env("SOURCE_CHANNEL_VALUE", "新浪微博");

function parseBitableUrl(url) {
  const parsed = new URL(url);
  let appToken = "";
  const parts = parsed.pathname.split("/").filter(Boolean);
  for (let i = 0; i < parts.length; i++) {
    if (parts[i] === "base" && i + 1 < parts.length) {
      appToken = parts[i + 1];
      break;
    }
  }
  const tableId = parsed.searchParams.get("table");
  if (!appToken || !tableId) throw new Error(`BITABLE_URL 解析失败: ${url}`);
  return [appToken, tableId];
}

async function withRetry(fn) {
  let lastErr = null;
  for (let attempt = 0; attempt <= HTTP_RETRY_TIMES; attempt++) {
    try {
      return await fn();
    } catch (e) {
      lastErr = e;
      const backoff = 600 * Math.pow(2, attempt);
      await new Promise((r) => setTimeout(r, backoff));
    }
  }
  throw lastErr;
}

function stripHtmlLike(s) {
  return String(s || "")
    .replace(/<[^>]*>/g, "")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ")
    .trim();
}

function extractWeiboId(url) {
  let m = url.match(/weibo\.com\/\d+\/([a-zA-Z0-9]+)/);
  if (m) return m[1];
  m = url.match(/m\.weibo\.cn\/status\/([a-zA-Z0-9]+)/);
  if (m) return m[1];
  m = url.match(/weibo\.com\/\d+\/([a-zA-Z0-9]+)\?/);
  if (m) return m[1];
  const parts = url.split("/").filter(Boolean);
  const last = parts[parts.length - 1];
  if (last && !last.includes("?")) return last;
  return null;
}

async function httpGet(url) {
  return withRetry(async () => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), HTTP_TIMEOUT_MS);
    try {
      const resp = await fetch(url, {
        method: "GET",
        headers: {
          "User-Agent": UA_COMMON,
          Accept: "application/json,text/html,*/*",
          Referer: "https://m.weibo.cn/",
          "X-Requested-With": "XMLHttpRequest",
        },
        redirect: "follow",
        signal: ctrl.signal,
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      return await resp.json();
    } finally {
      clearTimeout(t);
    }
  });
}

async function getTenantAccessToken() {
  if (!APP_ID || !APP_SECRET) throw new Error("请设置环境变量 APP_ID / APP_SECRET");
  const url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal";
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
    redirect: "follow",
  });
  if (!resp.ok) throw new Error(`tenant_access_token HTTP ${resp.status}`);
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`获取 tenant_access_token 失败: ${JSON.stringify(data)}`);
  return data.tenant_access_token;
}

function safeText(v) {
  if (v == null) return "";
  if (Array.isArray(v)) return v.length ? String(v[0]).trim() : "";
  if (typeof v === "object") return JSON.stringify(v);
  return String(v).trim();
}

async function fetchTargets(token) {
  if (!BITABLE_URL) throw new Error("请设置环境变量 BITABLE_URL（飞书多维表链接）");
  const [appToken, tableId] = parseBitableUrl(BITABLE_URL);
  const url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records`;
  const headers = { Authorization: `Bearer ${token}` };

  const targets = [];
  let pageToken = null;
  while (targets.length < MAX_TARGETS) {
    const params = new URLSearchParams();
    params.set("page_size", String(Math.min(500, PAGE_SIZE)));
    if (pageToken) params.set("page_token", pageToken);
    const resp = await fetch(`${url}?${params.toString()}`, { method: "GET", headers, redirect: "follow" });
    if (!resp.ok) throw new Error(`获取记录失败 HTTP ${resp.status}`);
    const data = await resp.json();
    if (data.code !== 0) throw new Error(`获取记录失败: ${JSON.stringify(data)}`);
    const obj = data.data || {};
    const items = obj.items || [];
    for (const rec of items) {
      const fields = rec.fields || {};
      const ch = safeText(fields[SOURCE_CHANNEL_FIELD]);
      if (ch !== TARGET_SOURCE_CHANNEL) continue;
      const existingContent = safeText(fields[CONTENT_ANALYSIS_FIELD]);
      const existingLink = safeText(fields[LINK_STATUS_FIELD]);
      const existingImg = safeText(fields[HAS_IMAGE_FIELD]);
      const existingVid = safeText(fields[HAS_VIDEO_FIELD]);

      const needsContent = !existingContent;
      const needsLink = !existingLink;
      const needsImg = !existingImg;
      const needsVid = !existingVid;

      if (ONLY_EMPTY && !(needsContent || needsLink || needsImg || needsVid)) continue;

      let originalUrl = "";
      for (const cand of ORIGINAL_URL_CANDIDATES) {
        if (fields[cand] != null) {
          const v = safeText(fields[cand]);
          if (v) {
            originalUrl = v;
            break;
          }
        }
      }
      if (!originalUrl) continue;
      if (!rec.record_id) continue;

      targets.push({
        record_id: rec.record_id,
        original_url: originalUrl,
        need_content: needsContent,
        need_link: needsLink,
        need_img: needsImg,
        need_video: needsVid,
      });
      if (targets.length >= MAX_TARGETS) break;
    }

    if (!obj.has_more || !obj.page_token) break;
    pageToken = obj.page_token;
  }
  return targets;
}

async function batchUpdate(token, updates) {
  if (!updates.length) return;
  const [appToken, tableId] = parseBitableUrl(BITABLE_URL);
  const url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records/batch_update`;
  const resp = await fetch(url, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ records: updates }),
  });
  if (!resp.ok) throw new Error(`批量更新失败 HTTP ${resp.status}`);
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`批量更新失败: ${JSON.stringify(data)}`);
}

async function extractWeiboText(originalUrl) {
  const weiboId = extractWeiboId(originalUrl);
  if (!weiboId) throw new Error(`无法从微博 URL 提取 weiboId: ${originalUrl}`);
  const apiUrl = `https://m.weibo.cn/statuses/show?id=${weiboId}`;
  const data = await httpGet(apiUrl);
  if (data.ok !== 1) throw new Error(`Weibo API error: ${JSON.stringify(data)}`);
  const obj = data.data || {};
  const text = stripHtmlLike(obj.text || obj.longText || "");
  const picNum = obj.pic_num || 0;
  return { text, picNum };
}

function buildContentAnalysis({ text, picNum }) {
  if (!text) return "";
  const mediaType = picNum > 0 ? "图片" : "视频";
  const res = buildAnalysis({
    title: "",
    text,
    platform: "微博",
    mediaType,
    visual: "",
    maxChars: MAX_CHARS,
  });
  return res.analysis || "";
}

async function main() {
  // 本地烟测模式：不依赖飞书多维表
  const TEST_URL = (env("TEST_URL", "") || "").trim();
  const TEST_SOURCE_CHANNEL = (env("TEST_SOURCE_CHANNEL", "") || "").trim();
  if (TEST_URL && TEST_SOURCE_CHANNEL) {
    const { text, picNum } = await extractWeiboText(TEST_URL);
    const content = buildContentAnalysis({ text, picNum });
    const hasImage = picNum > 0;
    const hasVideo = picNum <= 0;
    console.log(
      JSON.stringify(
        {
          test_source_channel: TEST_SOURCE_CHANNEL,
          test_url: TEST_URL,
          text_preview: String(text || "").slice(0, 80),
          content_analysis: content,
          link_status: "是",
          has_image: hasImage ? "是" : "否",
          has_video: hasVideo ? "是" : "否",
        },
        null,
        2
      )
    );
    return;
  }

  const token = await getTenantAccessToken();
  console.log("获取飞书 token 成功");

  const targets = await fetchTargets(token);
  console.log(`筛选到需要处理的微博记录：${targets.length} 条`);
  if (!targets.length) return;

  const updates = [];
  const workers = [];
  for (let w = 0; w < WORKERS; w++) {
    workers.push(
      (async () => {
        for (let i = w; i < targets.length; i += WORKERS) {
          const t = targets[i];
          try {
            const { text, picNum } = await extractWeiboText(t.original_url);
            const valid = true;
            const hasImage = picNum > 0;
            const hasVideo = picNum <= 0;

            const fields = {};
            if (t.need_link) fields[LINK_STATUS_FIELD] = valid ? "是" : "否";
            if (t.need_img) fields[HAS_IMAGE_FIELD] = hasImage ? "是" : "否";
            if (t.need_video) fields[HAS_VIDEO_FIELD] = hasVideo ? "是" : "否";

            if (t.need_content) {
              const content = buildContentAnalysis({ text, picNum });
              if (content) fields[CONTENT_ANALYSIS_FIELD] = content;
            }

            if (Object.keys(fields).length) {
              updates.push({ record_id: t.record_id, fields });
            }
            console.log(`  worker#${w + 1} ok record_id=${t.record_id}`);
          } catch (e) {
            console.log(`  worker#${w + 1} err record_id=${t.record_id}: ${e?.message || String(e)}`);
            if (t.need_link) {
              updates.push({
                record_id: t.record_id,
                fields: { [LINK_STATUS_FIELD]: "否" },
              });
            }
          }
        }
      })()
    );
  }
  await Promise.all(workers);

  console.log(`解析成功需回填：${updates.length} 条`);
  const chunkSize = 50;
  for (let i = 0; i < updates.length; i += chunkSize) {
    await batchUpdate(token, updates.slice(i, i + chunkSize));
    console.log(`已回填 ${Math.min(i + chunkSize, updates.length)}/${updates.length} 条`);
  }

  console.log(`完成：成功回填 ${updates.length} 条`);
}

main().catch((e) => {
  console.error(`执行失败: ${e?.message || String(e)}`);
  process.exit(1);
});

