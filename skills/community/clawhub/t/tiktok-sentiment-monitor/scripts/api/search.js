const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
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

async function createSearchTask(token, keyword, sort, time, limit) {
  return await requestApi(
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
}

async function getSearchTask(token, keyword, sort, time, limit) {
  const response = await pollTaskResult(
    "/api/tiktok/search/info",
    {
      keyword,
      sort_type: sort,
      publish_time: time,
      limit,
    },
    token,
    "查询任务",
  );
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "搜索结果格式错误: data 不是数组", true);
  }
  return processSearchResults(response.data);
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
