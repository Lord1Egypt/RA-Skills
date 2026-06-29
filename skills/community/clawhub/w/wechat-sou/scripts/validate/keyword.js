const utils = require("../utils/utils");

/**
 * 检查搜索关键词是否符合要求
 * @param {string} keyword - 搜索关键词
 * @returns {boolean} - 是否有效
 */
function isKeywordValid(keyword) {
  keyword = keyword.trim();
  if (keyword.length < 2) {
    utils.printError(`搜索关键词长度不能小于 2 个字符`);
    return false;
  }
  if (keyword.length > 50) {
    utils.printError(`搜索关键词长度不能超过 50 个字符`);
    return false;
  }
  if (/[<>\"'&]/g.test(keyword)) {
    utils.printError(`搜索关键词包含特殊字符, 请输入普通关键词, 例如: 新媒体`);
    return false;
  }
  if (keyword.includes("http")) {
    utils.printError(
      `搜索关键词包含 http 链接, 请输入普通关键词, 例如: 新媒体`,
    );
    return false;
  }
  return true;
}

/**
 * 清洗搜索关键词，移除非法字符
 * @param {string} keyword - 原始关键词
 * @returns {string} - 清洗后的搜索关键词
 */
function cleanKeyword(keyword) {
  keyword = keyword.trim();
  keyword = keyword.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\s.,!?# ，。！？]/g, "");
  keyword = keyword.replace(/\s+/g, " "); // 合并连续空格
  return keyword;
}

module.exports = {
  isKeywordValid,
  cleanKeyword,
};
