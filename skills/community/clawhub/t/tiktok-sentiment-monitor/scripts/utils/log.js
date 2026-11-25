const fs = require("fs");
const path = require("path");
const os = require("os");
const utils = require("./utils");

function localDateStr() {
  const d = new Date();
  return (
    d.getFullYear() +
    "-" +
    String(d.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(d.getDate()).padStart(2, "0")
  );
}

async function taskWrite(filename, content) {
  if (process.env.TT_GUAIKEI_ENABLE_LOG !== "1") return;
  if (!filename || typeof filename !== "string") {
    utils.printError("日志文件名必须是非空字符串");
    return;
  }
  if (!content || typeof content !== "string") {
    utils.printError("日志内容必须是非空字符串");
    return;
  }
  let safeFilename = `${process.pid}_${filename}`
    .replace(/[\\/:*?"<>|]/g, "_")
    .replace(/\.\.+/g, "_")
    .replace(/^\.+|\.+$/g, "");
  const ext = path.extname(safeFilename);
  const stem = ext ? safeFilename.slice(0, -ext.length) : safeFilename;
  if (safeFilename.length > 200) {
    safeFilename = stem.slice(0, Math.max(1, 200 - ext.length)) + ext;
  }
  if (safeFilename === "") {
    safeFilename = `log_${Date.now()}`;
  }

  const outputDir = path.join(
    os.tmpdir(),
    "tiktok-guaikei",
    "logs",
    localDateStr(),
  );
  const outputFilename = path.join(outputDir, safeFilename);

  try {
    await fs.promises.mkdir(outputDir, { recursive: true, mode: 0o700 });
    await fs.promises.writeFile(outputFilename, content, { mode: 0o600 });
    utils.printSuccess(`  → 已保存到 ${outputFilename}`);
  } catch (error) {
    utils.printError(`日志写入失败: ${error.message}`);
  }
}

module.exports = {
  taskWrite,
};
