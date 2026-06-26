/**
 * 仅此文件直接读取 process.env，供其他脚本引用。
 * 与网络请求、子进程拆分，便于静态安全扫描（如 ClawHub）。
 */

const DEFAULT_WENJUAN_HOST = "https://www.wenjuan.com";

function getTlsPinSha256() {
  return (process.env.WENJUAN_TLS_PIN_SHA256 || "").trim().toLowerCase();
}

function getMinRequestIntervalMs() {
  return Number(process.env.WENJUAN_MIN_REQUEST_INTERVAL_MS || 200);
}

function getWenjuanHost() {
  return String(process.env.WENJUAN_HOST || DEFAULT_WENJUAN_HOST)
    .trim()
    .replace(/\/+$/, "");
}

/** @returns {string|undefined} */
function getWenjuanTokenDirEnvRaw() {
  return process.env.WENJUAN_TOKEN_DIR;
}

function getWenjuanSyncLogFlag() {
  return process.env.WENJUAN_SYNC_LOG === "1";
}

/** @returns {string|undefined} */
function getWenjuanProjectIndexEnv() {
  return process.env.WENJUAN_PROJECT_INDEX;
}

/** @param {string} name */
function getEnvByName(name) {
  return process.env[name];
}

function isWslEnvMarker() {
  return !!(process.env.WSL_DISTRO_NAME || process.env.WSL_INTEROP);
}

function getWenjuanBrowserSpec() {
  return (process.env.WENJUAN_BROWSER || "").trim();
}

function getStandardBrowserSpec() {
  return (process.env.BROWSER || "").trim();
}

module.exports = {
  DEFAULT_WENJUAN_HOST,
  getTlsPinSha256,
  getMinRequestIntervalMs,
  getWenjuanHost,
  getWenjuanTokenDirEnvRaw,
  getWenjuanSyncLogFlag,
  getWenjuanProjectIndexEnv,
  getEnvByName,
  isWslEnvMarker,
  getWenjuanBrowserSpec,
  getStandardBrowserSpec,
};
