const constants = require("../config/constants");
const { requestApi } = require("../utils/request");

function processCommentResults(data) {
  if (!Array.isArray(data)) {
    return [];
  }

  return data.map((item) => {
    const processedItem = { ...item };

    if (item.author_uid) {
      processedItem.author_url = `https://www.tiktok.com/@${item.author_uid}`;
    }

    if (typeof item?.create_time === "number" && item.create_time) {
      processedItem.create_time_str = new Date(
        item.create_time * 1000,
      ).toLocaleString();
    }

    return processedItem;
  });
}

async function createCommentTask(token, url, limit) {
  const params = { _: Date.now() };

  const data = {
    url,
    limit,
  };

  return await requestApi(
    "POST",
    "/api/tiktok/comment/url",
    token,
    params,
    data,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getCommentTask(token, url, limit) {
  const params = {
    _: Date.now(),
    url: url,
    limit: limit,
  };

  const response = await requestApi(
    "GET",
    "/api/tiktok/comment/info",
    token,
    params,
    null,
    constants.QUERY_MAX_ATTEMPTS,
    "查询任务",
  );

  if (response.data) {
    return processCommentResults(response.data);
  }

  return [];
}

module.exports = {
  createCommentTask,
  getCommentTask,
};
