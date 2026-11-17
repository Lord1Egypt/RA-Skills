const utils = require("../utils/utils");

/**
 * 规范TikTok博主主页URL
 * @param {string} url - 输入的URL
 * @returns {string} 规范后的URL
 */
function tiktokUserUrl(url) {
  url = url.trim();
  if (url.includes("https://www.tiktok.com/@")) {
    url = url.substring(url.indexOf("https://www.tiktok.com/@"));
  } else {
    url = url.replace(/[^a-zA-Z0-9_. -]/g, "");
  }
  if (url.includes(" ")) {
    url = url.substring(0, url.indexOf(" "));
  }
  return url;
}

function optionFormat(sort, limit) {
  sort = Number.isFinite(sort) ? sort : 0;
  limit = Number.isFinite(limit) ? limit : 10;
  if (![0, 1].includes(sort)) {
    utils.printError(
      `排序依据 ${sort} 无效, 请使用 0(最新) / 1(最热)。已回退为 0`,
    );
    sort = 0;
  }
  if (limit < 1 || limit > 10000) {
    utils.printError(
      `获取的作品数量 ${limit} 无效, 请使用 1-10000。已回退为 10`,
    );
    limit = 10;
  }
  return [sort, limit];
}

module.exports = {
  tiktokUserUrl,
  optionFormat,
};
