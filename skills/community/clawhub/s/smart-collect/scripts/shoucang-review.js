#!/usr/bin/env node
/**
 * 复习回顾脚本
 * 用法: node shoucang-review.js
 */

const path = require('path');
const MarkdownStore = require('../lib/markdownStore');
const ReviewEngine = require('../lib/reviewEngine');
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

// 飞书通知器
class FeishuNotifier {
  constructor(config) {
    this.config = config;
  }

  async send(item) {
    // TODO: 实现飞书发送
    // 这里只打印
    console.log('=== 复习提醒 ===');
    console.log(`标题: ${item.title}`);
    console.log(`标签: ${(item.tags || []).join(', ')}`);
    console.log(`分类: ${item.category}`);
    console.log(`链接: ${item.url}`);
    console.log(`回顾次数: ${item.reviewCount || 0}`);
    console.log('================');
  }
}

const notifier = config.feishu ? new FeishuNotifier(config.feishu) : null;

async function main() {
  console.log('开始每日复习...');

  try {
    const results = await reviewEngine.runDailyReview(store, notifier);
    
    console.log(`复习完成:`);
    console.log(`  待回顾: ${results.total}`);
    console.log(`  已通知: ${results.notified}`);
    
    if (results.errors.length > 0) {
      console.log('  错误:');
      for (const err of results.errors) {
        console.log(`    - ${err.id}: ${err.error}`);
      }
    }
    
  } catch (err) {
    console.error('复习失败:', err.message);
    process.exit(1);
  }
}

main();
