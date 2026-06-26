/**
 * 检查抖音创作者中心的新评论
 * 在浏览器中通过 browser act evaluate 执行
 * 
 * 返回格式：
 * {
 *   success: true,
 *   type: 'comments',
 *   comments: [
 *     { id, author, content, time, hasReplied }
 *   ],
 *   videoTitle: string
 * }
 */

(function() {
  const result = {
    success: true,
    type: 'comments',
    comments: [],
    videoTitle: ''
  };

  // 获取视频标题
  const titleEl = document.querySelector('[class*="video-title"], [class*="title"]');
  if (titleEl) {
    result.videoTitle = titleEl.textContent.trim();
  }

  // 尝试从页面中提取视频标题
  const videoInfoEl = document.querySelector('[class*="video-info"], [class*="works"]');
  if (videoInfoEl) {
    const titleSpan = videoInfoEl.querySelector('span, div');
    if (titleSpan) {
      result.videoTitle = titleSpan.textContent.trim();
    }
  }

  // 解析评论列表 - 根据实际DOM结构
  // 评论项通常包含：用户名、时间、评论内容、回复/删除/举报按钮
  function parseComments() {
    const items = [];
    
    // 查找评论容器 - 多种选择器尝试
    const commentContainers = document.querySelectorAll([
      '[class*="comment-item"]',
      '[class*="CommentItem"]',
      '[data-e2e="comment-item"]'
    ].join(', '));
    
    // 如果精确选择器没找到，用更宽泛的查找
    const containers = commentContainers.length > 0 
      ? commentContainers 
      : document.querySelectorAll('li, [role="listitem"]');
    
    containers.forEach((el, index) => {
      try {
        // 提取用户名 - 通常是第一个文本元素
        const authorEl = el.querySelector([
          '[class*="author"]',
          '[class*="name"]',
          '[class*="username"]'
        ].join(', '));
        
        // 提取评论内容
        const contentEl = el.querySelector([
          '[class*="content"]',
          '[class*="text"]',
          '[class*="comment-text"]'
        ].join(', '));
        
        // 提取时间
        const timeEl = el.querySelector('[class*="time"]');
        
        // 检查是否已回复 - 查找是否有"作者"标签或已回复标记
        const authorTag = el.querySelector('[class*="author-tag"], [class*="tag"]');
        const hasAuthorReply = authorTag && authorTag.textContent.includes('作者');
        
        // 检查是否有"回复"按钮（如果回复按钮还在，说明未回复）
        const replyBtn = el.querySelector('[class*="reply"]');
        const hasReplyButton = replyBtn && replyBtn.textContent.includes('回复');
        
        if (contentEl && contentEl.textContent.trim()) {
          const content = contentEl.textContent.trim();
          // 排除空内容和占位符文本
          if (content && !content.includes('有爱评论') && content.length > 0) {
            items.push({
              id: `comment_${index}_${Date.now()}`,
              author: authorEl ? authorEl.textContent.trim() : '未知用户',
              content: content,
              time: timeEl ? timeEl.textContent.trim() : '',
              hasReplied: hasAuthorReply,
              hasReplyButton: hasReplyButton,
              element: el.outerHTML.substring(0, 500) // 用于调试
            });
          }
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
