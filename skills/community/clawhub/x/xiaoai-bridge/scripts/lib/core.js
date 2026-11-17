/**
 * xiaoai-bridge 核心逻辑。
 *
 * 这里放可离线测试的纯函数与少量配置解析，CLI/网络逻辑在 xiaoai-listen.js。
 *
 * 安全背景：
 * @mi-gpt/miot 会把包含 passToken / serviceToken 的会话缓存写到
 * `process.cwd()` 下的 `.mi.json`，因此 CLI 必须在登录前把 cwd 切到一个
 * 经过校验的私有目录（目录/文件校验逻辑见 lib/state.js）。
 */

import { ConfigError } from "./errors.js";
import { resolveStateDir } from "./state.js";

export { ConfigError };

export const VERSION = "1.3.13";

export const DEFAULT_POLL_INTERVAL_MS = 1000;
export const MIN_POLL_INTERVAL_MS = 500;
export const MAX_POLL_INTERVAL_MS = 60000;
export const DEFAULT_TRIGGER_PREFIX = "请";
export const MAX_TTS_TEXT_LENGTH = 1000;

export const DEFAULT_JEV_BASE_URL = "https://tokenrhythm.studio";
export const DEFAULT_JEV_MODEL = "NeoHorse-Jev-4B";
export const DEFAULT_JEV_LEVEL = "balanced";
export const JEV_LEVELS = new Set(["loose", "balanced", "strict"]);
export const DEFAULT_JEV_TIMEOUT_MS = 8000;
export const MIN_JEV_TIMEOUT_MS = 1000;
export const MAX_JEV_TIMEOUT_MS = 30000;

const TRUE_VALUES = new Set(["1", "true", "yes", "on"]);

function isTrue(value) {
  return TRUE_VALUES.has(String(value ?? "").trim().toLowerCase());
}

function parsePollInterval(raw) {
  const value = Number.parseInt(String(raw ?? "").trim(), 10);
  if (!Number.isFinite(value)) {
    return DEFAULT_POLL_INTERVAL_MS;
  }
  return Math.min(MAX_POLL_INTERVAL_MS, Math.max(MIN_POLL_INTERVAL_MS, value));
}

function parseJevTimeoutMs(raw) {
  const value = Number.parseInt(String(raw ?? "").trim(), 10);
  if (!Number.isFinite(value)) {
    return DEFAULT_JEV_TIMEOUT_MS;
  }
  return Math.min(MAX_JEV_TIMEOUT_MS, Math.max(MIN_JEV_TIMEOUT_MS, value));
}

/**
 * 解析 Jev 判定服务配置。未配置 JEV_API_KEY 时返回 null（回退热词触发）。
 *
 * Jev 是热词触发的上位替代：配置后由判定模型决定每条语音是否转发。
 *
 * @param {Record<string, string | undefined>} env
 * @returns {null | { apiKey: string, baseUrl: string, model: string, level: "loose" | "balanced" | "strict", decisionThreshold?: number, timeoutMs: number }}
 */
export function parseJevConfig(env = process.env) {
  const apiKey = String(env.JEV_API_KEY ?? "").trim();
  if (!apiKey) {
    return null;
  }
  if (!/^sk_[A-Za-z0-9._-]+$/.test(apiKey)) {
    throw new ConfigError("JEV_API_KEY 格式不正确：应以 sk_ 开头的平台密钥（见 tokenrhythm.studio）");
  }

  const rawBaseUrl = String(env.JEV_BASE_URL ?? "").trim();
  const baseUrl = rawBaseUrl || DEFAULT_JEV_BASE_URL;
  let parsedUrl;
  try {
    parsedUrl = new URL(baseUrl);
  } catch {
    throw new ConfigError(`JEV_BASE_URL 不是合法 URL：${rawBaseUrl}`);
  }
  if (parsedUrl.protocol !== "https:") {
    throw new ConfigError("JEV_BASE_URL 必须使用 https（判定请求携带 API Key）");
  }
  if (parsedUrl.username || parsedUrl.password) {
    throw new ConfigError("JEV_BASE_URL 不允许携带用户名或密码");
  }

  const model = String(env.JEV_MODEL ?? "").trim() || DEFAULT_JEV_MODEL;
  if (!/^[A-Za-z0-9._-]{1,64}$/.test(model)) {
    throw new ConfigError("JEV_MODEL 只允许字母、数字、点、下划线和连字符（1-64 位）");
  }

  const rawLevel = String(env.JEV_LEVEL ?? "").trim().toLowerCase();
  const level = rawLevel || DEFAULT_JEV_LEVEL;
  if (!JEV_LEVELS.has(level)) {
    throw new ConfigError(`JEV_LEVEL 仅支持 loose / balanced / strict，当前为「${rawLevel}」`);
  }

  let decisionThreshold;
  const rawThreshold = String(env.JEV_DECISION_THRESHOLD ?? "").trim();
  if (rawThreshold) {
    const value = Number(rawThreshold);
    if (!Number.isFinite(value) || value < 0 || value > 1) {
      throw new ConfigError("JEV_DECISION_THRESHOLD 必须是 0-1 之间的数字");
    }
    decisionThreshold = value;
  }

  return {
    apiKey,
    // 去掉尾部斜杠，避免拼出 https://host//v1/decision。
    baseUrl: baseUrl.replace(/\/+$/, ""),
    model,
    level,
    decisionThreshold,
    timeoutMs: parseJevTimeoutMs(env.JEV_TIMEOUT_MS),
  };
}

