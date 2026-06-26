/**
 * 内容提取模块
 * 负责从页面中提取标题和正文内容
 */

/**
 * 从页面中提取标题
 * @param {Page} page - 页面实例
 * @returns {Promise<string>} 标题
 */
async function extractTitle(page) {
  return await page.evaluate(() => {
    const el = document.querySelector('h2.rich_media_title') || 
              document.querySelector('#activity_name') || 
              document.querySelector('meta[property="og:title"]');
    return el ? (el.getAttribute('content') || el.textContent || '').trim() : '';
  });
}

/**
 * 从页面中提取正文内容
 * @param {Page} page - 页面实例
 * @returns {Promise<string>} 正文内容
 */
async function extractContent(page) {
  return await page.evaluate(() => {
    const el = document.querySelector('#js_content');
    return el ? el.innerText.trim() : '';
  });
}

/**
 * 从页面中提取所有内容
 * @param {Page} page - 页面实例
 * @returns {Promise<Object>} 包含标题和内容的对象
 */
async function extractAll(page) {
  const title = await extractTitle(page);
  const content = await extractContent(page);
  const url = page.url();
  
  return {
    title,
    content,
    url
  };
}

module.exports = {
  extractTitle,
  extractContent,
  extractAll
};
