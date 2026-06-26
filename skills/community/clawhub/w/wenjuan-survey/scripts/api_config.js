#!/usr/bin/env node
/**
 * 问卷网 API 统一配置
 * 可通过环境变量 WENJUAN_HOST 覆盖默认域名。
 */

const { DEFAULT_WENJUAN_HOST, getWenjuanHost } = require("./wenjuan_env");

const WENJUAN_HOST = getWenjuanHost();

function wenjuanUrl(pathname = "") {
  if (!pathname) return WENJUAN_HOST;
  const p = String(pathname);
  return `${WENJUAN_HOST}${p.startsWith("/") ? p : `/${p}`}`;
}

module.exports = {
  DEFAULT_WENJUAN_HOST,
  WENJUAN_HOST,
  wenjuanUrl,
};