/**
 * 解析触发词前缀（judge 子命令无需完整 MI 配置时复用）。
 *
 * @param {Record<string, string | undefined>} [env]
 */
export function parseTriggerPrefix(env = process.env) {
  const rawPrefix = env.TRIGGER_PREFIX;
  return rawPrefix === undefined ? DEFAULT_TRIGGER_PREFIX : String(rawPrefix).trim();
}

/**
 * 解析并校验环境变量。配置问题一律抛 ConfigError。
 *
 * 注意：这里不创建目录、不切工作目录，副作用留给 prepareSessionState。
 *
 * @param {Record<string, string | undefined>} [env]
 */
export function parseConfig(env = process.env) {
  const userId = String(env.MI_USER_ID ?? "").trim();
  if (!/^\d+$/.test(userId)) {
    throw new ConfigError(
      "MI_USER_ID 缺失或不是纯数字小米 ID（注意：不是手机号或邮箱，见小米账号「个人信息 - 小米 ID」）",
    );
  }

  const did = String(env.MI_DEVICE_ID ?? "").trim();
  if (!did) {
    throw new ConfigError("MI_DEVICE_ID 缺失（可填设备名称、miotDID 或 MAC，DEBUG=true 可查看设备列表）");
  }

  const passToken = String(env.MI_PASS_TOKEN ?? "").trim();
  const password = String(env.MI_PASSWORD ?? "").trim();
  if (!passToken && !password) {
    throw new ConfigError("缺少 MI_PASS_TOKEN 或 MI_PASSWORD（推荐 passToken，密码登录可能触发安全验证）");
  }

  const triggerPrefix = parseTriggerPrefix(env);
  const allowUnfiltered = isTrue(env.XIAOAI_ALLOW_UNFILTERED);
  if (!triggerPrefix && !allowUnfiltered) {
    throw new ConfigError(
      "TRIGGER_PREFIX 为空会处理所有语音消息。如确需如此，请显式设置 XIAOAI_ALLOW_UNFILTERED=true",
    );
  }

  const stateDirInfo = resolveStateDir(env);

  return {
    userId,
    did,
    passToken,
    password,
    debug: isTrue(env.DEBUG),
    triggerPrefix,
    allowUnfiltered,
    pollIntervalMs: parsePollInterval(env.POLL_INTERVAL),
    jev: parseJevConfig(env),
    stateDir: stateDirInfo.dir,
    stateDirSource: stateDirInfo.source,
    allowInsecureStateDir: isTrue(env.XIAOAI_ALLOW_INSECURE_STATE_DIR),
  };
}

/**
 * 从对话记录中提取需要处理的语音指令。
 *
 * 关键点：
 * - 小米接口返回的记录按时间「新 -> 旧」排列，且包含游标消息本身；
 * - 必须先把所有 time > since 的记录收集起来，最后统一推进 lastTimestamp，
 *   否则会漏掉同一轮里的多条新消息；
 * - 输出按时间「旧 -> 新」排序，便于消费方顺序处理。
 *
 * @param {Array<{ time?: number, query?: string }>} records
 * @param {{ prefix?: string, since?: number, allowUnfiltered?: boolean }} [options]
 * @returns {{ messages: Array<{ type: "message", text: string, originalText: string, timestamp: number }>, lastTimestamp: number }}
 */
