#!/usr/bin/env node
/**
 * 小红书内容创作工具
 * 
 * 功能：
 * 1. 内容润色 - 让内容更符合小红书风格
 * 2. 标题优化 - 生成吸引人的小红书标题
 * 3. 话题标签 - 生成相关话题标签
 * 4. emoji 优化 - 添加合适的 emoji
 * 5. 图文内容生成 - 根据内容生成图片描述
 */

const { AI } = require('@ai-sdk/google');

// 小红书风格提示词
const XHS_STYLE = `你是一位资深小红书博主，请帮我优化以下内容：

要求：
1. 标题要吸引人，使用数字、夸张语气、悬念等手法
2. 标题控制在 20-25 个汉字以内，一行显示舒适
3. 正文采用小红书风格：
   - 开头用感叹号引起注意，设置场景或提出问题
   - 分段清晰，短段落，每段 2-4 行
   - 使用 emoji 增加亲和力
   - 中间给出具体建议/方法，用数字列举
   - 结尾有互动邀请或总结
4. 语气亲切自然，像朋友分享
5. 不要夸大其词，保持真诚
`;

// 优化标题的提示词
const TITLE_PROMPT = `请为以下内容生成 5 个吸引人的小红书标题，符合小红书风格：
标题特点：
- 使用数字、疑问句、夸张语气
- 控制在 20-25 字以内
- 包含 emoji 或表情符号
- 可以直接点击，吸引眼球

内容：{{content}}`;

// 生成话题标签的提示词
const HASHTAG_PROMPT = `请为以下内容生成适合小红书的标签（#话题），不超过 10 个：
内容：{{content}}

话题类型：
- 第一个标签：核心话题
- 后续标签：细分领域、场景、人群等`;

// 小红书内容优化函数
function optimizeContentForXHS(content) {
  return {
    title: generateTitles(content)[0],
    content: content,
    hashtags: generateHashtags(content),
    emojiEnhanced: contentWithEmojis(content)
  };
}

// 生成标题
function generateTitles(content) {
  const prompts = [
    `一个震惊：${content.substring(0, 50)}`,
    `5 个 ${content.split(' ')[0]} 的小技巧：${content.substring(0, 50)}`,
    `不要再 ${content.split(' ')[0]} 了！${content.substring(0, 50)}`,
    `揭秘 ${content.split(' ')[0]} 的 ${Math.floor(Math.random() * 5) + 1} 个秘诀：${content.substring(0, 50)}`,
    `${content.split(' ')[0]}新手必看：${content.substring(0, 50)}`
  ];
  
  return prompts.map(prompt => {
    // 这里可以集成 AI 模型进行优化
    return prompt + ' 🎯';
  });
}

// 生成话题标签
function generateHashtags(content) {
  const keywords = content.toLowerCase().split(/\s+/).filter(w => w.length > 3);
  return `#生活记录 #分享 # ${keywords[0] || ''} #小红书 #日常 #笔记`;
}

// 添加 emoji 优化
function contentWithEmojis(content) {
  const emojiMap = {
    '开头': '✨',
    '建议': '💡',
    '总结': '📝',
    '互动': '💬'
  };
  
  return content
    .replace(/\n{2,}/g, '$&✨') // 段落间隔
    .replace(/\n\n/g, '$&💡')  // 技巧列表
    .replace(/\n\b/g, '\n');
}

// 核心内容生成器
function generateContent(topic, style = '生活', format = '图文') {
  const topics = {
    '生活': ['日常记录', '分享', '心得', '发现', '实用'],
    '美妆': ['测评', '教程', '妆容', '护肤', '心得'],
    '美食': ['探店', '食谱', '测评', '分享', '推荐'],
    '穿搭': ['分享', '穿搭', '街拍', '种草', '推荐'],
    '科技': ['测评', '分享', '技巧', '数码', '推荐'],
    '家居': ['分享', '改造', '收纳', '好物', '推荐'],
    '旅行': ['旅行', '打卡', '攻略', '分享', '记录'],
    '学习': ['学习', '成长', '分享', '心得', '笔记'],
    '健身': ['锻炼', '分享', '打卡', '心得', '打卡'],
    '其他': ['生活', '分享', '记录', '日常', 'vlog']
  };
  
  const topicList = topics[style] || topics['其他'];
  const randomTopic = topicList[Math.floor(Math.random() * topicList.length)];
  
  return `主题：${style}\n话题：${randomTopic}\n目标风格：${format}`;
}

// 分析小红书风格
function analyzeXHSStyle(content) {
  const features = {
    'emoji_count': (content.match(/[\U0001F600-\U0001F64F\U0001F300-\U0001F6FF]/g) || []).length,
    'paragraph_count': content.split('\n\n').length,
    'has_catchy_title': true,
    'has_hashtags': true,
    'tone': content.includes('你') ? '亲切' : '专业',
    'interactivity': content.includes('互动') ? '高' : '中'
  };
  
  return features;
}

// 小红书内容评分
function scoreContent(content) {
  const score = {
    标题吸引力: 0,
    内容相关性: 0,
    emoji 使用率: 0,
    段落清晰度: 0,
    互动性: 0
  };
  
  // 这里可以扩展评分逻辑
  
  return score;
}

// 主函数
async function main() {
  console.log('📱 小红书内容创作工具 v1.0\n');
  console.log('命令参数:');
  console.log('  - 优化内容：node index.js optimize --text "你的内容"');
  console.log('  - 生成标题：node index.js titles --text "你的内容"');
  console.log('  - 生成标签：node index.js hashtags --text "你的内容"');
  console.log('  - 生成内容：node index.js generate --topic "生活" --format "图文"');
  console.log('  - 分析风格：node index.js analyze --text "你的内容"');
}

main();
