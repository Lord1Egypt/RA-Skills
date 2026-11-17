const constants = require("../config/constants");
const { requestApi } = require("../utils/request");

function processPostResults(data) {
  if (!Array.isArray(data)) {
    return [];
  }
  return data;
}

async function createPostTask(token, url, sort, limit) {
  const params = { _: Date.now() };
  const data = {
    url: url,
    sort_type: sort,
    limit: limit,
  };
  return await requestApi(
    "POST",
    "/api/tiktok/post/url",
    token,
    params,
    data,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getPostTask(token, url, sort, limit) {
  const params = {
    _: Date.now(),
    url: url,
    sort_type: sort,
    limit: limit,
  };
  const response = await requestApi(
    "GET",
    "/api/tiktok/post/info",
    token,
    params,
    null,
    constants.QUERY_MAX_ATTEMPTS,
    "查询任务",
  );
  if (response.data) {
    return processPostResults(response.data);
  }
  return [];
}

module.exports = {
  createPostTask,
  getPostTask,
};
