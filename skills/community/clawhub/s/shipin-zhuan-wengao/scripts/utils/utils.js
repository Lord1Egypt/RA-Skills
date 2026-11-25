const fs = require("fs");
const path = require("path");

function printBanner() {
  process.stderr.write("╔════════════════════════════════════════════╗\n");
  process.stderr.write("║                                            ║\n");
  process.stderr.write("║          🎬 视频文案智能提取助手            ║\n");
  process.stderr.write("║                                            ║\n");
  process.stderr.write("╚════════════════════════════════════════════╝\n");
  process.stderr.write("\n");
}

function printLog(level, message) {
  message = String(message ?? "");
  const useColor = Boolean(process.stderr.isTTY) && !process.env.NO_COLOR;
  const colorMap = {
    INFO: "\x1b[34m",
    SUCCESS: "\x1b[32m",
    WARN: "\x1b[33m",
    ERROR: "\x1b[31m",
  };
  const color = useColor ? colorMap[level] || "" : "";
  const reset = useColor ? "\x1b[0m" : "";
  console.error(
    `${color}[${new Date().toLocaleString()}] [${level}] ${message}${reset}`,
  );
}

/**
 * 定义技能下载/临时目录路径
 */
function downloadPath() {
  return path.join(path.dirname(__filename), "..", "..", "tmp");
}

/**
 * 记录最近一次成功的视频分析任务ID，供 --id last 复用
 */
function lastTaskPath() {
  return path.join(downloadPath(), ".last_task_id");
}

function saveLastTask(id) {
  try {
    fs.mkdirSync(downloadPath(), { recursive: true });
    fs.writeFileSync(lastTaskPath(), String(id), "utf-8");
  } catch (_) {
    /* 非关键路径，忽略失败 */
  }
}

function loadLastTask() {
  try {
    if (fs.existsSync(lastTaskPath())) {
      return fs.readFileSync(lastTaskPath(), "utf-8").trim();
    }
  } catch (_) {
    /* 忽略读取失败 */
  }
  return "";
}

/**
 * 上传已成功、任务 ID 尚未拿到时的续传记录。
 */
function pendingUploadPath() {
  return path.join(downloadPath(), ".pending_upload.json");
}

function savePendingUpload(record) {
  try {
    fs.mkdirSync(downloadPath(), { recursive: true });
    fs.writeFileSync(pendingUploadPath(), JSON.stringify(record), "utf-8");
  } catch (_) {
    /* 续传记录失败时下次重新上传 */
  }
}

function loadPendingUpload() {
  try {
    if (!fs.existsSync(pendingUploadPath())) return null;
    const record = JSON.parse(fs.readFileSync(pendingUploadPath(), "utf-8"));
    if (!record || typeof record.ossUrl !== "string" || !record.ossUrl) {
      return null;
    }
    return record;
  } catch (_) {
    return null;
  }
}

function clearPendingUpload() {
  try {
    if (fs.existsSync(pendingUploadPath())) fs.unlinkSync(pendingUploadPath());
  } catch (_) {
    /* 忽略删除失败 */
  }
}

module.exports = {
  printBanner,
  printInfo: (msg) => printLog("INFO", msg),
  printSuccess: (msg) => printLog("SUCCESS", msg),
  printError: (msg) => printLog("ERROR", msg),
  printWarn: (msg) => printLog("WARN", msg),
  downloadPath,
  saveLastTask,
  loadLastTask,
  savePendingUpload,
  loadPendingUpload,
  clearPendingUpload,
};
