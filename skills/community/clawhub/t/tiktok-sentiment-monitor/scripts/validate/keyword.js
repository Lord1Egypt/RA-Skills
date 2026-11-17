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
  if (keyword.length > 100) {
    utils.printError(`搜索关键词长度不能超过 100 个字符`);
    return false;
  }
  if (/[<>\"'&]/g.test(keyword)) {
    utils.printError(`搜索关键词包含特殊字符, 请输入普通关键词, 例如: AI`);
    return false;
  }
  if (keyword.includes("http")) {
    utils.printError(`搜索关键词包含 http 链接, 请输入普通关键词, 例如: AI`);
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
  keyword = keyword.replace(/\s+/g, " "); // 合并连续空格
  return keyword;
}

/**
 * 格式化并验证搜索选项
 * @param {number} sort - 排序依据 (0:综合, 1:最多点赞)
 * @param {number} time - 时间范围 (0:全部, 1:一天内, 7:七天内, 30:一个月内, 90:三个月内, 180:半年内)
 * @param {number} limit - 搜索数量 (1-10000)
 * @returns {[number, number, number, number]} 格式化后的选项数组
 */
function optionFormat(sort, time, limit) {
  sort = Number.isFinite(sort) ? sort : 0;
  time = Number.isFinite(time) ? time : 0;
  limit = Number.isFinite(limit) ? limit : 10;
  if (![0, 1].includes(sort)) {
    utils.printError(
      `排序依据 ${sort} 无效, 请使用 0(相关度) / 1(最多点赞)。已回退为 0`,
    );
    sort = 0;
  }
  if (![0, 1, 7, 30, 90, 180].includes(time)) {
    utils.printError(
      `发布时间 ${time} 无效, 请使用 0/1/7/30/90/180。已回退为 0`,
    );
    time = 0;
  }
  if (limit < 1 || limit > 10000) {
    utils.printError(`数量 ${limit} 无效, 请使用 1-10000。已回退为 10`);
    limit = 10;
  }
  return [sort, time, limit];
}

module.exports = {
  isKeywordValid,
  cleanKeyword,
  optionFormat,
};
