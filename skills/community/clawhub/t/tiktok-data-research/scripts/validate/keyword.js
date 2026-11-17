/**
 * 关键词与枚举校验。非法值直接失败，不改写成默认值。
 * 长度按 Unicode 码点计算，与后端按字符计数一致。
 */

function codePointLength(value) {
  return Array.from(value).length;
}

/**
 * 去掉控制字符和零宽字符，连续空白收敛为一个空格。
 * 保留 emoji，TikTok 搜索会用到。
 * @param {string} keyword
 * @returns {string}
 */
function normalizeKeyword(keyword) {
  if (typeof keyword !== "string") return "";
  return keyword
    .replace(/[\u0000-\u001f\u007f\u200b-\u200f\ufeff]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

/**
 * @param {string} keyword
 * @returns {string} 空字符串表示合法，否则是给人和 agent 看的原因
 */
function keywordError(keyword) {
  if (typeof keyword !== "string" || keyword.trim() === "") {
    return "关键词不能为空";
  }
  const length = codePointLength(keyword);
  if (length < 1 || length > 100) {
    return "关键词长度需为 1-100 个字符";
  }
  if (/[<>"']/.test(keyword)) {
    return "关键词不能包含 < > \" '";
  }
  if (
    /https?:\/\//i.test(keyword) ||
    /tiktok\.com/i.test(keyword) ||
    /www\./i.test(keyword)
  ) {
    return "关键词不能是链接。博主主页请用 post-cli，视频评论请用 comment-cli";
  }
  return "";
}

function assertChoice(value, allowed, label) {
  const n = Number(value);
  if (!allowed.includes(n)) {
    throw new Error(`${label} ${value} 无效, 允许值: ${allowed.join(", ")}`);
  }
  return n;
}

function assertIntegerRange(value, min, max, label) {
  const n = Number(value);
  if (!Number.isInteger(n) || n < min || n > max) {
    throw new Error(`${label} ${value} 无效, 允许 ${min}-${max} 的整数`);
  }
  return n;
}

/**
 * @returns {[number, number, number]}
 */
function assertSearchOptions(sort, time, limit) {
  sort = assertChoice(sort, [0, 1], "排序 sort");
  time = assertChoice(time, [0, 1, 7, 30, 90, 180], "发布时间 time");
  limit = assertIntegerRange(limit, 1, 10000, "搜索数量 limit");
  return [sort, time, limit];
}

module.exports = {
  normalizeKeyword,
  keywordError,
  assertSearchOptions,
  assertChoice,
  assertIntegerRange,
};
