/**
 * 日志脱敏。
 *
 * 背景：上游 `@mi-gpt/miot` 在请求失败时会 `console.error("... failed", res)`，
 * 而 `res` 是 axios 错误包装对象，其中 `request.headers` 含
 * `Cookie: userId=...; passToken=...; serviceToken=...`，登录/轮询失败时会把
 * 小米账号凭据打印到 stderr（ClawHub 1.2.0 扫描发现）。
 *
 * 这里在 CLI 入口安装 console 包装，对所有日志参数做脱敏，覆盖：
 * - Cookie / Set-Cookie 整行
 * - JSON / 表单里的 passToken、password、serviceToken、ssecurity、nonce 等字段
 * - `MI_PASS_TOKEN=` 之类的环境变量转储
 *
 * 注意：这是“尽力而为”的防护。上游若把凭据拼进任意文本（无键名）仍可能漏出，
 * 因此运行期仍不应把 stderr 长期落盘。
 */

import util from "node:util";

const SECRET_KEYS =
  "passToken|password|serviceToken|yetAnotherServiceToken|ssecurity|psecurity|nonce|MI_PASS_TOKEN|MI_PASSWORD|JEV_API_KEY";

const COOKIE_HEADER =
  /((?:set-)?cookie"?\s*:\s*)("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|[^\n,}]+)/gi;
const KEY_VALUE = new RegExp(`("?(?:${SECRET_KEYS})"?\\s*[:=]\\s*"?)([^",;\\s}]+)`, "gi");
const FORM_PARAM = new RegExp(`((?:${SECRET_KEYS})=)[^&;,\\s]+`, "gi");
const BEARER = /(authorization"?\s*:\s*"?bearer\s+)[^\s",]+/gi;
// Jev 平台密钥（sk_ 开头）：无键名拼接进任意文本时的兜底脱敏。
const JEV_TOKEN = /\bsk_[A-Za-z0-9._-]{8,}/g;

function stringify(value) {
  if (typeof value === "string") {
    return value;
  }
  if (value instanceof Error) {
    return `${value.name}: ${value.message}${value.stack ? `\n${value.stack}` : ""}`;
  }
  try {
    return util.inspect(value, {
      depth: 6,
      breakLength: 120,
      maxArrayLength: 50,
      maxStringLength: 5000,
    });
  } catch {
    return String(value);
  }
}

/**
 * 对任意日志值做脱敏，返回字符串。
 *
 * @param {unknown} value
 * @returns {string}
 */
export function redactSecrets(value) {
  return stringify(value)
    .replace(COOKIE_HEADER, "$1***")
    .replace(KEY_VALUE, "$1***")
    .replace(FORM_PARAM, "$1***")
    .replace(BEARER, "$1***")
    .replace(JEV_TOKEN, "sk_***");
}

const patched = new WeakSet();

/**
 * 包装给定 console 的常用方法，使所有输出经过脱敏。
 *
 * @param {Console} [consoleObject]
 */
export function installRedactedConsole(consoleObject = console) {
  if (!consoleObject || patched.has(consoleObject)) {
    return;
  }
  patched.add(consoleObject);

  for (const method of ["log", "info", "debug", "warn", "error", "trace"]) {
    if (typeof consoleObject[method] !== "function") {
      continue;
    }
    const original = consoleObject[method].bind(consoleObject);
    consoleObject[method] = (...args) => original(...args.map((arg) => redactSecrets(arg)));
  }
}
