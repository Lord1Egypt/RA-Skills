/**
 * TOKEN管理模块
 */
const utils = require("./utils");

function isValidToken(token) {
  if (!token || typeof token !== "string") return false;
  if (token.length < 16 || token.length > 256) return false;
  if (!/^[0-9a-zA-Z\_-]+$/.test(token)) return false;
  return true;
}

function skillKey(token) {
  token = (token || "").trim();
  if (!isValidToken(token)) {
    utils.printError(
      "警告: 你的 GUAIKEI_API_TOKEN 未配置或已失效,技能功能已暂停服务. ",
    );
    return "";
  }

  utils.printInfo("已使用配置的私有TOKEN");
  return token;
}

module.exports = {
  skillKey,
};
