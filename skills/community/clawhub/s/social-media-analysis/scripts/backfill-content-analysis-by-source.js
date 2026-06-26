#!/usr/bin/env node
/**
 * 多渠道回填「内容解析」（纯 Node 版本）
 *
 * 功能：
 * - 从飞书多维表读取记录
 * - 按来源渠道（来源渠道字段）筛选：抖音APP/酷安APP/今日头条/快手APP/小红书APP 等
 * - 读取原文 URL（候选字段：获取原文URL/原文 URL/原文URL/原文url/doc_url）
 * - 解析 URL 提取标题/摘要（抖音额外解析 desc）
 * - 生成 100 字以内内容解析并写回「内容解析」
 *
 * 回填策略：
 * - 默认 ONLY_EMPTY=1：仅当「内容解析」为空时写回
 *
 * 运行：
 *   set APP_ID=...; set APP_SECRET=...; set BITABLE_URL=...
 *   node scripts/backfill-content-analysis-by-source.js
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

const ORIGINAL_URL_CANDIDATES = [
  // Clawhub 输入名：original_url_field（这里做映射兼容）
  env("ORIGINAL_URL_FIELD") || env("WEIBO_ORIGINAL_URL_FIELD"),
  "获取原文URL",
  "原文 URL",
  "原文URL",
  "原文url",
  "doc_url",
].filter(Boolean);

// 默认覆盖你表里常见渠道（不含“新浪微博”，微博由 backfill-weibo-content-analysis.js 专门处理）
const DEFAULT_CHANNELS = [
  "微信",
  "抖音APP",
  "小米社区",
  "快手APP",
  "今日头条",
  "什么值得买",
  "酷安APP",
  "搜狐",
  "小红书APP",
];
const SOURCE_CHANNELS = (env("SOURCE_CHANNELS", DEFAULT_CHANNELS.join(",")))
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);
function normalizeChannelValue(s) {
  return String(s || "")
    .replace(/\s+/g, "")
    .trim();
}

const SOURCE_CHANNELS_SET = new Set(SOURCE_CHANNELS.map((s) => normalizeChannelValue(s)));

const ONLY_EMPTY = ["1", "true", "yes"].includes((env("ONLY_EMPTY", "1")).toLowerCase());
const MAX_TARGETS = parseInt(env("LIMIT", "50"), 10);
const PAGE_SIZE = parseInt(env("PAGE_SIZE", "200"), 10);
const WORKERS = parseInt(env("WORKERS", "4"), 10);
const MAX_CHARS = parseInt(env("MAX_CHARS", "100"), 10);

const HTTP_TIMEOUT_MS = parseInt(env("HTTP_TIMEOUT_MS", "15000"), 10);
const HTTP_RETRY_TIMES = parseInt(env("HTTP_RETRY_TIMES", "1"), 10);

const UA_COMMON =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

const SOURCE_CHANNEL_VALUE_TO_PLATFORM = {
  "抖音APP": ["抖音", "视频"],
  "酷安APP": ["酷安", "图文"],
  "今日头条": ["今日头条", "图文"],
  "快手APP": ["快手", "视频"],
  "小红书APP": ["小红书", "图文"],
};

const SOURCE_CHANNEL_VALUE_TO_PLATFORM_NORM = Object.fromEntries(
  Object.entries(SOURCE_CHANNEL_VALUE_TO_PLATFORM).map(([k, v]) => [normalizeChannelValue(k), v])
);

function inferMediaFlagsFromHtml(html) {
  const s = String(html || "");
  const hasImage = /<img\b/i.test(s) || /og:image/i.test(s);
  const hasVideo =
    /<video\b/i.test(s) ||
    /\bmp4\b/i.test(s) ||
    /\bm3u8\b/i.test(s) ||
    /\bwebm\b/i.test(s);
  return { hasImage, hasVideo };
}

function inferMediaTypeFromFlags(hasImage, hasVideo) {
  if (hasVideo) return "视频";
  if (hasImage) return "图片";
  return "未知";
}

function inferDefaultFlagsFromChannel(sourceChannel) {
  // 仅对“我们已知是视频/图文”的平台给出确定结论
  const mapped = SOURCE_CHANNEL_VALUE_TO_PLATFORM_NORM[sourceChannel];
  if (!mapped) return null;
  const inferredMediaType = mapped[1];
  const hasImage = String(inferredMediaType).includes("图文");
  const hasVideo = String(inferredMediaType).includes("视频");
  if (!hasImage && !hasVideo) return null;
  return { hasImage, hasVideo };
}

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

async function withRetry(fn, retryTimes) {
  let lastErr = null;
  for (let attempt = 0; attempt <= retryTimes; attempt++) {
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

async function httpGetText(url) {
  return withRetry(async () => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), HTTP_TIMEOUT_MS);
    try {
      const resp = await fetch(url, {
        method: "GET",
        headers: { "User-Agent": UA_COMMON, Accept: "text/html,application/json,*/*" },
        redirect: "follow",
        signal: ctrl.signal,
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      return await resp.text();
    } finally {
      clearTimeout(t);
    }
  }, HTTP_RETRY_TIMES);
}

