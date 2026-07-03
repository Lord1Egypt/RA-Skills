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

function optionFormat(sort, duration, publish_time, limit) {
  sort = sort || 0;
  duration = duration || 0;
  publish_time = publish_time || 0;
  limit = limit || 10;
  if (sort !== 0 && sort !== 1 && sort !== 2) {
    utils.printError(
      `排序依据 ${sort} 无效, 请使用 0, 1, 2 中的一个。默认值为 0`,
    );
    sort = 0;
  }
  if (duration !== 0 && duration !== 1 && duration !== 2 && duration !== 3) {
    utils.printError(
      `视频时长 ${duration} 无效, 请使用 0, 1, 2, 3 中的一个。默认值为 0`,
    );
    duration = 0;
  }
  if (
    publish_time !== 0 &&
    publish_time !== 1 &&
    publish_time !== 2 &&
    publish_time !== 3
  ) {
    utils.printError(
      `发布时间 ${publish_time} 无效, 请使用 0, 1, 2, 3 中的一个。默认值为 0`,
    );
    publish_time = 0;
  }
  if (limit < 1 || limit > 10000) {
    utils.printError(
      `搜索数量 ${limit} 无效, 请使用 1-10000 中的一个。默认值为 10`,
    );
    limit = 10;
  }
  return [sort, duration, publish_time, limit];
}

module.exports = {
  isKeywordValid,
  cleanKeyword,
  optionFormat,
};
