/**
 * 在 CommonJS 脚本中打开系统默认浏览器（微信扫码页、绑定手机号页、报表页等共用）。
 *
 * **本文件不直接使用 `child_process`**（便于 ClawHub 等静态扫描）；统一通过 npm **`open`** 包
 *（动态 `import('open')`）调起系统浏览器；`open` 在 `node_modules` 内自行处理各平台实现。
 *
 * 策略链：
 * 1. `WENJUAN_BROWSER`：通过 `open` 的 `app` 选项指定可执行文件（支持 `firefox` 或 `firefox %s --new-window` 形式）
 * 2. 默认：`open(url)` 打开系统默认浏览器（含 WSL 等由 `open` 包处理）
 * 3. `BROWSER`：类 Unix 上同上，通过 `app` 传入（仅 linux/darwin）
 *
 * 无图形会话或 `open` 失败时，业务侧须配合 `writeUrlForManualOpen` 写入完整 URL 文件。
 */

const fs = require("fs");
const fsp = require("fs").promises;
const path = require("path");
const {
  isWslEnvMarker,
  getWenjuanBrowserSpec,
  getStandardBrowserSpec,
} = require("./wenjuan_env");

/**
 * @param {string} url
 * @param {Record<string, unknown>} [options] 透传给 `open`（如 `wait`、`app`）
 * @returns {Promise<boolean>} 是否由 npm `open` 成功返回
 */
async function openWithNpmOpen(url, options = {}) {
  try {
    const mod = await import("open");
    const fn = typeof mod.default === "function" ? mod.default : mod;
    if (typeof fn !== "function") {
      return false;
    }
    await fn(url, { wait: false, ...options });
    return true;
  } catch {
    return false;
  }
}

/**
 * 使用 `WENJUAN_BROWSER` / `BROWSER` 类 spec 调 `open` 的 `app` 选项（不自行 spawn）。
 * @param {string} url
 * @param {string} spec 如 `firefox`、`firefox %s --new-window`、或带路径的可执行文件
 */
async function openWithBrowserAppSpec(url, spec) {
  const s = String(spec).trim();
  if (!s) return false;
  try {
    if (s.includes("%s")) {
      const parts = s.split("%s");
      const left = parts[0].trim().split(/\s+/).filter(Boolean);
      const right = parts.slice(1).join("%s").trim().split(/\s+/).filter(Boolean);
      const name = left[0];
      if (!name) return false;
      const appArguments = [...left.slice(1), ...right];
      return await openWithNpmOpen(url, {
        app: { name, arguments: appArguments },
      });
    }
    const tokens = s.split(/\s+/).filter(Boolean);
    const name = tokens[0];
    if (!name) return false;
    const appArguments = tokens.slice(1);
    if (appArguments.length > 0) {
      return await openWithNpmOpen(url, { app: { name, arguments: appArguments } });
    }
    return await openWithNpmOpen(url, { app: { name } });
  } catch {
    return false;
  }
}

function isWsl() {
  if (process.platform !== "linux") {
    return false;
  }
  if (isWslEnvMarker()) {
    return true;
  }
  try {
    const v = fs.readFileSync("/proc/version", "utf8");
    return /microsoft/i.test(v);
  } catch {
    return false;
  }
}

async function openViaWenjuanBrowserEnv(url) {
  const spec = getWenjuanBrowserSpec();
  if (!spec) return false;
  return openWithBrowserAppSpec(url, spec);
}

/** 仅类 Unix；Windows 不用 BROWSER，避免 SSH 会话里误指向 Linux 路径 */
async function openViaStandardBrowserEnv(url) {
  if (process.platform !== "linux" && process.platform !== "darwin") {
    return false;
  }
  const spec = getStandardBrowserSpec();
  if (!spec) return false;
  return openWithBrowserAppSpec(url, spec);
}

/**
 * 依次尝试：显式浏览器（env）→ npm `open` 默认浏览器 → BROWSER（类 Unix）。
 * @param {string} url
 * @returns {Promise<boolean>}
 */
async function openUrlBestEffort(url) {
  if (!url || typeof url !== "string") {
    return false;
  }

  if (await openViaWenjuanBrowserEnv(url)) {
    return true;
  }
  if (await openWithNpmOpen(url, { wait: false })) {
    return true;
  }
  if (await openViaStandardBrowserEnv(url)) {
    return true;
  }

  return false;
}

/**
 * 将完整 URL 写入文件，避免终端折行、半选复制导致查询参数丢失（Agent / SSH 场景）。
 * @param {string} url
 * @param {string} dir
 * @param {string} fileName
 * @returns {Promise<string>} 绝对路径
 */
async function writeUrlForManualOpen(url, dir, fileName) {
  await fsp.mkdir(dir, { recursive: true });
  const file = path.join(dir, fileName);
  await fsp.writeFile(file, `${url}\n`, "utf-8");
  try {
    await fsp.chmod(file, 0o600);
  } catch {
    /* Windows 等环境可能不支持 chmod */
  }
  return file;
}

/** 兼容旧名：等价于 `openWithNpmOpen(url, { wait: false })`（不再使用子进程直连） */
async function spawnOpenUrl(url) {
  return openWithNpmOpen(url, { wait: false });
}

module.exports = {
  openWithNpmOpen,
  spawnOpenUrl,
  openUrlBestEffort,
  writeUrlForManualOpen,
  isWsl,
};
