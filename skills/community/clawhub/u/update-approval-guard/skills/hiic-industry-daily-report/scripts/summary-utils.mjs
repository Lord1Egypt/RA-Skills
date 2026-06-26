/**
 * 清理摘要，移除元数据标签
 */
function cleanSummary(text) {
  if (!text) return '';
  
  let cleaned = text
    // 移除常见的元数据标签
    .replace(/^Title:\s*/i, '')
    .replace(/^URL Source:\s*/i, '')
    .replace(/^Markdown Content:\s*/i, '')
    .replace(/^Published Time:\s*/i, '')
    .replace(/^Author:\s*/i, '')
    .replace(/^来源：\s*/i, '')
    .replace(/URL Source:.*$/gm, '')
    // 移除多余的空格和换行
    .replace(/\s+/g, ' ')
    .trim();
  
  return cleaned;
}

/**
 * 生成高质量摘要（不重复标题）
 */
function generateSummary(content, title, originalDesc, options = {}) {
  const { minLength = 60, maxLength = 200 } = options;
  
  // 优先级：完整内容 > 原始描述
  let source = content || originalDesc;
  
  if (!source) return '暂无详细内容';
  
  // 清理元数据
  source = cleanSummary(source);
  
  // 移除标题重复部分
  const titleKeywords = title.split(/\s+/).filter(w => w.length > 2);
  for (const keyword of titleKeywords) {
    if (source.startsWith(keyword)) {
      source = source.slice(keyword.length).trim();
      break;
    }
  }
  
  // 如果内容太短，直接返回
  if (source.length <= maxLength) {
    return source.slice(0, maxLength);
  }
  
  // 提取摘要
  let summary = source.slice(0, maxLength);
  
  // 尝试在标点符号处截断
  const punctuations = ['。', '？', '！', '；', '.', '?', '!', ';'];
  let lastPunctuation = -1;
  
  for (const punct of punctuations) {
    const idx = summary.lastIndexOf(punct);
    if (idx > lastPunctuation && idx >= minLength * 0.6) {
      lastPunctuation = idx;
    }
  }
  
  if (lastPunctuation >= minLength * 0.7) {
    summary = summary.slice(0, lastPunctuation + 1);
  } else {
    // 在逗号处截断
    const lastComma = Math.max(
      summary.lastIndexOf('，'),
      summary.lastIndexOf(','),
      summary.lastIndexOf('、')
    );
    
    if (lastComma >= minLength * 0.7) {
      summary = summary.slice(0, lastComma);
    }
    summary = summary.trim() + '...';
  }
  
  return summary;
}
