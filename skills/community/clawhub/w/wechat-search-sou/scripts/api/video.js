/**
 * 微信视频搜索模块
 */
const constants = require("../config/constants");
const { requestApi } = require("../utils/request");

/**
 * 创建微信视频搜索任务
 * @param {string} token - 技能令牌
 * @param {string} keyword - 搜索关键词
 * @param {number} sort - 排序, 0:综合, 1:最新, 2:最热
 * @param {number} duration - 视频时长, 0:不限, 1:5分钟以下, 2:5-20分钟, 3:20分钟以上
 * @param {number} limit - 搜索数量, 1-10000
 * @returns {Promise<Object>} 搜索任务状态
 * @throws {Error} API调用失败时抛出错误
 */
async function createSearchTask(token, keyword, sort, duration, limit) {
  const params = {
    _: Date.now(),
    token: token,
  };

  const data = {
    keyword,
    sort,
    duration,
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
 * @param {number} sort - 排序, 0:综合, 1:最新, 2:最热
 * @param {number} duration - 视频时长, 0:不限, 1:5分钟以下, 2:5-20分钟, 3:20分钟以上
 * @param {number} limit - 搜索数量, 1-10000
 * @returns {Promise<Array>} 搜索结果数组
 * @throws {Error} API调用失败时抛出错误
 */
async function getSearchTask(token, keyword, sort, duration, limit) {
  const params = {
    _: Date.now(),
    token: token,
    keyword: keyword,
    sort: sort,
    duration: duration,
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