export function extractCommands(records, options = {}) {
  const prefix = options.prefix === undefined ? DEFAULT_TRIGGER_PREFIX : String(options.prefix);
  const allowUnfiltered = options.allowUnfiltered === true;
  const since = Number.isFinite(options.since) ? Number(options.since) : 0;

  if (!prefix && !allowUnfiltered) {
    throw new ConfigError(
      "TRIGGER_PREFIX 为空会处理所有语音消息。如确需如此，请显式设置 XIAOAI_ALLOW_UNFILTERED=true",
    );
  }

  const messages = [];
  let lastTimestamp = since;

  for (const record of Array.isArray(records) ? records : []) {
    const timestamp = Number(record?.time);
    if (!Number.isFinite(timestamp)) {
      continue;
    }

    if (timestamp > lastTimestamp) {
      lastTimestamp = timestamp;
    }
    if (timestamp <= since) {
      continue;
    }

    const query = typeof record?.query === "string" ? record.query : "";
    if (!query) {
      continue;
    }
    if (prefix && !query.startsWith(prefix)) {
      continue;
    }

    const text = (prefix ? query.slice(prefix.length) : query).trim();
    if (!text) {
      continue;
    }

    messages.push({
      type: "message",
      text,
      originalText: query,
      timestamp,
    });
  }

  messages.sort((a, b) => a.timestamp - b.timestamp);
  return { messages, lastTimestamp };
}

/**
 * 从对话记录中提取全部新语音转写（不做触发词过滤）。
 *
 * 与 extractCommands 共享同一套时间戳游标语义，供 Jev 判定模式使用：
 * 先由判定模型决定转发与否，前缀命中只作为传给判定服务的信号。
 *
 * @param {Array<{ time?: number, query?: string }>} records
 * @param {{ since?: number, prefix?: string }} [options]
 * @returns {{ messages: Array<{ text: string, originalText: string, timestamp: number, prefixMatched: boolean }>, lastTimestamp: number }}
 */
export function extractTranscripts(records, options = {}) {
  const prefix = options.prefix === undefined ? DEFAULT_TRIGGER_PREFIX : String(options.prefix);
  const since = Number.isFinite(options.since) ? Number(options.since) : 0;

  const messages = [];
  let lastTimestamp = since;

  for (const record of Array.isArray(records) ? records : []) {
    const timestamp = Number(record?.time);
    if (!Number.isFinite(timestamp)) {
      continue;
    }

    if (timestamp > lastTimestamp) {
      lastTimestamp = timestamp;
    }
    if (timestamp <= since) {
      continue;
    }

    const query = typeof record?.query === "string" ? record.query : "";
    if (!query) {
      continue;
    }

    const prefixMatched = Boolean(prefix) && query.startsWith(prefix);
    // 前缀命中的消息沿用旧契约：text 去掉前缀；仅“请”这类孤前缀仍然丢弃。
    const text = (prefixMatched ? query.slice(prefix.length) : query).trim();
    if (!text) {
      continue;
    }

    messages.push({ text, originalText: query, timestamp, prefixMatched });
  }

  messages.sort((a, b) => a.timestamp - b.timestamp);
  return { messages, lastTimestamp };
}

/**
 * 轮询一次并返回全部新语音转写（Jev 判定模式）。
 *
 * @param {{ getConversations: (options: { limit: number, timestamp: number }) => Promise<{ records?: Array<{ time?: number, query?: string }> } | undefined> }} client
 * @param {{ lastTimestamp: number, triggerPrefix: string }} state
 */
export async function pollTranscripts(client, state) {
  const conversations = await client.getConversations({
    limit: 10,
    timestamp: state.lastTimestamp,
  });

  const { messages, lastTimestamp } = extractTranscripts(conversations?.records, {
    since: state.lastTimestamp,
    prefix: state.triggerPrefix,
  });

  state.lastTimestamp = lastTimestamp;
  return messages;
}

/**
 * 轮询一次并把结果转换为消息列表。
 *
 * @param {{ getConversations: (options: { limit: number, timestamp: number }) => Promise<{ records?: Array<{ time?: number, query?: string }> } | undefined> }} client
 * @param {{ lastTimestamp: number, triggerPrefix: string, allowUnfiltered?: boolean }} state
 */
export async function pollOnce(client, state) {
  const conversations = await client.getConversations({
    limit: 10,
    timestamp: state.lastTimestamp,
  });

  const { messages, lastTimestamp } = extractCommands(conversations?.records, {
    prefix: state.triggerPrefix,
    since: state.lastTimestamp,
    allowUnfiltered: state.allowUnfiltered === true,
  });

  state.lastTimestamp = lastTimestamp;
  return messages;
}

/**
 * 在回调执行期间把 console.log 重定向到 stderr。
 *
 * @mi-gpt/miot 在 DEBUG 模式会用 console.log 打印设备列表，直接混进监听模式的
 * stdout 会破坏「stdout 只有 JSON」的契约，因此在监听/播报模式初始化时启用。
 *
 * @template T
 * @param {() => Promise<T>} fn
 * @returns {Promise<T>}
 */
export async function withLogsToStderr(fn) {
  const originalLog = console.log;
  console.log = (...args) => console.error(...args);
  try {
    return await fn();
  } finally {
    console.log = originalLog;
  }
}
