/**
 * TOKEN管理模块
 */
const utils = require("./utils");

/**
 * 验证 TOKEN 格式
 * @param {string} token - 待验证的 TOKEN
 * @returns {boolean} 是否有效
 */
function isValidToken(token) {
  if (!token || typeof token !== "string") {
    return false;
  }

  if (token.length !== 32) {
    return false;
  }

  const hexPattern = /^[0-9a-fA-F]{32}$/;
  return hexPattern.test(token);
}

/**
 * 获取有效的技能令牌
 * @param {string|undefined} token - 环境变量中的技能令牌
 * @returns {string} 有效令牌
 */
function skillToken(token) {
  if (!isValidToken(token)) {
    utils.printWarn(
      "警告: 你的 GUAIKEI_API_TOKEN 未正确配置,技能已暂停. \n" +
        "请添加微信: 13395823479,获取专属私有TOKEN,一键配置即可恢复全部功能,永久稳定可用,不影响日常办公!",
    );
    return "";
  }

  utils.printInfo("已使用配置的私有TOKEN");
  return token;
}

module.exports = {
  skillToken,
};
