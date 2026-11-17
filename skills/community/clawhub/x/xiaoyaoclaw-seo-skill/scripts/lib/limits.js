'use strict';
/**
 * limits.js — 全部硬上限集中一处（审阅时一眼可核对）
 *
 * 这些值同时写在 SKILL.md「网络与权限边界」里，改这里要同步改文档。
 */

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';

const MAX_DOMAINS = 10;                  // 单次运行最多审计 10 个域名
const MAX_BYTES_HTML = 1024 * 1024;      // 首页 HTML：1 MB
const MAX_BYTES_TEXT = 256 * 1024;       // robots/sitemap/llms.txt 等文本：256 KB
const MAX_REDIRECTS = 3;                 // 重定向最多 3 跳，每跳重新校验
const REQUEST_TIMEOUT_MS = 10000;        // 单次请求硬超时
const ALLOWED_PORTS = new Set([80, 443]); // 只允许标准端口，杜绝端口扫描

module.exports = {
  UA,
  MAX_DOMAINS,
  MAX_BYTES_HTML,
  MAX_BYTES_TEXT,
  MAX_REDIRECTS,
  REQUEST_TIMEOUT_MS,
  ALLOWED_PORTS,
};
