const fs = require("fs");

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

module.exports = {
  isFilePath,
  isUrl,
};