async function httpGetTextWithHeaders(url, headers) {
  return withRetry(async () => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), HTTP_TIMEOUT_MS);
    try {
      const resp = await fetch(url, {
        method: "GET",
        headers,
        redirect: "follow",
        signal: ctrl.signal,
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      return await resp.text();
    } finally {
      clearTimeout(t);
    }
  }, HTTP_RETRY_TIMES);
}

function safeText(v) {
  if (v == null) return "";
  if (Array.isArray(v)) return v.length ? String(v[0]).trim() : "";
  if (typeof v === "object") return JSON.stringify(v);
  return String(v).trim();
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

    const resp = await fetch(`${url}?${params.toString()}`, {
      method: "GET",
      headers,
      redirect: "follow",
    });
    if (!resp.ok) throw new Error(`获取记录失败 HTTP ${resp.status}`);
    const data = await resp.json();
    if (data.code !== 0) throw new Error(`获取记录失败: ${JSON.stringify(data)}`);

    const obj = data.data || {};
    const items = obj.items || [];
    for (const rec of items) {
      const fields = rec.fields || {};
      const ch = safeText(fields[SOURCE_CHANNEL_FIELD]);
      const chNorm = normalizeChannelValue(ch);
      if (!SOURCE_CHANNELS_SET.has(chNorm)) continue;

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
        source_channel: chNorm,
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

async function batchUpdateRecords(token, updates) {
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

function stripHtmlLike(s) {
  return String(s || "")
    .replace(/<[^>]*>/g, "")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/\s+/g, " ")
    .trim();
}

function extractMetaTitleDesc(html) {
  const title =
    stripHtmlLike(
      (html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["'][^>]*>/i) || [])[1]
    ) ||
    stripHtmlLike((html.match(/<title>([^<]+)<\/title>/i) || [])[1]) ||
    "";

  let desc =
    stripHtmlLike(
      (html.match(/<meta[^>]+property=["']og:description["'][^>]+content=["']([^"']+)["'][^>]*>/i) || [])[1]
    ) ||
    stripHtmlLike(
      (html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["'][^>]*>/i) || [])[1]
    ) ||
    "";

  if (!desc) {
    // JSON-LD
    const ld = html.match(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/i);
    if (ld && ld[1]) {
      try {
        const obj = JSON.parse(ld[1]);
        if (obj && typeof obj === "object") {
          desc =
            stripHtmlLike(
              obj.articleBody ||
                obj.description ||
                obj.abstract ||
                obj.text ||
                ""
            ) || "";
          // title fallback
        }
      } catch {}
    }
  }
  return [title, desc];
}

function deepFindFirstString(obj, keys, maxDepth = 6) {
  const seen = new Set();
  const stack = [{ v: obj, d: 0 }];

  while (stack.length) {
    const { v, d } = stack.pop();
    if (d > maxDepth) continue;
    if (v == null) continue;

    const type = typeof v;
    if (type === "string") {
      continue;
    }
    if (type !== "object") continue;

    if (seen.has(v)) continue;
    seen.add(v);

    if (Array.isArray(v)) {
      for (const item of v) stack.push({ v: item, d: d + 1 });
      continue;
    }

    for (const k of keys) {
      if (Object.prototype.hasOwnProperty.call(v, k)) {
        const sv = v[k];
        if (typeof sv === "string" && sv.trim()) return sv.trim();
      }
    }

    for (const vv of Object.values(v)) {
      if (vv && typeof vv === "object") stack.push({ v: vv, d: d + 1 });
    }
  }
  return "";
}

function extractFromNextData(html) {
  // 常见于 Next.js：<script id="__NEXT_DATA__" type="application/json">...</script>
  const next = html.match(/<script[^>]+id=["']__NEXT_DATA__["'][^>]*>([\s\S]*?)<\/script>/i);
  if (!next || !next[1]) return { title: "", text: "" };
  try {
    const obj = JSON.parse(next[1]);
    const title = deepFindFirstString(obj, ["title", "headline", "name"]);
    const text =
      deepFindFirstString(obj, [
        "description",
        "abstract",
        "articleBody",
        "text",
        "content",
        "caption",
        "noteContent",
        "feedDesc",
      ]) || "";
    return { title, text };
  } catch {
    return { title: "", text: "" };
  }
}

function extractTextByRegex(html, regex, maxLen = 6000) {
  const m = html.match(regex);
  if (!m) return "";
  const raw = m[1] || "";
  const s = stripHtmlLike(raw);
  if (!s) return "";
  return s.length > maxLen ? s.slice(0, maxLen) : s;
}

function extractEscapedJsonString(html, key) {
  // 从类似："key":"...转义字符串..." 里提取，并用 JSON.parse 解码 \\uXXXX / \\n 等转义
  // 适用于很多网页把文本塞进脚本 JSON 的情况（比普通 /"key":"([^"]*)"/ 更稳）
  try {
    const re = new RegExp(`"${key}"\\s*:\\s*"((?:\\\\.|[^"\\\\])*)"`,"m");
    const m = html.match(re);
    if (!m || !m[1]) return "";
    const decoded = JSON.parse(`"${m[1]}"`);
    if (typeof decoded !== "string") return "";
    return stripHtmlLike(decoded);
  } catch {
    return "";
  }
}

function extractEscapedJsonAnyKey(html, keys) {
  for (const k of keys) {
    const v = extractEscapedJsonString(html, k);
    if (v) return v;
  }
  return "";
}

function extractToutiaoId(url) {
  const m1 = String(url).match(/\/item\/(\d+)/);
  if (m1) return m1[1];
  const m2 = String(url).match(/\/i(\d+)/);
  if (m2) return m2[1];
  return "";
}

async function tryExtractToutiaoViaAltUrls(originalUrl) {
  const id = extractToutiaoId(originalUrl);
  if (!id) return { title: "", text: "" };

  const candidates = [
    // 移动端通常更可能返回预渲染内容（比原始站点 HTML 更可读）
    `https://m.toutiao.com/i${id}/`,
    // 常见文章路径变体
    `https://www.toutiao.com/a${id}/`,
    `https://www.toutiao.com/i${id}/`,
    `https://www.toutiao.com/item/${id}/`,
  ];

  for (const u of candidates) {
    try {
      const html = await httpGetText(u);
      let [title, desc] = extractMetaTitleDesc(html);
      if (!desc) {
        const next = extractFromNextData(html);
        title = title || next.title || "";
        desc = next.text || "";
      }
      if (!desc) {
        const keys = ["abstract", "description", "articleBody", "content", "text", "title", "headline"];
        desc = extractEscapedJsonAnyKey(html, ["abstract", "description", "articleBody", "content", "text"]);
        if (!title) title = extractEscapedJsonAnyKey(html, ["title", "headline", "name"]);
      }
      if (desc && desc.trim().length >= 10) return { title, text: desc };
    } catch {
      // ignore
    }
  }

  return { title: "", text: "" };
}

async function extractToutiaoWithPlaywright(url) {
  // 尽力：如果 playwright 未安装，就直接抛错并由上层忽略
  const mod = require("playwright");
  const { chromium } = mod;
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  try {
    await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
    await page.waitForTimeout(5000);
    const content = await page.evaluate(() => {
      const title =
        document.querySelector("h1")?.innerText ||
        document.querySelector('meta[property="og:title"]')?.getAttribute("content") ||
        "";
      const article =
        document.querySelector("article") ||
        document.querySelector(".article") ||
        document.body;
      const text = (article?.innerText || "").trim();
      return { title, text };
    });
    return {
      title: String(content.title || "").trim(),
      text: String(content.text || "").trim(),
    };
  } finally {
    await browser.close();
  }
}

async function extractDouyinDescFromUrl(url) {
  // 复刻 scripts/parse-douyin-video.js 的解析逻辑，只拿 desc
  let awemeId = "";
  let m = url.match(/modal_id=([0-9]+)/);
  if (m) awemeId = m[1];
  if (!awemeId) {
    m = url.match(/video\/([^/?]*)/);
    if (m) awemeId = m[1];
  }
  if (!awemeId) {
    m = url.match(/note\/([^/?]*)/);
    if (m) awemeId = m[1];
  }
  if (!awemeId) throw new Error(`无法从抖音 URL 中提取视频ID: ${url}`);

  const requestUrl = `https://www.douyin.com/jingxuan?modal_id=${awemeId}`;
  const headers = {
    "User-Agent": UA_COMMON,
    Accept:
      "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    Referer: "https://www.douyin.com/",
    Connection: "keep-alive",
  };

  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), HTTP_TIMEOUT_MS);
  try {
    const resp = await fetch(requestUrl, { method: "GET", headers, redirect: "follow", signal: ctrl.signal });
    if (!resp.ok) throw new Error(`douyin request HTTP ${resp.status}`);
    const htmlContent = await resp.text();

    const pattern = /"([^"]*?(?:playAddr|searchProps|app)[^"]*?)"/g;
    const matches = [];
    let mm;
    while ((mm = pattern.exec(htmlContent)) !== null) {
      matches.push(mm[1]);
    }
    let targetMatch = "";
    for (const s of matches) {
      if (s.includes("playAddr") && s.includes("searchProps") && s.includes("app")) {
        targetMatch = s;
        break;
      }
    }
    if (!targetMatch) throw new Error("未找到包含视频数据的 JSON 片段");
    const decodedJson = decodeURIComponent(targetMatch);
    const videoDataJson = JSON.parse(decodedJson);
    const videoDetail = (((videoDataJson || {}).app || {}).videoDetail) || {};
    const desc = videoDetail.desc || "";
    return { title: desc || "", text: desc || "" };
  } finally {
    clearTimeout(t);
  }
}

async function extractBySourceChannel(sourceChannel, originalUrl) {
  const [platform, mediaType] =
    SOURCE_CHANNEL_VALUE_TO_PLATFORM_NORM[sourceChannel] || [sourceChannel, "未知"];

  if (sourceChannel === "抖音APP") {
    const { title, text } = await extractDouyinDescFromUrl(originalUrl);
    const hasImage = false;
    const hasVideo = true;
    return { title, text, visual: "", platform, mediaType: "视频", hasImage, hasVideo };
  }

  // 默认：普通抓取 HTML（用于酷安/今日头条/快手/小红书等尽力提取 meta/json）
  let html = await httpGetText(originalUrl);

  // 小红书：如果提供了 Cookie，尽可能拿到内容
  if (sourceChannel === "小红书APP") {
    const xhsCookie = env("XHS_COOKIE");
    if (xhsCookie.trim()) {
      try {
        html = await httpGetTextWithHeaders(originalUrl, {
          Cookie: xhsCookie,
          "User-Agent": UA_COMMON,
          Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        });
      } catch {
        // 继续使用第一次抓到的 html
      }
    }
  }

  let [title, desc] = extractMetaTitleDesc(html);
  if (!desc) {
    // 再尝试从 Next.js 数据结构里抽取
    const next = extractFromNextData(html);
    title = title || next.title || "";
    desc = next.text || "";
  }
  if (!desc) {
    // 再尝试一些常见键名的字符串抽取（best-effort，避免过度依赖站点结构）
    const maybeKeysMap = {
      "酷安APP": ["desc", "description", "content", "feedDesc"],
      "快手APP": ["caption", "description", "text", "title", "feedDesc"],
      "今日头条": ["abstract", "description", "articleBody", "content", "text"],
      "小红书APP": ["noteContent", "desc", "description", "text", "content"],
    };
    const keys = maybeKeysMap[sourceChannel];
    if (keys) {
      desc = extractEscapedJsonAnyKey(html, keys);
      if (!title) title = extractEscapedJsonAnyKey(html, ["title", "headline", "name"]);
    }
  }

  // 今日头条：若仍然没有正文摘要，尝试 Playwright 渲染提取 innerText
  if (sourceChannel === "今日头条" && (!desc || desc.length < 10)) {
    // 1) 先尝试移动端/备用路径（不依赖 playwright）
    try {
      const alt = await tryExtractToutiaoViaAltUrls(originalUrl);
      if (alt.text && alt.text.length >= 10) {
        title = title || alt.title || "";
        desc = alt.text;
      }
    } catch {
      // ignore
    }
  }

  if (sourceChannel === "今日头条" && (!desc || desc.length < 10)) {
    // 2) 仍然没有，再尝试 Playwright 渲染提取 innerText（需要 playwright 依赖）
    try {
      const content = await extractToutiaoWithPlaywright(originalUrl);
      title = title || content.title || "";
      if (content.text && content.text.length) desc = content.text;
    } catch {
      // 忽略：playwright 可能未安装/站点反爬
    }
  }

  let visual = "";
  if (!desc && title) visual = `标题：${title}`;
  const defaults = inferDefaultFlagsFromChannel(sourceChannel);
  let hasImage;
  let hasVideo;
  let inferredMediaType;
  if (defaults) {
    hasImage = defaults.hasImage;
    hasVideo = defaults.hasVideo;
    inferredMediaType = inferMediaTypeFromFlags(hasImage, hasVideo);
  } else {
    const flags = inferMediaFlagsFromHtml(html);
    hasImage = flags.hasImage;
    hasVideo = flags.hasVideo;
    inferredMediaType = inferMediaTypeFromFlags(hasImage, hasVideo);
  }

  const mediaTypeFinal = inferredMediaType === "未知" ? mediaType : inferredMediaType;
  return {
    title: title || "",
    text: desc || "",
    visual,
    platform,
    mediaType: mediaTypeFinal,
    hasImage,
    hasVideo,
  };
}

function buildContentAnalysis({ title, text, platform, mediaType, visual }) {
  const res = buildAnalysis({
    title: title || "",
    text: text || "",
    platform: platform || "",
    mediaType: mediaType || "",
    visual: visual || "",
    maxChars: MAX_CHARS,
  });
  return res.analysis || "";
}

async function worker({ token, targets, idxStart, workerId }) {
  let idx = idxStart;
  const updates = [];
  while (idx < targets.length) {
    const t = targets[idx];
    idx += WORKERS;
    const { record_id, source_channel, original_url, need_content, need_link, need_img, need_video } = t;
    try {
      const parsed = await extractBySourceChannel(source_channel, original_url);
      const valid = true;

      const defaults = inferDefaultFlagsFromChannel(source_channel);
      const hasImage = !!parsed.hasImage;
      const hasVideo = !!parsed.hasVideo;

      const fields = {};
      if (need_link) fields[LINK_STATUS_FIELD] = valid ? "是" : "否";
      if (need_img) {
        if (defaults || hasImage) fields[HAS_IMAGE_FIELD] = hasImage ? "是" : "否";
      }
      if (need_video) {
        if (defaults || hasVideo) fields[HAS_VIDEO_FIELD] = hasVideo ? "是" : "否";
      }

      if (need_content) {
        const contentVal =
          parsed.title || parsed.text ? buildContentAnalysis(parsed) : "";
        if (contentVal) fields[CONTENT_ANALYSIS_FIELD] = contentVal;
      }

      if (Object.keys(fields).length) {
        updates.push({ record_id, fields });
      }
      console.log(`  worker#${workerId} ok record_id=${record_id}`);
    } catch (e) {
      console.log(`  worker#${workerId} err record_id=${record_id}: ${e && e.message ? e.message : String(e)}`);
      const defaults = inferDefaultFlagsFromChannel(source_channel);
      const hasImage = defaults ? defaults.hasImage : false;
      const hasVideo = defaults ? defaults.hasVideo : false;

      const fields = {};
      if (need_link) fields[LINK_STATUS_FIELD] = "否";
      // 仅当渠道已知“确定类型”时才回填图片/视频；否则避免误写“否”
      if (need_img && defaults) fields[HAS_IMAGE_FIELD] = hasImage ? "是" : "否";
      if (need_video && defaults) fields[HAS_VIDEO_FIELD] = hasVideo ? "是" : "否";
      if (Object.keys(fields).length) {
        updates.push({ record_id, fields });
      }
    }
  }
  return updates;
}

async function main() {
  const TEST_URL = (process.env.TEST_URL || "").trim();
  const TEST_CHANNEL = (process.env.TEST_CHANNEL || "").trim();
  if (TEST_URL && TEST_CHANNEL) {
    const testChannelNorm = normalizeChannelValue(TEST_CHANNEL);
    const parsed = await extractBySourceChannel(testChannelNorm, TEST_URL);
    const contentVal = buildContentAnalysis(parsed);
    const hasImage = !!parsed.hasImage;
    const hasVideo = !!parsed.hasVideo;
    console.log(
      JSON.stringify(
        {
          test_channel: TEST_CHANNEL,
          test_url: TEST_URL,
          parsed,
          content_analysis: contentVal,
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

  if (!BITABLE_URL) throw new Error("请设置环境变量 BITABLE_URL（飞书多维表链接）");

  const token = await getTenantAccessToken();
  console.log("获取飞书 token 成功");

  const targets = await fetchTargets(token);
  console.log(`筛选到需要处理的记录：${targets.length} 条（渠道：${SOURCE_CHANNELS.join(", ")})`);
  if (!targets.length) return;

  const t0 = Date.now();
  const allUpdates = [];

  // 简单并发 worker：避免引入第三方依赖
  const workers = [];
  for (let w = 0; w < WORKERS; w++) {
    workers.push(worker({ token, targets, idxStart: w, workerId: w + 1 }));
  }
  const results = await Promise.all(workers);
  for (const arr of results) allUpdates.push(...arr);

  console.log(`解析成功需要回填：${allUpdates.length} 条（耗时 ${((Date.now() - t0) / 1000).toFixed(1)}s）`);
  if (!allUpdates.length) return;

  // 批量更新
  const chunkSize = 50;
  for (let i = 0; i < allUpdates.length; i += chunkSize) {
    await batchUpdateRecords(token, allUpdates.slice(i, i + chunkSize));
    console.log(`已回填 ${Math.min(i + chunkSize, allUpdates.length)}/${allUpdates.length} 条`);
  }

  console.log(`完成：成功回填 ${allUpdates.length} 条`);
}

main().catch((e) => {
  console.error(`执行失败: ${e && e.message ? e.message : String(e)}`);
  process.exit(1);
});

