/**
 * 检查抖音创作者中心的新评论
 * 在浏览器中通过 evaluate 执行此脚本
 * 
 * 返回格式：
 * {
 *   type: 'comments',
 *   comments: [
 *     { id, author, content, time, hasReplied }
 *   ]
 * }
 */

(function() {
  const result = {
    type: 'comments',
    comments: []
  };

  // 解析评论
  function parseComments() {
    const items = [];
    const commentElements = document.querySelectorAll('[class*="comment"]');
    
    commentElements.forEach((el, index) => {
      try {
        // 尝试提取评论信息
        const authorEl = el.querySelector('[class*="name"], [class*="author"]');
        const contentEl = el.querySelector('[class*="content"], [class*="text"]');
        const timeEl = el.querySelector('[class*="time"], [class*="date"]');
        
        // 检查是否已回复（有嵌套的回复区域）
        const replyArea = el.querySelector('[class*="reply"]');
        const hasReplied = replyArea !== null;
        
        if (contentEl && contentEl.textContent.trim()) {
          items.push({
            id: `comment_${index}_${Date.now()}`,
            author: authorEl ? authorEl.textContent.trim() : '未知用户',
            content: contentEl.textContent.trim(),
            time: timeEl ? timeEl.textContent.trim() : '',
            hasReplied: hasReplied
          });
        }
      } catch (e) {
        // 忽略解析错误
      }
    });
    
    return items;
  }

  result.comments = parseComments();
  return JSON.stringify(result, null, 2);
})();
