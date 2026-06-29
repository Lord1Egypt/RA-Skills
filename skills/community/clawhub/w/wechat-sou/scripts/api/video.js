/**
 * 微信视频搜索模块
 */
const constants = require("../config/constants");
const { requestApi } = require("../utils/request");

/**
 * 创建微信视频搜索任务
 * @param {string} token - 技能令牌
 * @param {string} keyword - 搜索关键词
 * @param {number} limit - 搜索数量, 1-100000
 * @returns {Promise<Object>} 搜索任务状态
 * @throws {Error} API调用失败时抛出错误
 */
async function createSearchTask(token, keyword, limit) {
  const params = {
    _: Date.now(),
    token: token,
  };

  const data = {
    keyword,
    limit,
  };

  return await requestApi(
    "POST",
    "/api/wechat/video-search/keyword",
    params,
    data,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

/**
 * 获取微信视频搜索任务结果
 * @param {string} token - 技能令牌
 * @param {string} keyword - 搜索关键词
 * @param {number} limit - 搜索数量, 1-100000
 * @returns {Promise<Array>} 搜索结果数组
 * @throws {Error} API调用失败时抛出错误
 */
async function getSearchTask(token, keyword, limit) {
  const params = {
    _: Date.now(),
    token: token,
    keyword: keyword,
    limit: limit,
  };

  const response = await requestApi(
    "GET",
    "/api/wechat/video-search/info",
    params,
    null,
    constants.QUERY_MAX_ATTEMPTS,
    "查询任务",
  );

  if (response.data) {
    return response.data;
  }

  return [];
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
