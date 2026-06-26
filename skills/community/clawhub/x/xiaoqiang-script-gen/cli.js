#!/usr/bin/env node
/**
 * video-script-generator CLI
 * AI-powered short video script generator
 * 
 * Usage:
 *   node cli.js "topic" --style 实用 --platform 抖音
 *   node cli.js titles "topic"
 *   node cli.js hook "topic" --duration 15
 *   node cli.js hashtags "topic"
 */

const { spawn } = require('child_process');

// Simple template-based generator (no external API needed)
const TEMPLATES = {
  titles: {
    实用: [
      '{keyword}必须知道的{number}件事',
      '99%的人都忽略了{keyword}的{aspect}',
      '为什么你{action}却{result}？',
      '教你{number}招搞定{keyword}',
      '{keyword}的{number}个技巧，看完就懂了',
      '别人不会告诉你的{keyword}秘密',
      '{keyword}指南|新手必看',
      '这个{keyword}方法，简单又有效',
    ],
    搞笑: [
      '{keyword}翻车现场，笑死我了',
      '当我尝试{keyword}，结果...',
      '{keyword}能有什么坏心思？',
      '室友非要跟我比{keyword}，结果...',
      '以为{keyword}很简单，直到...',
    ],
    情感: [
      '致{keyword}的你',
      '{keyword}，有多爱你就有多心痛',
      '如果{keyword}可以重来',
      '最好的{keyword}是什么样的',
      '感谢{keyword}教会我的事',
    ],
    知识: [
      '{keyword}深度解析',
      '{keyword}原理揭秘',
      '5分钟看懂{keyword}',
      '{keyword}入门指南',
      '从零了解{keyword}',
    ],
  },
  hooks: {
    15: [
      '你知道吗？{keyword}其实很简单',
      '今天教你{number}招搞定{keyword}',
      '{keyword}的真相，90%人都不知道',
      '花3分钟，彻底搞懂{keyword}',
    ],
    30: [
      '我发现了一个{keyword}的秘密...',
      '身边很多人都在问{keyword}，今天统一解答',
      '关于{keyword}，你一定不知道的{number}件事',
      '做对了{keyword}，真的可以改变很多',
    ],
    60: [
      '最近很多人问我{keyword}的问题，今天用5分钟彻底讲清楚',
      '从入门到精通，今天把{keyword}说透',
      '这期内容很干，建议先收藏再看',
    ],
  },
  comments: [
    '你也遇到过这种情况吗？评论区聊聊',
    '踩过这个坑的点个赞',
    '关注我，每天分享干货',
    '觉得有用就转发给需要的人',
    '你还有什么问题？评论区问我',
    '同意的点个赞',
    '这个话题太真实了',
  ],
  hashtagTemplate: {
    抖音: ['#{keyword}', '#{keyword}技巧', '#{keyword}干货', '#职场', '#成长', '#自我提升', '#干货分享', '#知识分享'],
    快手: ['#{keyword}', '#{keyword}教程', '#每天学习', '#知识'],
    视频号: ['#{keyword}', '#{keyword}分享', '#干货'],
    'B站': ['#{keyword}', '#{keyword}解说', '#知识分享', '#教程'],
  },
};

const ASPECTS = ['底层逻辑', '核心要点', '关键细节', '本质', '核心', '精髓'];
const ACTIONS = ['努力', '坚持', '学习', '工作', '沟通'];
const RESULTS = ['没效果', '被忽视', '不成功', '白费功夫', '原地踏步'];

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function fillTemplate(template, vars) {
  return template
    .replace(/{keyword}/g, vars.keyword)
    .replace(/{number}/g, vars.number || pickRandom(['1', '2', '3', '5', '10']))
    .replace(/{aspect}/g, pickRandom(ASPECTS))
    .replace(/{action}/g, pickRandom(ACTIONS))
    .replace(/{result}/g, pickRandom(RESULTS));
}

function generateTitles(keyword, style = '实用') {
  const templates = TEMPLATES.titles[style] || TEMPLATES.titles.实用;
  const titles = [];
  for (let i = 0; i < 5; i++) {
    titles.push(fillTemplate(pickRandom(templates), { keyword, number: pickRandom(['1', '2', '3', '5']) }));
  }
  return titles;
}

