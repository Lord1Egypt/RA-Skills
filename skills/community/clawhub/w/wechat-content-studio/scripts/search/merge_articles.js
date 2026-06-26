/**
 * 多篇文章合并工具
 * 将多篇文章智能合并为一篇，保留所有图片引用
 */

/**
 * 合并多篇文章
 * @param {Array} articles - 文章数组（来自搜索或提取）
 * @param {string} keyword - 搜索关键词或主题
 * @returns {Object} 合并后的文章对象
 */
export function mergeArticles(articles, keyword = '精选文章') {
  if (!articles || articles.length === 0) {
    throw new Error('没有文章可合并');
  }

  // 生成新标题
  const title = generateMergedTitle(articles, keyword);
  
  // 合并内容
  const mergedContent = mergeContent(articles);
  
  // 生成 Markdown
  const markdown = generateMarkdown(title, mergedContent, articles);
  
  return {
    title,
    content: mergedContent.html,
    markdown,
    sourceCount: articles.length,
    sources: articles.map(a => ({
      title: a.title || a.msg_title,
      url: a.url || a.msg_link,
      author: a.author || a.msg_author,
      source: a.source || a.account_name
    }))
  };
}

/**
 * 生成合并后的标题
 */
function generateMergedTitle(articles, keyword) {
  const topics = new Set();
  
  // 从各文章标题中提取关键词
  articles.forEach(article => {
    const title = article.title || article.msg_title || '';
    // 简单分词（实际应该用更智能的方法）
    const words = title.split(/[\s,，.。]/).filter(w => w.length > 1);
    words.forEach(w => {
      if (!isStopWord(w)) {
        topics.add(w);
      }
    });
  });
  
  // 如果有关键词，优先使用
  if (keyword && keyword.length > 1) {
    return `${keyword}深度解析：${Array.from(topics).slice(0, 5).join('·')}`;
  }
  
  // 否则使用前几篇文章的标题组合
  const mainTopics = Array.from(topics).slice(0, 3).join(' · ');
  return `精选合集：${mainTopics}`;
}

/**
 * 合并多篇文章的内容
 */
function mergeContent(articles) {
  let html = '';
  let imageIndex = 0;
  const imageMap = new Map(); // 原图片 URL -> 新图片路径
  
  articles.forEach((article, index) => {
    const title = article.title || article.msg_title || '无标题';
    const author = article.author || article.msg_author || article.account_name || '佚名';
    const source = article.source || article.account_name || '未知来源';
    
    // 添加来源分隔
    html += `
<section style="margin: 40px 0; padding: 30px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #07c160;">
  <h2 style="margin: 0 0 15px 0; color: #333; font-size: 20px;">📌 来源${index + 1}：${title}</h2>
  <p style="margin: 0; color: #999; font-size: 14px;">
    <span>作者：${author}</span> | 
    <span>公众号：${source}</span>
  </p>
</section>
`;
    
    // 提取并处理正文内容
    let content = article.content || article.msg_content || '';
    
    if (content) {
      // 处理图片引用
      content = content.replace(/<img[^>]*?(?:data-src|src)="([^"]*)"[^>]*?>/gi, (match, src) => {
        imageIndex++;
        const newSrc = `images/image_${imageIndex}.jpg`;
        imageMap.set(src, newSrc);
        return match.replace(src, newSrc);
      });
      
      // 添加内容
      html += `<div style="margin: 30px 0;">${content}</div>`;
    }
    
    // 添加分隔线
    if (index < articles.length - 1) {
      html += `<hr style="border: none; border-top: 2px dashed #e0e0e0; margin: 40px 0;">`;
    }
  });
  
  return {
    html,
    imageCount: imageIndex,
    imageMap
  };
}

/**
 * 生成 Markdown 格式
 */
function generateMarkdown(title, mergedContent, articles) {
  let md = `---
title: ${title}
cover: ./images/cover.jpg
---

# ${title}

> **本文整合自 ${articles.length} 篇精选文章**，为您呈现多角度的深度解析。

---

${mergedContent.html}

---

## 📚 参考来源

${articles.map((article, i) => {
  const t = article.title || article.msg_title || '无标题';
  const a = article.author || article.msg_author || '佚名';
  const s = article.source || article.account_name || '未知来源';
  const url = article.url || article.msg_link || '#';
  return `${i + 1}. **${t}** - ${a}（${s}）[阅读原文](${url})`;
}).join('\n')}

---

*本文内容源自网络公开文章，版权归原作者和公众号所有，仅用于学习分享。*
`;

  // 简单的 HTML 转 Markdown（保留核心结构）
  md = md.replace(/<section[^>]*>([\s\S]*?)<\/section>/gi, '$1\n\n');
  md = md.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '## $1\n\n');
  md = md.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '$1\n\n');
  md = md.replace(/<div[^>]*>([\s\S]*?)<\/div>/gi, '$1\n\n');
  md = md.replace(/<span[^>]*>([\s\S]*?)<\/span>/gi, '$1');
  md = md.replace(/<br\s*\/?>/gi, '\n');
  md = md.replace(/<[^>]+>/g, '');
  md = md.replace(/\n{3,}/g, '\n\n');
  
  return md.trim();
}

/**
 * 常见停用词
 */
function isStopWord(word) {
  const stopWords = new Set([
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
    '他', '她', '它', '们', '这个', '那个', '什么', '怎么', '可以'
  ]);
  return stopWords.has(word.toLowerCase());
}
