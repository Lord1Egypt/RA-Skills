const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
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

async function createPostTask(token, url, sort, limit) {
  return await requestApi(
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
}

async function getPostTask(token, url, sort, limit) {
  const response = await pollTaskResult(
    "/api/tiktok/post/info",
    {
      url,
      sort_type: sort,
      limit,
    },
    token,
    "查询任务",
  );
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "作品结果格式错误: data 不是数组", true);
  }
  return processPostResults(response.data);
}

module.exports = {
  createPostTask,
  getPostTask,
};
