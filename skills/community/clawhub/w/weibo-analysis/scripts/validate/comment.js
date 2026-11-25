const { assertChoice, assertIntegerRange } = require("./keyword");

function parseWeiboUrl(input) {
  const url = String(input ?? "").trim();
  const length = Array.from(url).length;
  if (length < 1 || length > 255) {
    return "";
  }
  if (!/weibo\.com\//i.test(url) && !/weibo\.cn\//i.test(url)) {
    return "";
  }
  return url;
}

function assertCommentOptions(sort, limit) {
  sort = assertChoice(sort, [0, 1], "排序 sort");
  limit = assertIntegerRange(limit, 1, 10000, "评论数量 limit");
  return [sort, limit];
}

module.exports = { parseWeiboUrl, assertCommentOptions };
