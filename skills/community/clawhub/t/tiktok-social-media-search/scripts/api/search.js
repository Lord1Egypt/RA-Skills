const constants = require("../config/constants");
const { requestApi } = require("../utils/request");

function processSearchResults(data) {
  if (!Array.isArray(data)) {
    return [];
  }

  return data.map((item) => {
    const processedItem = { ...item };

    if (item.author_uid) {
      processedItem.author_url = `https://www.tiktok.com/@${item.author_uid}`;
    }

    if (
      typeof item?.create_time === "number" &&
      item.create_time &&
      !item.create_time_str
    ) {
      processedItem.create_time_str = new Date(
        item.create_time * 1000,
      ).toLocaleString();
    }

    return processedItem;
  });
}

async function createSearchTask(token, keyword, sort, time, limit) {
  const params = { _: Date.now() };

  const data = {
    keyword,
    sort_type: sort,
    publish_time: time,
    limit: limit,
  };

  return await requestApi(
    "POST",
    "/api/tiktok/search/keyword",
    token,
    params,
    data,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getSearchTask(token, keyword, sort, time, limit) {
  const params = {
    _: Date.now(),
    keyword: keyword,
    sort_type: sort,
    publish_time: time,
    limit: limit,
  };

  const response = await requestApi(
    "GET",
    "/api/tiktok/search/info",
    token,
    params,
    null,
    constants.QUERY_MAX_ATTEMPTS,
    "查询任务",
  );

  if (response.data) {
    return processSearchResults(response.data);
  }

  return [];
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
