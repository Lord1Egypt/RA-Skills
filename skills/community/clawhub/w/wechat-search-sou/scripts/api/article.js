/**
 * 微信文章搜索模块
 */
const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { formatUnixSeconds } = require("../utils/time");

/**
 * @param {Array} data
 * @returns {Array}
 */
function processArticleResults(data) {
  if (!Array.isArray(data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "文章搜索结果格式异常", true);
  }

  return data.map((item) => {
    const processedItem = { ...item };
    if (
      typeof item?.pubtime === "number" &&
      item.pubtime &&
      !item.pubtime_str
    ) {
      processedItem.pubtime_str = formatUnixSeconds(item.pubtime);
    }
    return processedItem;
  });
}

/**
 * 创建微信文章搜索任务
 */
async function createSearchTask(token, keyword, sort, publish_time, limit) {
  const params = { _: Date.now() };

  const data = {
    keyword,
    sort,
    publish_time,
    limit,
  };

  return await requestApi(
    "POST",
    "/api/wechat/article-search/keyword",
    params,
    data,
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

/**
 * 获取微信文章搜索任务结果
 */
async function getSearchTask(token, keyword, sort, publish_time, limit) {
  const params = {
    keyword: keyword,
    sort: sort,
    publish_time: publish_time,
    limit: limit,
  };

  const response = await pollTaskResult(
    "/api/wechat/article-search/info",
    params,
    token,
    "查询任务",
  );

  if (response.data) {
    return processArticleResults(response.data);
  }

  return [];
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
