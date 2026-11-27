/**
 * 后端数字 errcode → Skill 稳定 error_code。
 * 顺序：包月文案 → 余额（搜索 16 / 作品·评论 15 / 文案）→ 裸 14 作 PLAN_LIMIT → 频控 → 日限。
 * 搜索 Create：余额官方码 16；查价失败走 Gate 的 1（可重试），不用 15。
 * 搜索频控误用 1（与「处理中」同码），靠 RATE_RE；搜索的 2 是插入失败（可重试）。
 */
const { ApiError } = require("./errors");

const PLAN_LIMIT_RE = /包月TOKEN|搜索量受限|作品量受限|评论量受限|最多支持\d+条/;
const BALANCE_RE = /余额可能不足|TOKEN余额|请通过www\.guaikei\.com充值/;
const RATE_RE = /短时间内请勿提交过多/;
const DAY_LIMIT_RE = /今日消费已达每日上限|每日消费限额|每日上限/;

const PLAN_LIMIT_FALLBACK =
  "当前 TOKEN 套餐单次条数超限（包月：搜索/作品最多 30，评论最多 40）。请降低 --limit，或到 www.guaikei.com 升级按量套餐";

/**
 * @param {number} errcode
 * @param {string} [errmsg]
 * @param {"search"|"post"|"comment"|""} [apiKind]
 * @returns {ApiError}
 */
function mapBackendApiError(errcode, errmsg, apiKind) {
  const msg = (errmsg && String(errmsg).trim()) || "";
  const kind = apiKind || "";

  if (PLAN_LIMIT_RE.test(msg)) {
    return new ApiError("PLAN_LIMIT", msg || PLAN_LIMIT_FALLBACK, true);
  }

  // 搜索余额 16；余额文案通用（含搜索异常带 15+余额文案）
  if (errcode === 16 || BALANCE_RE.test(msg)) {
    return new ApiError(
      "INSUFFICIENT_BALANCE",
      msg ||
        "TOKEN 余额可能不足，请通过 www.guaikei.com 充值后重试",
      true,
    );
  }

  // 作品/评论余额 15；搜索现行后端不用 15 表余额，裸 15 勿引导充值
  if (errcode === 15 && kind !== "search") {
    return new ApiError(
      "INSUFFICIENT_BALANCE",
      msg ||
        "TOKEN 余额可能不足，请通过 www.guaikei.com 充值后重试",
      true,
    );
  }

  if (errcode === 14) {
    return new ApiError("PLAN_LIMIT", msg || PLAN_LIMIT_FALLBACK, true);
  }

  // 作品/评论频控官方码 2；搜索频控为 1 + 文案（搜索的 2 是插入失败，勿当频控）
  if (RATE_RE.test(msg) || (errcode === 2 && kind !== "search")) {
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
