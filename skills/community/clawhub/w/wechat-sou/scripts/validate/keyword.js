const utils = require("../utils/utils");

function isKeywordValid(keyword) {
  keyword = String(keyword ?? "").trim();
  if (keyword.length < 2) {
    utils.printError(`搜索关键词长度不能小于 2 个字符`);
    return false;
  }
  if (keyword.length > 50) {
    utils.printError(`搜索关键词长度不能超过 50 个字符`);
    return false;
  }
  if (/https?:\/\//i.test(keyword) || /www\./i.test(keyword)) {
    utils.printError(`搜索关键词不能是链接, 请输入普通关键词, 例如: 新媒体`);
    return false;
  }
  if (/[<>"'&]/.test(keyword)) {
    utils.printError(
      `搜索关键词包含特殊字符 < > " ' &, 请输入普通关键词, 例如: 新媒体`,
    );
    return false;
  }
  return true;
}

/**
 * 整理关键词的空白：去掉首尾空白，连续空白合并为一个空格。
 * 不再剥离标点/外文，避免改变用户原意。
 * @param {string} keyword
 * @returns {string}
 */
function normalizeKeyword(keyword) {
  keyword = String(keyword ?? "").trim();
  keyword = keyword.replace(/\s+/g, " ");
  return keyword;
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
 * 校验文章搜索选项。显式非法值直接失败，不改写成默认值。
 */
function assertArticleOptions(sort, publishTime, limit) {
  sort = assertChoice(sort, [0, 1, 2], "排序 sort");
  publishTime = assertChoice(
    publishTime,
    [0, 1, 2, 3],
    "发布时间 publishTime",
  );
  limit = assertIntegerRange(limit, 1, 10000, "搜索数量 limit");
  return [sort, publishTime, limit];
}

/**
 * 校验视频搜索选项。显式非法值直接失败，不改写成默认值。
 */
function assertVideoOptions(sort, duration, limit) {
  sort = assertChoice(sort, [0, 1, 2], "排序 sort");
  duration = assertChoice(duration, [0, 1, 2, 3], "视频时长 duration");
  limit = assertIntegerRange(limit, 1, 10000, "搜索数量 limit");
  return [sort, duration, limit];
}

module.exports = {
  isKeywordValid,
  normalizeKeyword,
  assertArticleOptions,
  assertVideoOptions,
};
