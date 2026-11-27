/**
 * 后端数字 errcode → Skill 稳定 error_code。
 * 视频转文本与采集类接口码表不同：14=提示词过长；包月次数不足常为 2+"次数不足"；
 * CheckDayMoney 日限为 18。优先按 errmsg 判别。
 */
const { ApiError } = require("./errors");

const PROMPT_TOO_LONG_RE = /提示词不能超过|提示词过长/;
const PLAN_LIMIT_RE = /次数不足|包月类TOKEN|包月TOKEN/;
const BALANCE_RE = /余额可能不足|TOKEN余额|请通过www\.guaikei\.com充值/;
const RATE_RE = /短时间内请勿提交过多/;
const DAY_LIMIT_RE = /今日消费已达每日上限|每日消费限额|每日上限/;

/**
 * @param {number} errcode
 * @param {string} [errmsg]
 * @returns {ApiError}
 */
function mapBackendApiError(errcode, errmsg) {
  const msg = (errmsg && String(errmsg).trim()) || "";

  if (errcode === 14 || PROMPT_TOO_LONG_RE.test(msg)) {
    return new ApiError(
      "PROMPT_TOO_LONG",
      msg || "提示词不能超过 1000 个字符",
      true,
    );
  }

  if (PLAN_LIMIT_RE.test(msg)) {
    return new ApiError(
      "PLAN_LIMIT",
      msg || "今日可用次数不足，请明日再试或到 www.guaikei.com 升级套餐",
      true,
    );
  }

  if (BALANCE_RE.test(msg)) {
    return new ApiError(
      "INSUFFICIENT_BALANCE",
      msg ||
        "TOKEN 余额可能不足，请通过 www.guaikei.com 充值后重试",
      true,
    );
  }

  if (RATE_RE.test(msg)) {
    return new ApiError(
      "RATE_LIMITED",
      msg || "短时间内请勿提交过多任务，请稍后重试",
      true,
    );
  }

  if (errcode === 18 || DAY_LIMIT_RE.test(msg)) {
    return new ApiError(
      "DAILY_LIMIT",
      msg ||
        "今日消费已达每日上限，请明日再试，或登录 www.guaikei.com 调整每日消费限额",
      true,
    );
  }

  // 其余 errcode 2（TOKEN 获取失败、内部错误等）立即失败，避免无意义重试
  if (errcode === 2) {
    return new ApiError("API_ERROR", msg || "请求失败", true);
  }

  return new ApiError(
    errcode.toString(),
    msg || "请求失败",
    errcode >= 10 || (errcode !== 0 && errcode !== 1),
  );
}

module.exports = {
  mapBackendApiError,
  PROMPT_TOO_LONG_RE,
  PLAN_LIMIT_RE,
  BALANCE_RE,
  RATE_RE,
  DAY_LIMIT_RE,
};
