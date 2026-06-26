#!/usr/bin/env node
/**
 * 智能收藏入口
 * 支持自然语言管理收藏
 * 用法: node smart-collect.js "<指令>" [收藏ID]
 */

const path = require('path');
const MarkdownStore = require('../lib/markdownStore');
const ReviewEngine = require('../lib/reviewEngine');
const NLPParser = require('../lib/nlpParser');
const Fetcher = require('../lib/fetcher');

// 加载配置
const configPath = path.join(__dirname, '../config.json');
let config = {};
try {
  config = require(configPath);
} catch (e) {
  console.log('注意: 未找到配置文件');
}

const storagePath = config.storagePath || '~/Desktop/Obsidian/Star';
const store = new MarkdownStore(storagePath);
const reviewEngine = new ReviewEngine(config.review || {});
const nlpParser = new NLPParser(store, reviewEngine);
const fetcher = new Fetcher();

// LLM 接口
class SimpleLLM {
  async complete(prompt) {
    // TODO: 实现实际 LLM 调用
    return JSON.stringify({
      summary: ['测试摘要'],
      tags: ['测试'],
      category: '阅读'
    });
  }
}

const llm = new SimpleLLM();

async function main() {
  const args = process.argv.slice(2);
  
  // 帮助信息
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
智能收藏系统 - 自然语言管理

用法:
  node smart-collect.js add <url>              添加收藏
  node smart-collect.js review                 手动触发复习
  node smart-collect.js "<指令>" <收藏ID>     自然语言管理
  node smart-collect.js list                   列出所有收藏
  node smart-collect.js help                   显示帮助

自然语言指令示例:
  - 推迟3天           推迟复习
  - 已看完归档         归档收藏
  - 添加标签 AI       添加标签
  - 删除标签 xxx      删除标签
  - 已回顾            标记已回顾
`);
    return;
  }

  // 添加收藏
  if (args[0] === 'add' && args[1]) {
    const url = args[1];
    console.log(`抓取: ${url}`);
    
    try {
      const fetchResult = await fetcher.fetch(url);
      let aiResult = { summary: [], tags: [], category: '未分类' };
      
      if (fetchResult.status === 'success' && fetchResult.content) {
        aiResult = await fetcher.generateSummary(fetchResult.content, llm);
      }
      
      const id = await store.create({
        url,
        title: fetchResult.title || url,
        summary: aiResult.summary,
        tags: aiResult.tags,
        category: aiResult.category,
        status: fetchResult.status === 'success' ? 'inbox' : 'needs-review'
      });
      
      console.log(`收藏成功: ${id}`);
    } catch (err) {
      console.error('错误:', err.message);
    }
    return;
  }

  // 手动复习
  if (args[0] === 'review') {
    const Reviewer = require('./shoucang-review');
    // 调用 review 逻辑
    const results = await reviewEngine.runDailyReview(store, null);
    console.log('复习完成:', results.total);
    return;
  }

  // 列出收藏
  if (args[0] === 'list') {
    const items = await store.list();
    console.log(`共 ${items.length} 条收藏:\n`);
    for (const item of items.slice(0, 20)) {
      console.log(`[${item.id}] ${item.title}`);
      console.log(`  状态: ${item.status} | 分类: ${item.category} | 标签: ${(item.tags || []).join(', ')}`);
      console.log();
    }
    return;
  }

  // 自然语言管理
  if (args[0] && args[1]) {
    const command = args[0];
    const id = args[1];
    
    try {
      const result = await nlpParser.parse(command, id);
      console.log('执行结果:', JSON.stringify(result, null, 2));
    } catch (err) {
      console.error('错误:', err.message);
    }
    return;
  }

  console.log('用法: node smart-collect.js --help');
}

main();
