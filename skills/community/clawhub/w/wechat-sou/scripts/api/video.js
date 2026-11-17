/**
 * 微信视频搜索模块
 */
const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { formatUnixSeconds } = require("../utils/time");

/**
 * @param {Array} data
 * @returns {Array}
 */
function processVideoResults(data) {
  if (!Array.isArray(data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "视频搜索结果格式异常", true);
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
 * 创建微信视频搜索任务
 */
async function createSearchTask(token, keyword, sort, duration, limit) {
  const params = { _: Date.now() };

  const data = {
    keyword,
    sort,
    duration,
    limit,
  };

  return await requestApi(
    "POST",
    "/api/wechat/video-search/keyword",
    params,
    data,
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

/**
 * 获取微信视频搜索任务结果
 */
async function getSearchTask(token, keyword, sort, duration, limit) {
  const params = {
    keyword: keyword,
    sort: sort,
    duration: duration,
    limit: limit,
  };

  const response = await pollTaskResult(
    "/api/wechat/video-search/info",
    params,
    token,
    "查询任务",
  );

  if (response.data) {
    return processVideoResults(response.data);
  }

  return [];
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
