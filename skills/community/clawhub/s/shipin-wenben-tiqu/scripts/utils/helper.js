const { Downloader } = require("../utils/download.js");
const constants = require("../config/constants");
const { safeDownloadName } = require("./validator");
const fs = require("fs");

function inlineLog(msg) {
  try {
    if (process.stderr.isTTY) {
      process.stderr.clearLine(0);
      process.stderr.cursorTo(0);
      process.stderr.write(msg + "\r");
      return;
    }
  } catch (_) {}
  process.stderr.write(msg + "\n");
}

function byteHumanize(byte) {
  if (byte === 0) {
    return "0 b";
  }
  const units = ["b", "kB", "MB", "GB", "TB"];
  const number = Math.floor(Math.log(byte) / Math.log(1024));
  return (byte / Math.pow(1024, number)).toFixed(1) + " " + units[number];
}

/**
 * 下载文件
 */
async function download(url, path) {
  return new Promise((resolve, reject) => {
    const options = {
      retry: {
        maxRetries: constants.CREATE_MAX_ATTEMPTS,
        delay: constants.RETRY_INTERVAL,
      },
      override: false,
      fileName: (name) => safeDownloadName(name),
    };

    let progressLog = "";
    const dl = new Downloader(url, path, options);

    dl.on("end", (info) => {
      const filePath = info && info.filePath ? info.filePath : "";
      if (info && info.incomplete) {
        if (filePath) {
          try {
            fs.unlinkSync(filePath);
          } catch (_) {}
        }
        reject(new Error("下载未完成，文件不完整"));
        return;
      }
      if (!filePath) {
        reject(new Error("下载失败: 未返回文件路径"));
        return;
      }
      inlineLog((progressLog ? progressLog + " - " : "") + "下载完成");
      resolve(info);
    })
      .on("skip", () => {
        reject(new Error("目标位置已有同名文件，已取消下载，以免误用旧文件"));
      })
      .on("retry", (attempt, opts) => {
        let count = Math.floor(opts.delay / 1000);
        const retryLog = () => {
          inlineLog(`重试${attempt}/${opts.maxRetries}次，等待${count}秒`);
          if (count > 0) {
            setTimeout(() => retryLog(), 1000);
          }
          count--;
        };
        retryLog();
      })
      .on("resume", (isResumed) => {
        if (!isResumed) {
          inlineLog("该链接不支持断点续传，文件将从头重新开始加载。");
        }
      })
      .on("progress.throttled", (stats) => {
        const progress = stats.progress.toFixed(1);
        const speed = byteHumanize(stats.speed);
        const downloaded = byteHumanize(stats.downloaded);
        const total = byteHumanize(stats.total);
        progressLog = `${stats.name}: ${speed}/s - ${progress}% [${downloaded}/${total}]`;
        inlineLog(progressLog);
      })
      .on("error", (error) => {
        inlineLog("下载失败:" + error.message);
        reject(error);
      });

    dl.start().catch((err) => {
      inlineLog("下载失败:" + err.message);
      reject(err);
    });
  });
}

module.exports = {
  byteHumanize,
  download,
  inlineLog,
};
