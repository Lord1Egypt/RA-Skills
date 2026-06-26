#!/usr/bin/env node
/**
 * map_stocks.js - 全球 AI 新闻 → A 股候选标的映射
 *
 * 根据全球 AI 新闻关键词，只输出 A 股候选池。
 * 适合中国用户场景，减少 token 消耗，避免输出美股。
 *
 * 用法:
 *   echo '{"articles":[...]}' | node map_stocks.js
 *   node map_stocks.js --keywords "NVIDIA,算力,光模块"
 */

// ── 概念→A 股映射表 ────────────────────────────────────────────────
const MAPPING = {
  'nvidia|nvda|gpu|cuda|芯片|算力|ai chip|semiconductor': [
    { name: '寒武纪', code: '688256', sector: 'AI芯片', reason: '国产 AI 芯片映射' },
    { name: '海光信息', code: '688041', sector: 'AI芯片', reason: '国产 GPU/DCU 映射' },
    { name: '中科曙光', code: '603019', sector: 'AI服务器', reason: '算力基础设施' },
    { name: '浪潮信息', code: '000977', sector: 'AI服务器', reason: 'AI 服务器龙头' },
  ],
  '光模块|800g|1.6t|数据中心|datacenter|data center|switch|network': [
    { name: '中际旭创', code: '300308', sector: '光模块', reason: '高速光模块龙头' },
    { name: '新易盛', code: '300502', sector: '光模块', reason: '光模块核心标的' },
    { name: '天孚通信', code: '300394', sector: '光模块', reason: '光器件上游' },
  ],
  'openai|chatgpt|gpt|sora|大模型|llm|agent|anthropic|claude': [
    { name: '科大讯飞', code: '002230', sector: '大模型', reason: '国内通用大模型代表' },
    { name: '昆仑万维', code: '300418', sector: '大模型', reason: '天工大模型/海外布局' },
    { name: '金山办公', code: '688111', sector: 'AI应用', reason: '办公 AI 落地' },
    { name: '三六零', code: '601360', sector: 'AI应用', reason: '搜索+AI 安全应用' },
  ],
  'google|gemini|alphabet|deepmind|search': [
    { name: '科大讯飞', code: '002230', sector: '大模型', reason: '国内对标大模型' },
    { name: '三六零', code: '601360', sector: 'AI应用', reason: '搜索+AI 方向' },
    { name: '昆仑万维', code: '300418', sector: '大模型', reason: '海外模型生态映射' },
  ],
  'meta|llama|开源模型|mistral|deepseek|开源': [
    { name: '昆仑万维', code: '300418', sector: '大模型', reason: '开源模型生态映射' },
    { name: '科大讯飞', code: '002230', sector: '大模型', reason: '国内模型对标' },
    { name: '金山办公', code: '688111', sector: 'AI应用', reason: 'AI 应用落地' },
  ],
  'adobe|创意|视频生成|文生视频|图像生成|midjourney|firefly|design': [
    { name: '万兴科技', code: '300624', sector: 'AI应用', reason: 'AI 视频/创意工具' },
    { name: '昆仑万维', code: '300418', sector: '大模型', reason: '多模态/海外应用布局' },
    { name: '金山办公', code: '688111', sector: 'AI应用', reason: '办公创作工具映射' },
  ],
  '机器人|robot|optimus|humanoid|具身智能|tesla': [
    { name: '拓普集团', code: '601689', sector: '机器人', reason: '机器人零部件' },
    { name: '三花智控', code: '002050', sector: '机器人', reason: '执行器/热管理' },
    { name: '绿的谐波', code: '688017', sector: '机器人', reason: '谐波减速器' },
    { name: '汇川技术', code: '300124', sector: '机器人', reason: '伺服系统' },
  ],
  '自动驾驶|fsd|autonomous|self-driving|adas|智能驾驶': [
    { name: '德赛西威', code: '002920', sector: '自动驾驶', reason: '智驾域控核心' },
    { name: '中科创达', code: '300496', sector: '自动驾驶', reason: '智能座舱/OS' },
    { name: '经纬恒润', code: '688326', sector: '自动驾驶', reason: '自动驾驶解决方案' },
  ],
};

function matchStocks(text) {
  const lower = text.toLowerCase();
  const cnMap = new Map();

  for (const [pattern, stocks] of Object.entries(MAPPING)) {
    const keywords = pattern.split('|');
    const matched = keywords.some(kw => lower.includes(kw));
    if (!matched) continue;

    for (const s of stocks) {
      if (!cnMap.has(s.code)) cnMap.set(s.code, s);
    }
  }

  // 转为数组，并按板块排序
  const all = [...cnMap.values()];
  all.sort((a, b) => a.sector.localeCompare(b.sector, 'zh-CN'));
  return all;
}

function main() {
  const args = process.argv.slice(2);

  let text = '';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--keywords' || args[i] === '-k') {
      text = args[++i] || '';
    }
  }

  if (!text) {
    try {
      const fs = require('fs');
      const input = fs.readFileSync(0, 'utf-8');
      const data = JSON.parse(input);
      if (data.articles) {
        text = data.articles.map(a => `${a.title} ${a.summary || ''}`).join(' ');
      } else {
        text = input;
      }
    } catch {
      console.error('Usage: node map_stocks.js --keywords "NVIDIA,算力" OR pipe JSON from fetch_news.js');
      process.exit(2);
    }
  }

  const result = matchStocks(text);
  console.error(`[Stock Mapper] Matched: ${result.length} A-share stocks`);
  process.stdout.write(JSON.stringify({ a_shares: result }, null, 2) + '\n');
}

main();
