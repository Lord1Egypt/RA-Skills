#!/usr/bin/env node

/**
 * 闲鱼搜索技能 - CLI 入口
 * 使用方法：node cli.js "帮我找闲鱼上的 MacBook Air M1 预算 2300"
 */

const { parseSearchConfig } = require('./utils');
const { SearchConfig, generateReport } = require('./search');
const { generateFullReport } = require('./templates');

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🔍 闲鱼搜索技能');
    console.log('');
    console.log('使用方法:');
    console.log('  node cli.js "帮我找闲鱼上的 MacBook Air M1 预算 2300"');
    console.log('  node cli.js "搜索二手 iPhone 13 预算 3000 电池 85 以上"');
    console.log('');
    console.log('示例:');
    console.log('  node cli.js "闲鱼上有没有 9 成新的 PS5"');
    console.log('  node cli.js "帮我看看闲鱼相机 预算 5000 北京"');
    process.exit(0);
  }
  
  const input = args.join(' ');
  
  console.log(`🔍 解析输入：${input}\n`);
  
  // 解析配置
  const config = parseSearchConfig(input);
  
  console.log('📋 解析结果:');
  console.log(`  关键词：${config.keyword}`);
  console.log(`  预算：¥${config.budget} - ¥${config.budgetMax}`);
  console.log(`  成色：${config.condition}`);
  console.log(`  电池：≥${config.batteryMin}%`);
  console.log(`  平台：${config.platform}`);
  console.log(`  地区：${config.location || '不限'}`);
  console.log(`  信用要求：${config.requireGoodCredit ? '是' : '否'}`);
  console.log('');
  
  // 生成搜索链接
  const searchConfig = new SearchConfig(config);
  const searchUrl = searchConfig.getSearchUrl();
  
  console.log(`🔗 搜索链接：${searchUrl}`);
  console.log('');
  console.log('⚠️  由于闲鱼平台有反爬虫机制，请点击上方链接查看实时商品列表。');
  console.log('');
  console.log('💡 提示：将商品链接发给我，我可以帮你分析是否有坑！');
}

main().catch(console.error);