function generateHook(keyword, duration = 30, style = '实用') {
  const key = String(duration);
  const templates = TEMPLATES.hooks[key] || TEMPLATES.hooks['30'];
  return fillTemplate(pickRandom(templates), { keyword, number: pickRandom(['1', '2', '3', '5']) });
}

function generateComments(keyword) {
  const comments = [];
  for (let i = 0; i < 4; i++) {
    comments.push(fillTemplate(pickRandom(TEMPLATES.comments), { keyword }));
  }
  return comments;
}

function generateHashtags(keyword, platform = '抖音') {
  const templates = TEMPLATES.hashtagTemplate[platform] || TEMPLATES.hashtagTemplate.抖音;
  const tags = templates.map(t => t.replace(/{keyword}/g, keyword));
  return [...new Set(tags)].slice(0, 10);
}

function formatOutput(keyword, options = {}) {
  const { style = '实用', platform = '抖音', duration = 30, json = false } = options;
  
  const titles = generateTitles(keyword, style);
  const hook = generateHook(keyword, duration, style);
  const comments = generateComments(keyword);
  const hashtags = generateHashtags(keyword, platform);
  
  if (json) {
    return JSON.stringify({ titles, hook, comments, hashtags, keyword, style, platform }, null, 2);
  }
  
  const lines = [];
  lines.push(`\n🎬 视频主题：${keyword}`);
  lines.push('\n📌 爆款标题（5条）');
  titles.forEach((t, i) => lines.push(`${i + 1}. ${t}`));
  
  lines.push(`\n🎙️ 开头话术（${duration}秒）`);
  lines.push(`"${hook}"`);
  
  lines.push('\n💬 评论区互动话术');
  comments.forEach(c => lines.push(`- ${c}`));
  
  lines.push('\n#标签');
  lines.push(hashtags.join(' '));
  
  return lines.join('\n');
}

// CLI parsing
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage:');
  console.log('  video-script "topic" [options]');
  console.log('  video-script titles "topic"');
  console.log('  video-script hook "topic" --duration 30');
  console.log('  video-script hashtags "topic"');
  console.log('\nOptions:');
  console.log('  --style <实用|搞笑|情感|知识>  (default: 实用)');
  console.log('  --platform <抖音|快手|视频号|B站>  (default: 抖音)');
  console.log('  --duration <15|30|60>  (default: 30)');
  console.log('  --json  Output as JSON');
  process.exit(0);
}

const command = args[0];
let topic = '';
let options = { style: '实用', platform: '抖音', duration: 30, json: false };

if (command === 'titles') {
  topic = args[1] || '';
  if (!topic) { console.error('Error: topic required'); process.exit(1); }
  console.log(generateTitles(topic).map((t, i) => `${i + 1}. ${t}`).join('\n'));
} else if (command === 'hook') {
  topic = args[1] || '';
  if (!topic) { console.error('Error: topic required'); process.exit(1); }
  args.slice(2).forEach((a, i, arr) => {
    if (a === '--duration' && arr[i + 1]) options.duration = parseInt(arr[i + 1]);
  });
  console.log(`"${generateHook(topic, options.duration)}"`);
} else if (command === 'hashtags') {
  topic = args[1] || '';
  if (!topic) { console.error('Error: topic required'); process.exit(1); }
  args.slice(2).forEach((a, i, arr) => {
    if (a === '--platform' && arr[i + 1]) options.platform = arr[i + 1];
  });
  console.log(generateHashtags(topic, options.platform).join(' '));
} else if (command === 'comments') {
  topic = args[1] || '';
  if (!topic) { console.error('Error: topic required'); process.exit(1); }
  console.log(generateComments(topic).map((c, i) => `- ${c}`).join('\n'));
} else {
  // Full generation
  topic = command;
  args.slice(1).forEach((a, i, arr) => {
    if (a === '--style' && arr[i + 1]) options.style = arr[i + 1];
    if (a === '--platform' && arr[i + 1]) options.platform = arr[i + 1];
    if (a === '--duration' && arr[i + 1]) options.duration = parseInt(arr[i + 1]);
    if (a === '--json') options.json = true;
  });
  console.log(formatOutput(topic, options));
}
