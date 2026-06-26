/**
 * 抖音评论一键检查脚本
 * 直接在浏览器 evaluate 中执行，返回待处理的评论列表
 * 
 * 使用方式：
 * browser act evaluate fn: "<此脚本内容>"
 * 
 * 返回格式：
 * {
 *   success: true,
 *   page: 'comments',
 *   videoTitle: '视频标题',
 *   pendingComments: [
 *     { index, author, time, content, hasReplied }
 *   ],
 *   total: number,
 *   pending: number
 * }
 */

(function() {
  const result = {
    success: true,
    page: 'comments',
    videoTitle: '',
    pendingComments: [],
    total: 0,
    pending: 0
  };

  // 检查是否在评论管理页面
  if (!window.location.href.includes('/comment')) {
    result.success = false;
    result.error = '当前不在评论管理页面';
    return JSON.stringify(result);
  }

  // 获取视频标题 - 根据实际页面结构
  const titleSelectors = [
    '[class*="video-title"]',
    '[class*="works-title"]', 
    '[class*="title"]'
  ];
  
  for (const sel of titleSelectors) {
    const el = document.querySelector(sel);
    if (el && el.textContent.trim().length > 0 && el.textContent.trim().length < 200) {
      result.videoTitle = el.textContent.trim();
      break;
    }
  }

  // 解析评论 - 根据实际 DOM 结构
  // 评论通常在 listitem 或 li 元素中
  const allItems = document.querySelectorAll('li, [role="listitem"]');
  
  allItems.forEach((item, idx) => {
    // 跳过非评论项
    const itemText = item.textContent || '';
    if (itemText.includes('没有更多') || itemText.includes('有爱评论')) {
      return;
    }
    
    // 提取评论者名称
    let author = '';
    const nameEl = item.querySelector('[class*="name"]');
    if (nameEl) {
      author = nameEl.textContent.trim();
    }
    
    // 如果没找到name class，尝试其他方式
    if (!author) {
      // 评论者名称通常是较早出现的短文本
      const textNodes = item.querySelectorAll('div > div, span');
      for (const node of textNodes) {
        const text = node.textContent.trim();
        if (text.length > 0 && text.length < 20 && !text.includes('分钟') && !text.includes('小时')) {
          author = text;
          break;
        }
      }
    }
    
    // 提取时间
    let time = '';
    const timePatterns = ['分钟前', '小时前', '天前', '刚刚', '-'];
    const allText = item.textContent;
    for (const pattern of timePatterns) {
      const match = allText.match(new RegExp(`(\\d*${pattern})`));
      if (match) {
        time = match[1];
        break;
      }
    }
    
    // 提取评论内容
    let content = '';
    const contentCandidates = item.querySelectorAll('[class*="content"], [class*="text"]');
    for (const c of contentCandidates) {
      const text = c.textContent.trim();
      if (text.length > 0 && text !== author && !timePatterns.some(p => text.includes(p))) {
        content = text;
        break;
      }
    }
    
    // 检查是否已回复
    const hasAuthorTag = itemText.includes('作者') && itemText.indexOf('作者') < itemText.indexOf(content || 'x');
    const hasReplyBtn = itemText.includes('回复');
    
    // 有效评论判定
    if (content && content.length > 0 && !content.includes('有爱评论')) {
      result.total++;
      
      const commentInfo = {
        index: idx,
        author: author || '未知用户',
        time: time || '未知时间',
        content: content.substring(0, 100), // 截断过长内容
        hasReplied: hasAuthorTag
      };
      
      // 未回复的评论加入待处理列表
      if (!hasAuthorTag && hasReplyBtn) {
        result.pending++;
        result.pendingComments.push(commentInfo);
      }
    }
  });

  return JSON.stringify(result, null, 2);
})();
