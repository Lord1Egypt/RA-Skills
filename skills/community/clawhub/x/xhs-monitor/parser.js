/**
 * 模块4: 正则匹配 + LLM意图解析
 * 提取: 直播时间、商品、笔记类型、标题、正文
 */

// 关键词匹配规则
const KEYWORDS = {
  live: ['直播', '啵啵间', '开播', '今晚', '明晚', '几点', '几点开播', '直播预告'],
  product: ['上新', '新款', '新品', '餐具', '餐盘', '杯子', '摆件', '装饰', '家具', '好物', '推荐', '分享'],
  preview: ['预告', '预告来了', '即将', '要来了', '明天', '周五', '周六', '周日']
};

// 匹配笔记类型
const matchNoteType = (text) => {
  const lowerText = text.toLowerCase();
  if (KEYWORDS.live.some(k => lowerText.includes(k))) return '直播预告';
  if (KEYWORDS.product.some(k => lowerText.includes(k))) return '新品上架';
  return '日常分享';
};

// 提取直播时间
const extractLiveTime = (text) => {
  const patterns = [/今晚(\d+)[点时]/, /明晚(\d+)[点时]/, /今天(\d+)[点时]/, /明天(\d+)[点时]/, /(\d+)[点时]/];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) return m[0];
  }
  return null;
};

// 提取商品
const extractProducts = (text) => {
  const products = [];
  const kw = ['Doing Goods', '新款', '新品', '上新'];
  for (const k of kw) {
    if (text.includes(k)) {
      const idx = text.indexOf(k);
      const after = text.substring(idx + k.length).split('\n')[0].trim();
      if (after && after.length > 1 && after.length < 50) {
        products.push(k + after);
      }
    }
  }
  return products.length > 0 ? products : [];
};

// 提取标题（通常是第一行或包含关键字的短句）
const extractTitle = (text) => {
  const lines = text.split('\n').filter(l => l.trim());
  if (lines.length > 0) {
    // 取第一行作为标题
    return lines[0].trim().substring(0, 100);
  }
  return '';
};

// 提取正文（去掉第一行和账号名等噪音）
const extractContent = (text) => {
  const lines = text.split('\n').filter(l => l.trim());
  // 去掉第一行（标题）和最后几行（账号名、点赞数等）
  const content = lines.slice(1, -2).join(' ').trim();
  return content.substring(0, 200);
};

// 生成一句话总结
const generateSummary = (note) => {
  const parts = [];
  
  if (note.title) parts.push(note.title);
  if (note.content && note.content.length > 0) parts.push(note.content);
  
  let summary = parts.join(' - ').substring(0, 100);
  
  // 如果太短，用原文
  if (summary.length < 20 && note.rawText) {
    summary = note.rawText.split('\n')[0].substring(0, 100);
  }
  
  return summary;
};

// 解析单条笔记
const parseNote = (note) => {
  const text = note.text || '';
  
  // 提取标题
  const title = extractTitle(text);
  
  // 提取正文
  const content = extractContent(text);
  
  // 生成一句话总结
  const rawTextSummary = generateSummary({ title, content, rawText: text });
  
  const result = {
    noteId: note.noteId,
    title: title,
    content: content,
    rawTextSummary: rawTextSummary,
    noteType: matchNoteType(text),
    liveTime: extractLiveTime(text),
    productItems: extractProducts(text),
    isValuable: false
  };
  
  if (result.noteType === '直播预告' || result.noteType === '新品上架' || result.productItems.length > 0) {
    result.isValuable = true;
  }
  
  return result;
};

const parseNotes = (notes) => notes.map(parseNote);

module.exports = { parseNotes, parseNote };
