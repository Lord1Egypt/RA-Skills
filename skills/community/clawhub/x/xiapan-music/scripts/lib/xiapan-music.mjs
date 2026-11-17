// AUTO-GENERATED FILE — 不要手改这个文件。
// 源文件：src/core/xiapan-music.mjs（唯一真相源）
// @generated sha256: 7a8677551306d60debd3c5bc9cc4e1ac3b68d35e9a8d251a96c0f0a92396d051
// @generated at: 2026-10-28T02:31:55.385Z
// 同步命令：node scripts/sync-core.mjs（校验：node scripts/sync-core.mjs --check）
// @generated end

// 虾盘云音乐（Xiapan Music）核心客户端 · 唯一真相源
// 纯 ESM、零 npm 依赖、Node >= 18；允许注入 fetch 便于测试。
//
// ⚠️ 本文件是生成源。`skills/xiapan-music/scripts/lib/xiapan-music.mjs`
//    由 `scripts/sync-core.mjs` 从本文件复制，只替换文件头注释（含 sha256），
//    不要手改拷贝。也不要在这里读/写任何凭据文件（Key 只从参数/env/device.json 取）。
//
// 接口契约见 docs/PLAN.md §3 与 docs/api-contract.md。

import { readFileSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";

/** 线上 API 基址（国内外均可达；api.u-claw.org 境外不稳，勿用） */
export const API_BASE = "https://api.u-claw.org.cn";

/** Suno 音乐模型：一次提交出 2 首，约 ¥2.4/次（合 ¥1.2/首，以实际扣费为准；2026-10-28 真机实测） */
export const DEFAULT_MV = "chirp-v5-5";
/** 文字模型（写歌词）：deepseek-v4-flash，必须关闭 thinking 否则只回 reasoning_content */
export const DEFAULT_TEXT_MODEL = "deepseek-v4-flash";
/** 纯音乐 / BGM 模型：minimax-music-v2.6，约 ¥1/首 */
export const DEFAULT_BGM_MODEL = "minimax-music-v2.6";

/** 成本文案：只作「约」，禁止编造精确扣费，实际以账单为准（2026-10-28 真机实测：一次提交 2 首扣 ¥2.4） */
export const COST_HINT = {
  song: "一次提交约 ¥2.4（一次出 2 首，约 ¥1.2/首，以实际扣费为准）",
  bgm: "BGM 约 ¥1/首（以实际扣费为准）",
  lyrics: "写歌词成本可忽略（文本模型，约 ¥0.01 以内）；出歌另计约 ¥2.4/次（2 首）",
};

/** 无风格输入时的兜底英文风格标签（Suno tags） */
export const DEFAULT_TAGS = "Mandarin pop, warm vocal, acoustic guitar, soft drums, 96 BPM, hopeful";

/** 导流落点（所有 CTA 都从这里取，避免各处手写漂移） */
export const CTA = {
  board: "https://tu.u-claw.org.cn",
  registerKey: "https://api.u-claw.org.cn",
  recharge: "https://api.u-claw.org.cn/recharge",
  campaign: "xiapan-music",
};

/** 错误码：BAD_KEY | NO_BALANCE | RATE_LIMIT | BAD_REQUEST | TASK_FAILED | TIMEOUT | NETWORK */
export class XiapanMusicError extends Error {
  /**
   * @param {string} code
   * @param {string} message 已脱敏、可直接给用户看的中文说明
   * @param {object} [details] 附加信息（HTTP 状态、apiMessage、taskId 等；绝不含完整 Key）
   */
  constructor(code, message, details = {}) {
    super(message);
    this.name = "XiapanMusicError";
    this.code = code;
    this.details = details;
  }
}

// ---------------------------------------------------------------------------
// 小工具
// ---------------------------------------------------------------------------

/** 只保留 Key 前 8 位用于日志 / 报错（红线：任何输出不得含完整 Key） */
export function maskKey(key) {
  const k = typeof key === "string" ? key.trim() : "";
  if (!k) return "";
  return k.length <= 8 ? `${k.slice(0, 2)}…` : `${k.slice(0, 8)}…`;
}

const PLACEHOLDER_KEY = /^(your|xxx|placeholder|sk-\.\.\.|sk-xxx|填入|你的|<)/i;

/** 校验并清洗 Key：占位符/过短直接视为未配置 */
function cleanKey(key) {
  if (typeof key !== "string") return "";
  const k = key.trim().replace(/^Bearer\s+/i, "");
  if (!k || k.length < 8 || PLACEHOLDER_KEY.test(k) || /\s/.test(k)) return "";
  return k;
}

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

function num(v, fallback = 0) {
  const n = typeof v === "number" ? v : Number.parseFloat(v);
  return Number.isFinite(n) ? n : fallback;
}

/** 把 api.u-claw.org 直链改写到 .cn（旧数据里的直链可能是短域） */
export function normalizeMediaUrl(url) {
  const s = String(url || "").trim();
  if (!s) return "";
  return s.replace("://api.u-claw.org/", "://api.u-claw.org.cn/");
}

function sanitizeFileName(name, fallback = "song") {
  const base = String(name || "")
    .replace(/[\\/:*?"<>|\r\n\t]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 48);
  return base || fallback;
}

// ---------------------------------------------------------------------------
// Key 解析：--key > XIAPAN_API_KEY > ~/.dsh/.credentials.yaml 的 refs（由 DSH 插件注入为环境变量）
//            > ~/.uking/device.json 的 key
// ---------------------------------------------------------------------------

/**
 * @param {{ key?: string, env?: object, deviceFile?: string }} [opts]
 * @returns {string}
 */
export function resolveKey({ key, env = process.env, deviceFile } = {}) {
  const explicit = cleanKey(key);
  if (explicit) return explicit;

  const fromEnv = cleanKey(env && env.XIAPAN_API_KEY);
  if (fromEnv) return fromEnv;

  const file = deviceFile || join(homedir(), ".uking", "device.json");
  try {
    const j = JSON.parse(readFileSync(file, "utf8"));
    const fromDevice = cleanKey(j && j.key);
    if (fromDevice) return fromDevice;
  } catch {
    // 文件不存在 / 不可读 / 非 JSON：继续走报错
  }

  throw new XiapanMusicError(
    "BAD_KEY",
    "找不到虾盘云 API Key。任选一种：①命令加 --key；②设置环境变量 XIAPAN_API_KEY（DSH 用户写在 ~/.dsh/.credentials.yaml 的 refs 下）；③装机了 U-King 的电脑会自动用 ~/.uking/device.json。领 Key：https://api.u-claw.org.cn",
    { tried: ["--key", "XIAPAN_API_KEY", file] },
  );
}

// ---------------------------------------------------------------------------
// HTTP 底座
// ---------------------------------------------------------------------------

function classifyHttpError(status, json, text, path) {
  const apiMessage =
    (json && json.error && (json.error.message || json.error.type)) ||
    (json && json.message) ||
    (typeof json === "string" ? json : "") ||
    String(text || "").slice(0, 200);
  const details = { status, apiMessage, path };
  const msg = String(apiMessage || "");

  if (status === 401) {
    return new XiapanMusicError(
      "BAD_KEY",
      `Key 校验失败（HTTP 401）：${msg || "Invalid token"}。可能是 Key 无效，或账户余额不足后 new-api 统一返回 401；先查余额再换 Key。`,
      details,
    );
  }
  if (status === 402 || /insufficient_quota|insufficient balance|余额不足/i.test(msg)) {
    return new XiapanMusicError(
      "NO_BALANCE",
      `余额不足（HTTP ${status}）：${msg || "insufficient_quota"}。充值：https://api.u-claw.org.cn/recharge`,
      details,
    );
  }
  if (status === 403) {
    return new XiapanMusicError(
      "BAD_KEY",
      `Key 无权调用音乐模型（HTTP 403）：${msg}。请在虾盘云令牌设置里放行 suno_music / suno_lyrics，或更换一把 Key。`,
      details,
    );
  }
  if (status === 429) {
    return new XiapanMusicError("RATE_LIMIT", `请求太频繁（HTTP 429）：${msg}。稍等再试，不要自动重试付费提交。`, details);
  }
  if (status >= 500) {
    return new XiapanMusicError("NETWORK", `服务端异常（HTTP ${status}）：${msg || "upstream error"}。可稍后重试查询，不要重复提交付费任务。`, details);
  }
  return new XiapanMusicError("BAD_REQUEST", `请求被拒绝（HTTP ${status}）：${msg || "bad request"}`, details);
}

/**
 * 统一 JSON 请求。网络错误 → NETWORK；超时 → TIMEOUT；HTTP 错误 → 细分错误码。
 * @returns {Promise<{status:number, json:any}>}
 */
async function requestJson(method, path, { key, body, fetchImpl, timeoutMs = 60_000, baseUrl = API_BASE } = {}) {
  const doFetch = fetchImpl || globalThis.fetch;
  if (typeof doFetch !== "function") {
    throw new XiapanMusicError("NETWORK", "当前运行环境没有 fetch（需要 Node >= 18 或注入 fetch）", { path });
  }
  const controller = typeof AbortController === "function" ? new AbortController() : null;
  const timer = controller && timeoutMs > 0 ? setTimeout(() => controller.abort(), timeoutMs) : null;
  const headers = { Accept: "application/json" };
  if (key) headers.Authorization = `Bearer ${key}`;
  if (body !== undefined) headers["Content-Type"] = "application/json";
  try {
    const res = await doFetch(`${baseUrl}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller ? controller.signal : undefined,
    });
    const text = await res.text();
    let json = null;
    if (text) {
      try {
        json = JSON.parse(text);
      } catch {
        json = null;
      }
    }
    if (!res.ok) throw classifyHttpError(res.status, json, text, path);
    if (json === null) {
      throw new XiapanMusicError("NETWORK", `服务端返回了非 JSON 响应（${method} ${path}）`, {
        path,
        sample: String(text || "").slice(0, 120),
      });
    }
    return { status: res.status, json };
  } catch (err) {
    if (err instanceof XiapanMusicError) throw err;
    if (err && (err.name === "AbortError" || /aborted/i.test(String(err.message || "")))) {
      throw new XiapanMusicError("TIMEOUT", `请求超时（${timeoutMs}ms）：${method} ${path}`, { path, timeoutMs });
    }
    throw new XiapanMusicError("NETWORK", `网络请求失败：${(err && err.message) || err}`, {
      path,
      cause: String((err && err.message) || err),
    });
  } finally {
    if (timer) clearTimeout(timer);
  }
}

// ---------------------------------------------------------------------------
// 余额
// ---------------------------------------------------------------------------

/**
 * 查询余额（不扣费）。token 余额 = (hard_limit_usd - total_usage/100) × 500000; ¥1 = 500000 token。
 * @returns {Promise<{totalToken:number, usedToken:number, remainToken:number, remainCny:number}>}
 */
export async function queryBalance(key, opts = {}) {
  const k = resolveKey({ key, env: opts.env, deviceFile: opts.deviceFile });
  const [sub, usage] = await Promise.all([
    requestJson("GET", "/v1/dashboard/billing/subscription", { ...opts, key: k }),
    requestJson("GET", `/v1/dashboard/billing/usage?start_date=2020-01-01&end_date=${todayStr()}`, { ...opts, key: k }),
  ]);
  const hardLimitUsd = num(sub.json && sub.json.hard_limit_usd);
  const totalUsageCents = num(usage.json && usage.json.total_usage);
  const totalToken = Math.round(hardLimitUsd * 500000);
  const usedToken = Math.round((totalUsageCents / 100) * 500000);
  const remainToken = Math.max(0, totalToken - usedToken);
  return {
    totalToken,
    usedToken,
    remainToken,
    remainCny: +(remainToken / 500000).toFixed(2),
    hardLimitUsd,
    totalUsageCents,
  };
}

// ---------------------------------------------------------------------------
// 写歌词（文本模型，成本≈0）
// ---------------------------------------------------------------------------

const LANGUAGE_NAMES = {
  zh: "简体中文",
  "zh-cn": "简体中文",
  "zh-tw": "繁体中文",
  en: "English",
  ja: "日本語",
  ko: "한국어",
};

const LYRIC_SYSTEM_PROMPT = [
  "你是一位专业作词人，为 AI 音乐模型写可直接演唱的完整歌词。",
  "只输出一个 JSON 对象，形如 {\"title\":\"歌名\",\"tags\":\"风格标签\",\"lyrics\":\"带结构标签的歌词\"}；",
  "不要解释、不要 Markdown 代码块、不要在 JSON 外写任何字。",
  "要求：",
  "- lyrics 用 [Verse 1]、[Pre-Chorus]、[Chorus]、[Bridge]、[Outro] 等标签分段；总行数 20-32 行，适合演唱 2-4 分钟；",
  "- 每行 8-16 字，押韵自然、有画面感；副歌重复、上口；不要在歌词里写任何括号说明；",
  "- tags 是英文逗号分隔的风格词，覆盖曲风/情绪/BPM/配器/人声，不超过 120 个字符，",
  "  例如 \"Mandarin indie folk pop, 96 BPM, warm male vocal, acoustic guitar, hopeful\"；",
  "- title 不超过 20 个汉字，不含引号。",
].join("\n");

function buildLyricUserPrompt({ theme, style, language, title }) {
  const langName = LANGUAGE_NAMES[String(language || "zh").toLowerCase()] || language || "简体中文";
  const lines = [`主题/需求：${String(theme || "").trim() || "自由发挥，写一首温暖治愈的流行歌"}`];
  if (title) lines.push(`希望的歌名（可微调）：${title}`);
  if (style) lines.push(`希望的音乐风格：${style}`);
  lines.push(`歌词语言：${langName}`);
  return lines.join("\n");
}

/**
 * 从模型输出里容错解析 {title,tags,lyrics}：支持 ```json 围栏、前后缀话术、JSON 字符串。
 * @returns {{title:string, tags:string, lyrics:string}}
 */
export function parseLyricsJson(text) {
  const raw = String(text == null ? "" : text).trim();
  if (!raw) throw new XiapanMusicError("BAD_REQUEST", "歌词模型返回了空内容");

  const candidates = [];
  const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fenced) candidates.push(fenced[1].trim());
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start >= 0 && end > start) candidates.push(raw.slice(start, end + 1));
  candidates.push(raw);

  for (const c of candidates) {
    try {
      const obj = JSON.parse(c);
      const out = pickLyricFields(obj);
      if (out) return out;
    } catch {
      // 尝试下一个候选
    }
  }

  // 兜底：字段级正则（模型有时漏了 JSON 引号 / 用多行文本）
  const title = (raw.match(/"title"\s*:\s*"([^"]*)"/) || raw.match(/歌名[:：]\s*(.+)/) || [])[1];
  const tags = (raw.match(/"tags"\s*:\s*"([^"]*)"/) || raw.match(/风格[:：]\s*(.+)/) || [])[1];
  const lyricsMatch = raw.match(/"lyrics"\s*:\s*"([\s\S]*?)"\s*[,}]/);
  if (lyricsMatch) {
    let lyrics = lyricsMatch[1];
    try {
      lyrics = JSON.parse(`"${lyrics}"`);
    } catch {
      // 保留原始转义字面量
    }
    if (String(lyrics).trim()) {
      return {
        title: String(title || "").trim() || "未命名歌曲",
        tags: normalizeTags(tags),
        lyrics: String(lyrics).replace(/\\n/g, "\n").trim(),
      };
    }
  }
  throw new XiapanMusicError("BAD_REQUEST", "歌词模型没有返回可解析的 {title,tags,lyrics} JSON", {
    sample: raw.slice(0, 200),
  });
}

function pickLyricFields(obj) {
  if (!obj || typeof obj !== "object") return null;
  const lyrics = typeof obj.lyrics === "string" ? obj.lyrics.trim() : "";
  if (!lyrics) return null;
  return {
    title: normalizeTitle(obj.title),
    tags: normalizeTags(obj.tags),
    lyrics,
  };
}

function normalizeTitle(title) {
  const s = typeof title === "string" ? title.trim().replace(/^["'《]+|["'》]+$/g, "").trim() : "";
  return s.slice(0, 40) || "未命名歌曲";
}

function normalizeTags(tags) {
  if (Array.isArray(tags)) return tags.map((t) => String(t).trim()).filter(Boolean).join(", ").slice(0, 1000);
  if (typeof tags === "string") return tags.trim().replace(/\s*\n\s*/g, ", ").slice(0, 1000);
  return "";
}

/**
 * 写歌词。成本≈0；不提交任何付费任务。
 * 产出的歌词必须能直接当 Suno prompt 用：带结构标签、≥8 行、120-5000 字；
 * 不合格会自动免费重试一次（只重试文本模型，不涉及扣费）。
 * @param {{theme?:string, prompt?:string, style?:string, language?:string, title?:string, model?:string}} input
 * @param {string} [key]
 * @param {object} [opts] requestJson 可选项（fetchImpl / timeoutMs / baseUrl / lyricAttempts）
 * @returns {Promise<{title:string, tags:string, lyrics:string}>}
 */
export async function writeLyrics(input = {}, key, opts = {}) {
  const k = resolveKey({ key, env: opts.env, deviceFile: opts.deviceFile });
  const theme = input.theme || input.prompt || "";
  const attempts = Math.max(1, Math.min(3, opts.lyricAttempts || 2));
  let extraHint = "";
  let lastError = null;

  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const body = {
      model: input.model || DEFAULT_TEXT_MODEL,
      messages: [
        { role: "system", content: LYRIC_SYSTEM_PROMPT },
        { role: "user", content: buildLyricUserPrompt({ ...input, theme }) + extraHint },
      ],
      // 必须关闭 thinking，否则 deepseek-v4 只返回 reasoning_content
      thinking: { type: "disabled" },
      temperature: 0.9,
      max_tokens: 3000,
    };
    const { json } = await requestJson("POST", "/v1/chat/completions", { ...opts, key: k, body, timeoutMs: opts.timeoutMs || 120_000 });
    const choice = (json.choices && json.choices[0]) || {};
    const message = choice.message || {};
    const content = typeof message.content === "string" ? message.content : "";
    if (!content.trim()) {
      const reasoning = typeof message.reasoning_content === "string" ? message.reasoning_content : "";
      lastError = new XiapanMusicError(
        "BAD_REQUEST",
        reasoning
          ? "歌词模型只返回了 reasoning_content（thinking 未关闭），请检查请求体 thinking 字段"
          : "歌词模型返回了空内容",
        { finishReason: choice.finish_reason },
      );
      extraHint = "\n\n注意：上一次没有返回内容，请直接输出 JSON。";
      continue;
    }
    let parsed;
    try {
      parsed = parseLyricsJson(content);
    } catch (err) {
      lastError = err;
      extraHint = "\n\n注意：上一次输出无法解析为 JSON，请严格只输出 {\"title\":...,\"tags\":...,\"lyrics\":...}。";
      continue;
    }
    if (input.title) parsed.title = normalizeTitle(input.title);
    if (!parsed.tags) parsed.tags = DEFAULT_TAGS;
    if (isUsableLyrics(parsed.lyrics)) return parsed;
    lastError = new XiapanMusicError(
      "BAD_REQUEST",
      "歌词模型返回的歌词不够完整（需带 [Verse]/[Chorus] 等结构标签、≥8 行、120-5000 字）",
      { chars: parsed.lyrics.length },
    );
    extraHint = "\n\n注意：上一次歌词太短或缺少结构标签，请按 20-32 行、带 [Verse 1]/[Chorus]/[Bridge] 标签重写。";
  }
  throw lastError;
}

// ---------------------------------------------------------------------------
// 出歌（Suno，异步任务，一次提交出 2 首；提交即扣费，禁止自动重试提交）
// ---------------------------------------------------------------------------

export const SUNO_TASK_STATUS = {
  done: new Set(["SUCCESS", "COMPLETE", "COMPLETED"]),
  failed: new Set(["FAILURE", "FAILED", "ERROR", "ERRORED", "CANCELLED", "CANCELED"]),
  running: new Set(["SUBMITTED", "NOT_START", "PENDING", "QUEUED", "IN_PROGRESS", "PROCESSING", "RUNNING"]),
};

const STRUCTURE_TAG = /[\[【](verse|chorus|bridge|intro|outro|pre[- ]?chorus|hook|interlude|final chorus|refrain)[\]】]/i;

/**
 * 判断一段文本是否「像歌词」而不是一句风格描述。
 * 硬规则：一句风格描述绝不能直接当 prompt 提交给 Suno（实测只出 ~30s clip）。
 * 判定：含 [Verse]/[Chorus] 等结构标签，或 ≥6 行非空文本且 ≥80 字。
 */
export function looksLikeLyrics(text) {
  const s = String(text || "").trim();
  if (!s) return false;
  if (STRUCTURE_TAG.test(s)) return true;
  const lines = s.split(/\r?\n/).filter((l) => l.trim());
  return lines.length >= 6 && s.length >= 80;
}

/** 是否是可提交的完整歌词（长度/结构够一首歌） */
export function isUsableLyrics(text) {
  const s = String(text || "").trim();
  if (s.length < 120 || s.length > 5000) return false;
  const lines = s.split(/\r?\n/).filter((l) => l.trim());
  return looksLikeLyrics(s) && lines.length >= 8;
}

/**
 * 提交出歌任务。一次调用 = 一次提交 = 一次扣费；本函数绝不重试。
 * @param {{prompt?:string, lyrics?:string, title?:string, tags?:string, mv?:string, instrumental?:boolean}} input
 * @param {string} [key]
 * @param {object} [opts]
 * @returns {Promise<{taskId:string, mv:string}>}
 */
export async function submitSong(input = {}, key, opts = {}) {
  const k = resolveKey({ key, env: opts.env, deviceFile: opts.deviceFile });
  const prompt = String(input.prompt || input.lyrics || "").trim();
  if (!prompt) {
    throw new XiapanMusicError("BAD_REQUEST", "缺少歌词或歌曲描述（prompt/lyrics）");
  }
  // 硬规则：有歌词就必须是完整歌词（一句风格描述直接当 prompt 只会出 ~30s clip）。
  // 纯音乐（instrumental）例外：prompt 只放风格描述。
  if (opts.requireLyrics === true && input.instrumental !== true && !looksLikeLyrics(prompt)) {
    throw new XiapanMusicError(
      "BAD_REQUEST",
      "prompt 看起来是一句风格描述而不是完整歌词：请先用 writeLyrics 生成带 [Verse]/[Chorus] 标签的完整歌词再提交（纯音乐请传 instrumental:true）",
      { promptChars: prompt.length },
    );
  }
  if (prompt.length > 5000) {
    throw new XiapanMusicError("BAD_REQUEST", `歌词太长（${prompt.length} 字，上限 5000）`);
  }
  const tags = String(input.tags || "").trim();
  if (tags.length > 1000) {
    throw new XiapanMusicError("BAD_REQUEST", `风格标签太长（${tags.length} 字，上限 1000）`);
  }
  const mv = String(input.mv || DEFAULT_MV).trim();
  const body = { prompt, tags, title: String(input.title || "").trim(), mv };
  if (input.instrumental === true) body.make_instrumental = true;

  const { json } = await requestJson("POST", "/suno/submit/music", { ...opts, key: k, body, timeoutMs: opts.timeoutMs || 120_000 });
  const data = json && json.data;
  const taskId =
    typeof data === "string" ? data : data && (data.task_id || data.taskId || data.id) ? String(data.task_id || data.taskId || data.id) : "";
  const success = json && (json.code === "success" || json.code === "SUCCESS" || json.code === 200 || json.success === true);
  if (!success && !taskId) {
    const message = (json && (json.message || (json.error && json.error.message))) || "提交被拒绝";
    throw new XiapanMusicError("BAD_REQUEST", `提交失败：${message}`, { taskId: taskId || null, body: json });
  }
  if (!taskId) {
    // 2xx 但没 task_id：服务端可能已扣费；禁止自动重试，提示人工核对
    throw new XiapanMusicError(
      "BAD_REQUEST",
      "服务端已接受但未返回 task_id，可能已扣费：请到虾盘云账单核对，不要自动重试提交",
      { body: json },
    );
  }
  return { taskId, mv };
}

/**
 * 把 /suno/fetch 的 data.data 数组归一化为 clip 列表（纯函数，便于单测）。
 */
export function normalizeClips(list) {
  if (!Array.isArray(list)) return [];
  const clips = [];
  for (const c of list) {
    if (!c || typeof c !== "object") continue;
    const audioUrl = normalizeMediaUrl(c.audio_url || c.audioUrl || c.media_url || "");
    if (!audioUrl) continue;
    clips.push({
      clipId: String(c.clip_id || c.id || ""),
      title: String(c.title || "").trim(),
      duration: num(c.duration),
      model: String(c.model_name || c.model || ""),
      mv: String(c.major_model_version || c.mv || ""),
      audioUrl,
      imageUrl: normalizeMediaUrl(c.image_url || c.imageUrl || c.image_large_url || ""),
      status: String(c.status || ""),
    });
  }
  return clips;
}

/**
 * 轮询任务直到成功/失败/超时。轮询期间允许对网络错误做有限重试（付费提交不重试）。
 * @param {string} taskId
 * @param {{key?:string, intervalMs?:number, timeoutMs?:number, onProgress?:Function, fetchImpl?:Function, baseUrl?:string, maxNetworkRetries?:number}} [options]
 * @returns {Promise<{status:"completed", taskId:string, clips:Array<object>, raw:any}>}
 */
export async function waitSong(taskId, options = {}) {
  const k = resolveKey({ key: options.key, env: options.env, deviceFile: options.deviceFile });
  const intervalMs = Math.max(options.minIntervalMs || 1_000, options.intervalMs || 5_000);
  const timeoutMs = options.timeoutMs || 600_000;
  const maxNetworkRetries = options.maxNetworkRetries == null ? 5 : options.maxNetworkRetries;
  if (!taskId) throw new XiapanMusicError("BAD_REQUEST", "缺少 taskId");
  const startedAt = Date.now();
  let networkFailures = 0;
  let notFoundRetries = 0;
  const maxNotFoundRetries = options.maxNotFoundRetries == null ? 6 : options.maxNotFoundRetries;
  let last = null;

  while (Date.now() - startedAt < timeoutMs) {
    await sleep(intervalMs);
    let res;
    try {
      res = await requestJson("GET", `/suno/fetch/${encodeURIComponent(taskId)}`, {
        key: k,
        fetchImpl: options.fetchImpl,
        baseUrl: options.baseUrl,
        timeoutMs: options.pollTimeoutMs || 30_000,
      });
      networkFailures = 0;
    } catch (err) {
      // 提交后任务可能还没入库（task_not_found），前几次正常，给一段宽限
      const apiMessage = err && err.details && err.details.apiMessage;
      const isTaskNotFound = /task_not_found|task not found/i.test(String(apiMessage || ""));
      if (isTaskNotFound && notFoundRetries < maxNotFoundRetries) {
        notFoundRetries += 1;
        continue;
      }
      // 轮询期间允许对网络错误做有限重试；付费提交不重试
      if (err instanceof XiapanMusicError && (err.code === "NETWORK" || err.code === "TIMEOUT") && networkFailures < maxNetworkRetries) {
        networkFailures += 1;
        continue;
      }
      throw err;
    }

    const payload = (res.json && res.json.data) || {};
    const status = String(payload.status || "").toUpperCase();
    const progress = num(String(payload.progress || "").replace("%", ""));
    const clips = normalizeClips(payload.data);
    last = { status, progress, clips, raw: res.json };

    if (typeof options.onProgress === "function") {
      options.onProgress({
        status,
        progress,
        clips: clips.length,
        elapsedMs: Date.now() - startedAt,
      });
    }

    if (SUNO_TASK_STATUS.done.has(status)) {
      if (!clips.length) {
        throw new XiapanMusicError("TASK_FAILED", `任务 ${taskId} 标记成功但没有返回音轨`, {
          taskId,
          failReason: (payload && payload.fail_reason) || "",
        });
      }
      return { status: "completed", taskId, clips, raw: payload };
    }
    if (SUNO_TASK_STATUS.failed.has(status)) {
      const reason = payload.fail_reason || payload.error || "上游生成失败";
      throw new XiapanMusicError("TASK_FAILED", `生成失败：${typeof reason === "string" ? reason : JSON.stringify(reason)}`, {
        taskId,
        status,
      });
    }
  }

  throw new XiapanMusicError("TIMEOUT", `等待超过 ${Math.round(timeoutMs / 1000)}s 任务仍未完成（最后状态 ${last ? last.status : "未知"}）`, {
    taskId,
    lastStatus: last ? last.status : "",
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * 下载单个音频到本地（媒体直链无需鉴权）。
 * @returns {Promise<{file:string, bytes:number}>}
 */
export async function downloadClip(url, outFile, opts = {}) {
  const doFetch = opts.fetchImpl || globalThis.fetch;
  const mediaUrl = normalizeMediaUrl(url);
  if (!mediaUrl) throw new XiapanMusicError("BAD_REQUEST", "缺少音频 url");
  if (!outFile) throw new XiapanMusicError("BAD_REQUEST", "缺少输出文件路径");
  const res = await doFetch(mediaUrl, { signal: makeTimeoutSignal(opts.timeoutMs || 180_000) });
  if (!res.ok) {
    throw new XiapanMusicError("NETWORK", `音频下载失败（HTTP ${res.status}）`, { url: mediaUrl, status: res.status });
  }
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 1024) {
    throw new XiapanMusicError("NETWORK", `音频下载失败：文件只有 ${buf.length} 字节`, { url: mediaUrl });
  }
  const file = resolve(outFile);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, buf);
  return { file, bytes: buf.length };
}

function makeTimeoutSignal(ms) {
  if (typeof AbortController !== "function") return undefined;
  const c = new AbortController();
  if (ms > 0) {
    const timer = setTimeout(() => c.abort(), ms);
    // 不要因为这个定时器吊住进程事件循环（请求结束后由调用方自然释放）
    if (typeof timer.unref === "function") timer.unref();
  }
  return c.signal;
}

// ---------------------------------------------------------------------------
// 高层编排：写词 → 提交 → 等 → 下载
// ---------------------------------------------------------------------------

/**
 * 默认产物目录：~/Music/虾盘云音乐/（不存在尽量自动建）。
 * 注意：只读沙箱里 mkdir 可能 EPERM，这里不抛错——真正落盘时 downloadClip 会再建目录并给出清晰错误。
 * @returns {string}
 */
export function defaultSongOutDir() {
  const dir = join(homedir(), "Music", "虾盘云音乐");
  try {
    mkdirSync(dir, { recursive: true });
  } catch {
    // 目录不可写时保持路径返回；写盘阶段会暴露具体错误（出卡阶段绝不因目录问题失败）
  }
  return dir;
}

/**
 * 一句话出歌（有歌词直接用；没有就用 theme 写歌词）。
 * 硬规则：绝不去把「一句风格描述」直接提交——没有完整歌词时一律先 writeLyrics。
 * 注意：付费提交只发生一次；本函数不重试 submit。
 * @param {{theme?:string, prompt?:string, lyrics?:string, title?:string, tags?:string, style?:string,
 *          language?:string, mv?:string, outDir?:string, source?:string, onProgress?:Function}} input
 * @param {string} [key]
 * @param {object} [opts]
 * @returns {Promise<{ok:true, songs:Array<object>, elapsedMs:number, provider:object, costHint:string, nextSteps:object}>}
 */
export async function generateSong(input = {}, key, opts = {}) {
  const startedAt = Date.now();
  const k = resolveKey({ key, env: opts.env, deviceFile: opts.deviceFile });

  let lyrics = String(input.lyrics || "").trim();
  let title = String(input.title || "").trim();
  let tags = String(input.tags || input.style || "").trim();

  if (lyrics && !isUsableLyrics(lyrics)) {
    throw new XiapanMusicError(
      "BAD_REQUEST",
      "传入的 lyrics 不像完整歌词（需带 [Verse]/[Chorus] 等结构标签、≥8 行、120-5000 字）。一句风格描述不能直接出整歌——请只传 theme，让本函数先写词。",
      { lyricsChars: lyrics.length },
    );
  }

  if (!lyrics) {
    const written = await writeLyrics(
      {
        theme: input.theme || input.prompt || "",
        style: input.style || input.tags || "",
        language: input.language || "zh",
        title,
      },
      k,
      opts,
    );
    lyrics = written.lyrics;
    title = title || written.title;
    tags = tags || written.tags;
  }
  if (!tags) tags = DEFAULT_TAGS;

  const submitted = await submitSong({ prompt: lyrics, title, tags, mv: input.mv, instrumental: false }, k, { ...opts, requireLyrics: true });
  const waited = await waitSong(submitted.taskId, {
    ...opts,
    key: k,
    intervalMs: opts.intervalMs,
    timeoutMs: opts.timeoutMs,
    onProgress: input.onProgress,
  });

  const outDir = input.outDir || defaultSongOutDir();
  const stamp = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14);
  const songs = [];
  for (let i = 0; i < waited.clips.length; i += 1) {
    const clip = waited.clips[i];
    const file = join(outDir, `${sanitizeFileName(clip.title || title, "song")}-${stamp}-${i + 1}.mp3`);
    const saved = await downloadClip(clip.audioUrl, file, opts);
    songs.push({
      file: saved.file,
      bytes: saved.bytes,
      title: clip.title || title,
      lyrics: i === 0 ? lyrics : undefined,
      duration: clip.duration,
      clipId: clip.clipId,
      imageUrl: clip.imageUrl,
      audioUrl: clip.audioUrl,
      model: clip.model,
      mv: clip.mv,
    });
  }

  return {
    ok: true,
    songs,
    elapsedMs: Date.now() - startedAt,
    provider: { taskId: waited.taskId, model: songs[0] && songs[0].model, mv: submitted.mv },
    costHint: COST_HINT.song,
    nextSteps: buildNextSteps({ source: input.source, key: k }),
  };
}

// ---------------------------------------------------------------------------
// 纯音乐 / BGM（MiniMax via pay-server，同步单曲）
// ---------------------------------------------------------------------------

/**
 * 生成纯音乐/BGM，落盘成 mp3。
 * @param {{prompt:string, model?:string, outFile?:string, idempotencyKey?:string, onProgress?:Function}} input
 * @returns {Promise<{ok:true, file:string, bytes:number, taskId:string, model:string, elapsedMs:number, costHint:string, nextSteps:object}>}
 */
export async function generateBgm(input = {}, key, opts = {}) {
  const startedAt = Date.now();
  const k = resolveKey({ key, env: opts.env, deviceFile: opts.deviceFile });
  const prompt = String(input.prompt || "").trim();
  if (!prompt) throw new XiapanMusicError("BAD_REQUEST", "缺少 prompt（BGM 风格/场景描述）");
  const model = String(input.model || DEFAULT_BGM_MODEL).trim();
  const idempotencyKey = String(input.idempotencyKey || `xiapan-bgm-${startedAt}-${Math.random().toString(16).slice(2, 10)}`);

  const submitted = await requestJson("POST", "/v1/music/generations", {
    ...opts,
    key: k,
    body: { model, prompt, idempotency_key: idempotencyKey },
    timeoutMs: opts.submitTimeoutMs || 200_000,
  });
  const subBody = submitted.json || {};
  const taskId = String(subBody.id || subBody.task_id || subBody.taskId || (subBody.data && (subBody.data.id || subBody.data.task_id)) || "");
  if (!taskId) {
    throw new XiapanMusicError("BAD_REQUEST", "BGM 提交未返回任务 id", { body: subBody });
  }

  const intervalMs = Math.max(opts.minIntervalMs || 1_000, opts.intervalMs || 5_000);
  const timeoutMs = opts.timeoutMs || 600_000;
  const maxNetworkRetries = opts.maxNetworkRetries == null ? 5 : opts.maxNetworkRetries;
  let lastStatus = "";
  let networkFailures = 0;
  while (Date.now() - startedAt < timeoutMs) {
    await sleep(intervalMs);
    let polled;
    try {
      polled = await requestJson("GET", `/v1/music/generations/${encodeURIComponent(taskId)}`, {
        ...opts,
        key: k,
        timeoutMs: opts.pollTimeoutMs || 30_000,
      });
      networkFailures = 0;
    } catch (err) {
      if (err instanceof XiapanMusicError && (err.code === "NETWORK" || err.code === "TIMEOUT") && networkFailures < maxNetworkRetries) {
        networkFailures += 1;
        continue;
      }
      throw err;
    }
    const body = polled.json || {};
    const inner = body.data || {};
    lastStatus = String(body.status || inner.status || "").toUpperCase();
    if (typeof input.onProgress === "function") {
      input.onProgress({ status: lastStatus, elapsedMs: Date.now() - startedAt });
    }
    if (/COMPLET|SUCCESS|SUCCEED/.test(lastStatus)) break;
    if (/FAIL|ERROR|CANCEL/.test(lastStatus)) {
      throw new XiapanMusicError("TASK_FAILED", `BGM 生成失败：${body.error?.message || lastStatus}`, { taskId, status: lastStatus });
    }
  }
  if (!/COMPLET|SUCCESS|SUCCEED/.test(lastStatus)) {
    throw new XiapanMusicError("TIMEOUT", `等待 BGM 超过 ${Math.round(timeoutMs / 1000)}s 仍未完成（最后状态 ${lastStatus || "未知"}）`, {
      taskId,
      lastStatus,
    });
  }

  const contentRes = await (opts.fetchImpl || globalThis.fetch)(`${opts.baseUrl || API_BASE}/v1/music/generations/${encodeURIComponent(taskId)}/content`, {
    headers: { Authorization: `Bearer ${k}` },
    signal: makeTimeoutSignal(opts.downloadTimeoutMs || 300_000),
  });
  if (!contentRes.ok) {
    throw new XiapanMusicError("NETWORK", `BGM 下载失败（HTTP ${contentRes.status}）`, { taskId, status: contentRes.status });
  }
  const buf = Buffer.from(await contentRes.arrayBuffer());
  if (buf.length < 1024) {
    throw new XiapanMusicError("NETWORK", `BGM 下载失败：只有 ${buf.length} 字节`, { taskId });
  }
  const file = resolve(input.outFile || join(defaultSongOutDir(), `xiapan-bgm-${Date.now()}.mp3`));
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, buf);

  return {
    ok: true,
    file,
    bytes: buf.length,
    taskId,
    model,
    elapsedMs: Date.now() - startedAt,
    costHint: COST_HINT.bgm,
    nextSteps: buildNextSteps({ source: input.source, key: k }),
  };
}

// ---------------------------------------------------------------------------
// 导流 CTA
// ---------------------------------------------------------------------------

/**
 * 生成带 UTM 的下一步链接。
 *
 * 归因优先级：显式入参 > 环境变量 > 默认值
 *   source: {source} > env.XIAPAN_UTM_SOURCE > "cli"
 *   medium: {medium} > env.XIAPAN_UTM_MEDIUM > "skill"（DSH 插件注入 XIAPAN_UTM_MEDIUM=plugin）
 * source/medium 只允许 [a-z0-9_-]，防止有人把 Key 之类的东西透传进 URL。
 * 链接默认**不带** Key（防止 Key 进入日志/文件）；充值直达链接见 rechargeUrlWithKey()。
 * @param {{source?:string, medium?:string, env?:object, key?:string}} [opts]
 */
export function buildNextSteps({ source, medium, env = process.env } = {}) {
  const e = env || {};
  const src = sanitizeUtm(source || e.XIAPAN_UTM_SOURCE, "cli");
  const med = sanitizeUtm(medium || e.XIAPAN_UTM_MEDIUM, "skill");
  const withUtm = (url) => {
    const u = new URL(url);
    u.searchParams.set("utm_source", src);
    u.searchParams.set("utm_medium", med);
    u.searchParams.set("utm_campaign", CTA.campaign);
    return u.toString();
  };
  return {
    board: withUtm(CTA.board),
    registerKey: withUtm(CTA.registerKey),
    recharge: withUtm(CTA.recharge),
    utm: { source: src, medium: med, campaign: CTA.campaign },
    tip: "去画板做 MV / 继续创作：https://tu.u-claw.org.cn；没有 Key 去 https://api.u-claw.org.cn 领；充值 https://api.u-claw.org.cn/recharge",
  };
}

/** UTM 参数清洗：只留安全字符，避免 Key/任意串被拼进 URL */
function sanitizeUtm(value, fallback) {
  const s = String(value || "").trim().toLowerCase();
  const cleaned = s.replace(/[^a-z0-9_-]/g, "").slice(0, 40);
  return cleaned || fallback;
}

/**
 * 面向用户本人的「充值直达」链接（带 ?key=）。只在终端给人看时拼，
 * 不要写进 JSON / 文件 / 日志（红线：完整 Key 不落盘不入日志）。
 * @param {string} key
 * @param {string} [source]
 * @param {{medium?:string, env?:object}} [opts]
 */
export function rechargeUrlWithKey(key, source, opts = {}) {
  if (!key) return buildNextSteps({ source, medium: opts.medium, env: opts.env }).recharge;
  const links = buildNextSteps({ source, medium: opts.medium, env: opts.env });
  const u = new URL(links.recharge);
  u.searchParams.set("key", String(key).trim());
  return u.toString();
}

/** 文件大小（便于 CLI 输出） */
export function fileSize(file) {
  try {
    return statSync(file).size;
  } catch {
    return 0;
  }
}
