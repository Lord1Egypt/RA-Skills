/**
 * 格式化输出模块
 * 负责处理不同格式的输出，如JSON、Markdown等
 */

/**
 * 格式化为JSON格式
 * @param {Object} data - 要格式化的数据
 * @returns {string} JSON格式的字符串
 */
function formatJson(data) {
  return JSON.stringify(data, null, 2);
}

/**
 * 格式化为Markdown格式
 * @param {Object} data - 要格式化的数据
 * @returns {string} Markdown格式的字符串
 */
function formatMarkdown(data) {
  let markdown = `# ${data.title}\n\n`;
  markdown += `[原文链接](${data.url})\n\n`;
  markdown += data.content.replace(/\n/g, '\n\n');
  return markdown;
}

/**
 * 根据指定格式格式化数据
 * @param {Object} data - 要格式化的数据
 * @param {string} format - 格式类型（json, markdown）
 * @returns {string} 格式化后的字符串
 */
function format(data, format = 'json') {
  switch (format.toLowerCase()) {
    case 'markdown':
      return formatMarkdown(data);
    case 'json':
    default:
      return formatJson(data);
  }
}

module.exports = {
  formatJson,
  formatMarkdown,
  format
};
