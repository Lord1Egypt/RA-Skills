/**
 * 后端数字 errcode → Skill 稳定 error_code。
 * 优先按 errmsg 判别。日消费上限为后端 CheckDayMoney 的 18（不是 17）。
 */
const { ApiError } = require("./errors");

const PLAN_LIMIT_RE = /包月TOKEN|搜索量受限|最多支持\d+条/;
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

  if (PLAN_LIMIT_RE.test(msg)) {
    return new ApiError(
      "PLAN_LIMIT",
      msg ||
        "当前 TOKEN 套餐单次条数超限（包月：文章/视频搜索最多 20 条）。请降低 --limit，或到 www.guaikei.com 升级按量套餐",
      true,
    );
  }

  if (errcode === 15 || BALANCE_RE.test(msg)) {
    return new ApiError(
      "INSUFFICIENT_BALANCE",
      msg ||
        "TOKEN 余额可能不足，请通过 www.guaikei.com 充值后重试",
      true,
    );
  }

  if (errcode === 2 || RATE_RE.test(msg)) {
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

  return new ApiError(
    errcode.toString(),
    msg || "请求失败",
    errcode >= 10,
  );
}

module.exports = {
  mapBackendApiError,
  PLAN_LIMIT_RE,
  BALANCE_RE,
  RATE_RE,
  DAY_LIMIT_RE,
};
