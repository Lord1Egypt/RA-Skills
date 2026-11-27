const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");

async function createHotTask(token, category) {
  const response = await requestApi(
    "POST",
    "/api/weibo/hot/category",
    { _: Date.now() },
    { category },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

async function getHotTask(token, category, taskId) {
  const params = taskId ? { id: taskId } : { category };
  const response = await pollTaskResult(
    "/api/weibo/hot/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (response.data == null) {
    return { results: [], cost };
  }
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "热搜结果格式异常", true);
  }
  return { results: response.data, cost };
}

module.exports = { createHotTask, getHotTask };
