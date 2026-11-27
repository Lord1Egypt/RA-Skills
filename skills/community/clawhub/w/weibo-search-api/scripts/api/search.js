const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");

async function createSearchTask(token, keyword, searchType, limit) {
  const response = await requestApi(
    "POST",
    "/api/weibo/search/keyword",
    { _: Date.now() },
    { keyword, search_type: searchType, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

async function getSearchTask(token, keyword, searchType, limit, taskId) {
  const params = taskId
    ? { id: taskId }
    : { keyword, search_type: searchType, limit };
  const response = await pollTaskResult(
    "/api/weibo/search/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (response.data == null) {
    return { results: [], cost };
  }
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "搜索结果格式异常", true);
  }
  return { results: response.data, cost };
}

module.exports = { createSearchTask, getSearchTask };
