const fs = require("fs");
const path = require("path");

function isUrl(url) {
  try {
    const parsedUrl = new URL(url);
    return parsedUrl.protocol === "http:" || parsedUrl.protocol === "https:";
  } catch (_) {
    return false;
  }
}

function isFilePath(path) {
  try {
    const stats = fs.statSync(path);
    return stats.isFile();
  } catch (_) {
    return false;
  }
}

/**
 * 预签名只提交文件名。扩展名大小写统一成 .mp4，不改本地原文件。
 * @param {string} filePath
 * @returns {string}
 */
function presignFileName(filePath) {
  const base = path.basename(filePath);
  const ext = path.extname(base);
  if (ext.toLowerCase() !== ".mp4") {
    const shown = ext || "无扩展名";
    throw new Error(`当前仅支持 mp4，收到 ${shown}`);
  }
  if (ext === ".mp4") return base;
  return base.slice(0, -ext.length) + ".mp4";
}

/**
 * 直链下载结果没有扩展名时补 .mp4。已有其它扩展名则留给 presignFileName 拒绝。
 * @param {string} filePath
 * @returns {string}
 */
function ensureDownloadExtension(filePath) {
  if (path.extname(filePath) !== "") return filePath;
  let next = `${filePath}.mp4`;
  let n = 1;
  while (fs.existsSync(next)) {
    next = `${filePath}(${n++}).mp4`;
  }
  fs.renameSync(filePath, next);
  return next;
}

/**
 * 下载库给出的文件名可能含 Windows 非法字符、保留设备名，或百分号编码。
 * 在落盘前净化，不改下载库本身。
 * @param {string} fileName
 * @returns {string}
 */
function safeDownloadName(fileName) {
  let name = String(fileName || "");
  try {
    name = decodeURIComponent(name);
  } catch (_) {}
  name = name.replace(/[<>:"|?*\\/\u0000-\u001f]/g, "_").replace(/[. ]+$/g, "").trim();
  const ext = path.extname(name);
  const stem = ext ? name.slice(0, -ext.length) : name;
  if (!stem || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])$/i.test(stem)) {
    return `download_${Date.now()}.mp4`;
  }
  return name;
}

module.exports = {
  isFilePath,
  isUrl,
  presignFileName,
  ensureDownloadExtension,
  safeDownloadName,
};
