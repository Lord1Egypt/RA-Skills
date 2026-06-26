#!/usr/bin/env node
/**
 * CLI 脚本: 查询草稿列表和发布状态
 */

import { createWeChatMPClient } from '../index';

async function main() {
  const args = process.argv.slice(2);
  
  const command = args[0];
  
  try {
    const client = createWeChatMPClient();
    
    if (command === 'drafts') {
      // 查询草稿列表
      const offset = parseInt(args[1] || '0');
      const count = parseInt(args[2] || '10');
      
      console.log(`📋 正在查询草稿列表 (offset: ${offset}, count: ${count})...`);
      const result = await client.article.getDraftList(offset, count);
      
      console.log(`\n✅ 共 ${result.total_count} 条草稿，当前显示 ${result.item_count} 条:\n`);
      
      for (const item of result.item) {
        const news = item.content.news_item[0];
        console.log(`📄 ${news.title}`);
        console.log(`   Media ID: ${item.media_id}`);
        console.log(`   Author: ${news.author || 'N/A'}`);
        console.log(`   Update: ${new Date(item.update_time * 1000).toLocaleString()}`);
        console.log();
      }
    } else if (command === 'status') {
      // 查询发布状态
      const publishId = args[1];
      if (!publishId) {
        console.log('用法: node query.js status <publish_id>');
        process.exit(1);
      }
      
      console.log(`🔍 正在查询发布状态: ${publishId}...`);
      const result = await client.article.getPublishStatus(publishId);
      
      const statusMap: Record<number, string> = {
        0: '✅ 成功',
        1: '⏳ 发布中',
        2: '❌ 原创审核失败',
        3: '💥 失败'
      };
      
      console.log(`\n状态: ${statusMap[result.publish_status] || '未知'}`);
      console.log(`Publish ID: ${result.publish_id}`);
      
      if (result.article_id) {
        console.log(`Article ID: ${result.article_id}`);
      }
      
      if (result.article_detail) {
        console.log(`\n文章详情:`);
        for (const detail of result.article_detail.item) {
          console.log(`  [${detail.idx}] ${detail.article_url}`);
        }
      }
      
      if (result.fail_idx && result.fail_idx.length > 0) {
        console.log(`\n失败索引: ${result.fail_idx.join(', ')}`);
      }
    } else {
      console.log('用法:');
      console.log('  node query.js drafts [offset] [count]  - 查询草稿列表');
      console.log('  node query.js status <publish_id>      - 查询发布状态');
      process.exit(1);
    }
  } catch (error: any) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
