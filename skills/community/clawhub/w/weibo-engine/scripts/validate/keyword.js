const utils = require("../utils/utils");

function isKeywordValid(keyword) {
  keyword = String(keyword ?? "").trim();
  const length = Array.from(keyword).length;
  if (length < 1) {
    utils.printError("搜索关键词不能为空");
    return false;
  }
  if (length > 50) {
    utils.printError("搜索关键词长度不能超过 50 个字符");
    return false;
  }
  if (
    /https?:\/\//i.test(keyword) ||
    /weibo\.com/i.test(keyword) ||
    /weibo\.cn/i.test(keyword)
  ) {
    utils.printError("搜索关键词不能是链接, 请输入普通关键词");
    return false;
  }
  if (/[<>"'&]/.test(keyword)) {
    utils.printError("搜索关键词包含特殊字符 < > \" ' &");
    return false;
  }
  return true;
}

function normalizeKeyword(keyword) {
  keyword = String(keyword ?? "").trim();
  return keyword.replace(/\s+/g, " ");
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

module.exports = {
  isKeywordValid,
  normalizeKeyword,
  assertChoice,
  assertIntegerRange,
};
