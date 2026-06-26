#!/usr/bin/env node
/**
 * 添加收藏脚本
 * 用法: node shoucang-add.js <url>
 */

const path = require('path');
const MarkdownStore = require('../lib/markdownStore');
const { Fetcher, DeepSeekLLM } = require('../lib/fetcher');
const ReviewEngine = require('../lib/reviewEngine');

// 加载配置
const configPath = path.join(__dirname, '../config.json');
let config = {};
try {
  config = require(configPath);
} catch (e) {
  console.log('注意: 未找到配置文件，使用默认配置');
}

const storagePath = config.storagePath || '~/Desktop/Obsidian/Star';
const store = new MarkdownStore(storagePath);
const fetcher = new Fetcher();
const reviewEngine = new ReviewEngine(config.review || {});

// 使用 DeepSeek LLM
const llm = new DeepSeekLLM(config.llm || {});

async function main() {
  const url = process.argv[2];

  if (!url) {
    console.log('用法: node shoucang-add.js <url>');
    process.exit(1);
  }

  console.log(`开始抓取: ${url}`);

  try {
    // 1. 抓取网页
    const fetchResult = await fetcher.fetch(url);
    console.log(`抓取完成，类型: ${fetchResult.type}`);

    // 2. 生成 AI 摘要
    let aiResult = {
      summary: [],
      tags: [],
      category: '未分类'
    };

    if (fetchResult.status === 'success' && fetchResult.content) {
      try {
        aiResult = await fetcher.generateSummary(fetchResult.content, llm);
        console.log('AI摘要生成完成');
      } catch (err) {
        console.log('AI摘要生成失败:', err.message);
      }
    }

    // 3. 保存到 Markdown
    const id = await store.create({
      url,
      title: fetchResult.title || url,
      summary: aiResult.summary,
      tags: aiResult.tags,
      category: aiResult.category,
      status: fetchResult.status === 'success' ? 'inbox' : 'needs-review'
    });

    console.log(`收藏创建成功: ${id}`);

  } catch (err) {
    console.error('错误:', err.message);
    process.exit(1);
  }
}

main();
