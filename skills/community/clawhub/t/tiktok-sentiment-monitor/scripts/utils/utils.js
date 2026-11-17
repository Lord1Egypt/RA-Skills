/**
 * 打印横幅信息
 */
function printBanner() {
  process.stderr.write("╔════════════════════════════════════════════╗\n");
  process.stderr.write("║                                            ║\n");
  process.stderr.write("║          🎬 TikTok数据智能分析助手            ║\n");
  process.stderr.write("║                                            ║\n");
  process.stderr.write("╚════════════════════════════════════════════╝\n");
  process.stderr.write("\n");
}

/**
 * 打印带颜色的日志信息
 * @param {string} level - 日志级别 (INFO|SUCCESS|WARN|ERROR)
 * @param {string} message - 日志消息内容
 */
function printLog(level, message) {
  message = String(message ?? "");
  const colorMap = {
    INFO: "\x1b[34m",
    SUCCESS: "\x1b[32m",
    WARN: "\x1b[33m",
    ERROR: "\x1b[31m",
  };
  console.error(
    `${colorMap[level] || ""}[${new Date().toLocaleString()}] [${level}] ${message}\x1b[0m`,
  );
}

module.exports = {
  printBanner,
  printInfo: (msg) => printLog("INFO", msg),
  printSuccess: (msg) => printLog("SUCCESS", msg),
  printError: (msg) => printLog("ERROR", msg),
  printWarn: (msg) => printLog("WARN", msg),
};
