/**
 * 微信文章搜索模块
 */
const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");
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
    if (!item || typeof item !== "object") return item;
    const processedItem = { ...item };
    if (
      typeof item.pubtime === "number" &&
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
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）；缺失则查询仅带业务字段
 */
async function createSearchTask(token, keyword, sort, publish_time, limit) {
  const params = { _: Date.now() };

  const data = {
    keyword,
    sort,
    publish_time,
    limit,
  };

  const response = await requestApi(
    "POST",
    "/api/wechat/article-search/keyword",
    params,
    data,
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

/**
 * 获取微信文章搜索任务结果
 * @param {string} [taskId] Create 返回的任务 id；有则查询只传 id（不带业务字段）
 */
async function getSearchTask(
  token,
  keyword,
  sort,
  publish_time,
  limit,
  taskId,
) {
  const params = taskId
    ? { id: taskId }
    : {
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

  const cost = pickCost(response);
  if (response.data) {
    return { results: processArticleResults(response.data), cost };
  }

  return { results: [], cost };
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
