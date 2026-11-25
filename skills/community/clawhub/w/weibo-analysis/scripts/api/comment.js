const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");

async function createCommentTask(token, url, sort, limit) {
  const response = await requestApi(
    "POST",
    "/api/weibo/comment/url",
    { _: Date.now() },
    { url, sort_type: sort, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

async function getCommentTask(token, url, sort, limit, taskId) {
  const params = taskId
    ? { id: taskId }
    : { url, sort_type: sort, limit };
  const response = await pollTaskResult(
    "/api/weibo/comment/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (response.data == null) {
    return { results: [], cost };
  }
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "评论结果格式异常", true);
  }
  return { results: response.data, cost };
}

module.exports = { createCommentTask, getCommentTask };
