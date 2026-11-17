const utils = require("../utils/utils");

/**
 * 规范TikTok视频URL
 * @param {string} url - 输入的URL
 * @returns {string} 规范后的URL
 */
function tiktokPostUrl(url) {
  url = url.trim();
  if (url.includes("https://www.tiktok.com/@")) {
    url = url.substring(url.indexOf("https://www.tiktok.com/@"));
  } else {
    url = url.replace(/[^a-zA-Z0-9_ -]/g, "");
  }

  if (url.includes(" ")) {
    url = url.substring(0, url.indexOf(" "));
  }
  return url;
}

function optionFormat(limit) {
  limit = Number.isFinite(limit) ? limit : 10;
  if (limit < 1 || limit > 10000) {
    utils.printError(
      `获取的评论数量 ${limit} 无效, 请使用 1-10000。已回退为 10`,
    );
    limit = 10;
  }
  return limit;
}

module.exports = {
  tiktokPostUrl,
  optionFormat,
};
