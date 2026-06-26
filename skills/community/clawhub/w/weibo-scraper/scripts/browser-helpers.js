/**
 * Weibo Scraper - Browser Helper Scripts
 * 
 * 在 browser 工具的 evaluate 动作中使用这些代码片段。
 * 以下函数需要粘贴到 browser act → evaluate → fn 中执行。
 */

// ============ 滚动加载 ============
// 用法: browser act → evaluate → fn
// window.scrollTo(0, document.body.scrollHeight)

// ============ 提取所有帖子的日期和链接 ============
// 用法: browser act → evaluate → fn
// 返回 JSON 字符串，包含每条帖子的日期、时间、微博ID、是否截断

/*
(() => {
  const cards = document.querySelectorAll('.card');
  const posts = [];
  cards.forEach(card => {
    const timeEl = card.querySelector('.time');
    const articleEl = card.querySelector('.txt') || card.querySelector('article');
    const fullLink = card.querySelector('a[href*="/status/"]');
    if (timeEl) {
      posts.push({
        time: timeEl.textContent.trim(),
        hasFullLink: !!fullLink,
        statusId: fullLink ? fullLink.href.match(/status\/(\d+)/)?.[1] : null,
        preview: articleEl ? articleEl.textContent.trim().substring(0, 50) : ''
      });
    }
  });
  return JSON.stringify(posts, null, 2);
})()
*/

// ============ 提取详情页完整正文 ============
// 用法: 在 m.weibo.cn/status/{id} 页面执行
// 返回完整正文文本

/*
(() => {
  const article = document.querySelector('.txt') || document.querySelector('article');
  return article ? article.textContent.trim() : 'NOT FOUND';
})()
*/
