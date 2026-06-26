/**
 * escapeHtml — HTML 转义工具
 *
 * 用法：
 *   import { escapeHtml } from './escape-html.js';
 *   const safe = escapeHtml(userInput);
 *
 * 原理：利用 DOM API 自动转义，无需手动维护替换表。
 */

/**
 * 将字符串中的 HTML 特殊字符转义为实体
 * @param {string} str - 原始字符串
 * @returns {string} 转义后的安全 HTML
 */
export function escapeHtml(str) {
  if (str == null) return '';
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(String(str)));
  return div.innerHTML;
}
