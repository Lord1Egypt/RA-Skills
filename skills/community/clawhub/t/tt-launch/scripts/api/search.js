const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");
const { SkillError } = require("../utils/errors");
const { formatCreateTime } = require("../utils/time");
const { profileUrl } = require("../validate/url");

function processSearchResults(data) {
  if (!Array.isArray(data)) return [];
  const out = [];
  for (const item of data) {
    if (!item || typeof item !== "object" || !item.aweme_id) continue;
    const processed = { ...item };
    const authorUrl = profileUrl(item.author_uid);
    if (authorUrl) processed.author_url = authorUrl;
    const timeText = formatCreateTime(item.create_time);
    if (timeText) processed.create_time_str = timeText;
    out.push(processed);
  }
  return out;
}

/**
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）；缺失则查询仅带业务字段
 */
async function createSearchTask(token, keyword, sort, time, limit) {
  const response = await requestApi(
    "POST",
    "/api/tiktok/search/keyword",
    { _: Date.now() },
    {
      keyword,
      sort_type: sort,
      publish_time: time,
      limit,
    },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

/**
 * @param {string} [taskId] Create 返回的任务 id；有则查询只传 id（不带业务字段）
 * @returns {Promise<{ results: Array, cost?: number }>}
 */
async function getSearchTask(token, keyword, sort, time, limit, taskId) {
  const params = taskId
    ? { id: taskId }
    : {
        keyword,
        sort_type: sort,
        publish_time: time,
        limit,
      };
  const response = await pollTaskResult(
    "/api/tiktok/search/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "搜索结果格式错误: data 不是数组", true);
  }
  return { results: processSearchResults(response.data), cost };
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
