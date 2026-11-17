/**
 * 固定为北京时间，格式如 2026/9/4 20:13:20，月和日不补零。
 * @param {Date} date
 * @returns {string}
 */
function formatBeijingTime(date) {
  const shifted = new Date(date.getTime() + 8 * 60 * 60 * 1000);
  const year = shifted.getUTCFullYear();
  const month = shifted.getUTCMonth() + 1;
  const day = shifted.getUTCDate();
  const hour = String(shifted.getUTCHours()).padStart(2, "0");
  const minute = String(shifted.getUTCMinutes()).padStart(2, "0");
  const second = String(shifted.getUTCSeconds()).padStart(2, "0");
  return `${year}/${month}/${day} ${hour}:${minute}:${second}`;
}

/**
 * 把接口里的 create_time 格式化成北京时间。
 * 小于 1e12 按 Unix 秒，否则按毫秒。无法识别时返回空字符串。
 * @param {number} value
 * @returns {string}
 */
function formatCreateTime(value) {
  if (typeof value !== "number" || !Number.isFinite(value) || value <= 0) {
    return "";
  }
  const ms = value >= 1e12 ? value : value * 1000;
  const date = new Date(ms);
  if (Number.isNaN(date.getTime())) return "";
  return formatBeijingTime(date);
}

module.exports = {
  formatBeijingTime,
  formatCreateTime,
};
