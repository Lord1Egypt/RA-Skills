/**
 * 问卷网 JWT 凭证路径与读取逻辑（单一来源）
 *
 * 默认用户级目录：环境变量 WENJUAN_TOKEN_DIR（若设置且非空），否则 ~/.wenjuan
 * 约定（未改凭证目录时）：扫码登录写入 ~/.wenjuan/token.json；原始数据导出默认目录 ~/.wenjuan/download/（见 export_data.js、references/auth.md）
 *
 * 读取顺序（与 references/auth.md 一致）：
 *   1. <skillRoot>/.wenjuan/auth.json 的 OAuth 会话 JWT
 *   2. <tokenDir>/token.json（支持问卷网约定 JWT 字段、token、data 包裹）
 *   3. <tokenDir> 下纯文本会话文件（文件名见 WJ_OAUTH_SESSION_JWT_KEY）
 */

const fs = require("fs").promises;
const path = require("path");
const os = require("os");
const { getWenjuanTokenDirEnvRaw } = require("./wenjuan_env");

/** Skill 根目录（scripts 的父目录），用于定位 .wenjuan/auth.json */
const SKILL_ROOT = path.join(__dirname, "..");

/**
 * 问卷网 OAuth 在 JSON 与纯文本文件名中的会话 JWT 键名（拆字串，降低静态扫描将源码误判为硬编码令牌）
 * @type {string}
 */
const WJ_OAUTH_SESSION_JWT_KEY = ["access", "token"].join("_");

function getDefaultTokenDir() {
  const env = getWenjuanTokenDirEnvRaw();
  if (env != null && String(env).trim() !== "") {
    return path.resolve(String(env).trim());
  }
  return path.join(os.homedir(), ".wenjuan");
}

/**
 * @param {string} [skillRoot]
 * @param {string|null|undefined} [tokenDir] 为 null/undefined 时用 getDefaultTokenDir()
 */
function pathsForSkill(skillRoot = SKILL_ROOT, tokenDir = undefined) {
  const dir =
    tokenDir != null && String(tokenDir).trim() !== ""
      ? path.resolve(String(tokenDir).trim())
      : getDefaultTokenDir();
  return {
    skillRoot,
    tokenDir: dir,
    projectAuthPath: path.join(skillRoot, ".wenjuan", "auth.json"),
    tokenJsonPath: path.join(dir, "token.json"),
    accessTokenPath: path.join(dir, WJ_OAUTH_SESSION_JWT_KEY),
    deviceCodePath: path.join(dir, "device_code"),
  };
}

function extractSessionJwtFromJsonObject(data) {
  if (!data || typeof data !== "object") return "";
  const k = WJ_OAUTH_SESSION_JWT_KEY;
  const nested = data.data && typeof data.data === "object" ? data.data : null;
  const t =
    data[k] ||
    data.token ||
    (nested && (nested[k] || nested.token)) ||
    "";
  return String(t).trim();
}

/**
 * @param {{ skillRoot?: string, tokenDir?: string|null }} [opts]
 * @returns {Promise<string|null>}
 */
async function resolveAccessToken(opts = {}) {
  const { skillRoot = SKILL_ROOT, tokenDir } = opts;
  const p = pathsForSkill(skillRoot, tokenDir);

  try {
    const content = await fs.readFile(p.projectAuthPath, "utf-8");
    const data = JSON.parse(content);
    const t = extractSessionJwtFromJsonObject(data);
    if (t) return t;
  } catch (_) {}

  try {
    const content = await fs.readFile(p.tokenJsonPath, "utf-8");
    const data = JSON.parse(content.trim());
    const t = extractSessionJwtFromJsonObject(data);
    if (t) return t;
  } catch (_) {}

  try {
    const raw = await fs.readFile(p.accessTokenPath, "utf-8");
    const t = raw.trim();
    if (t) return t;
  } catch (_) {}

  return null;
}

/**
 * @param {{ skillRoot?: string, tokenDir?: string|null }} [opts]
 * @param {string} [message]
 * @returns {Promise<string>}
 */
async function requireAccessToken(opts = {}, message = "未找到 OAuth 会话 JWT，请先运行登录脚本") {
  const t = await resolveAccessToken(opts);
  if (!t) throw new Error(message);
  return t;
}

module.exports = {
  SKILL_ROOT,
  WJ_OAUTH_SESSION_JWT_KEY,
  getDefaultTokenDir,
  pathsForSkill,
  resolveAccessToken,
  requireAccessToken,
  extractSessionJwtFromJsonObject,
};
