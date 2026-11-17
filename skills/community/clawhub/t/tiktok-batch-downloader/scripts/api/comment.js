const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { SkillError } = require("../utils/errors");
const { formatCreateTime } = require("../utils/time");
const { profileUrl } = require("../validate/url");

function processCommentResults(data) {
  if (!Array.isArray(data)) return [];
  const out = [];
  for (const item of data) {
    if (!item || typeof item !== "object" || !item.cid) continue;
    const processed = { ...item };
    const userUrl = profileUrl(item.user_uid);
    if (userUrl) processed.user_url = userUrl;
    const timeText = formatCreateTime(item.create_time);
    if (timeText) processed.create_time_str = timeText;
    out.push(processed);
  }
  return out;
}

async function createCommentTask(token, url, limit) {
  return await requestApi(
    "POST",
    "/api/tiktok/comment/url",
    { _: Date.now() },
    { url, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getCommentTask(token, url, limit) {
  const response = await pollTaskResult(
    "/api/tiktok/comment/info",
    { url, limit },
    token,
    "查询任务",
  );
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "评论结果格式错误: data 不是数组", true);
  }
  return processCommentResults(response.data);
}

module.exports = {
  createCommentTask,
  getCommentTask,
};
