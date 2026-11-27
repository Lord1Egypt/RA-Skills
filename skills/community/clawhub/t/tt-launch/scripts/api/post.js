const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");
const { SkillError } = require("../utils/errors");
const { formatCreateTime } = require("../utils/time");

function processPostResults(data) {
  if (!Array.isArray(data)) return [];
  const out = [];
  for (const item of data) {
    if (!item || typeof item !== "object" || !item.aweme_id) continue;
    const processed = { ...item };
    const timeText = formatCreateTime(item.create_time);
    if (timeText) processed.create_time_str = timeText;
    out.push(processed);
  }
  return out;
}

/**
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）
 */
async function createPostTask(token, url, sort, limit) {
  const response = await requestApi(
    "POST",
    "/api/tiktok/post/url",
    { _: Date.now() },
    {
      url,
      sort_type: sort,
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
async function getPostTask(token, url, sort, limit, taskId) {
  const params = taskId
    ? { id: taskId }
    : {
        url,
        sort_type: sort,
        limit,
      };
  const response = await pollTaskResult(
    "/api/tiktok/post/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "作品结果格式错误: data 不是数组", true);
  }
  return { results: processPostResults(response.data), cost };
}

module.exports = {
  createPostTask,
  getPostTask,
};
