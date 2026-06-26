/**
 * 小红书 MCP 服务 - 基础示例
 *
 * 说明：此脚本需要在项目根目录下运行
 * 运行：node examples/01-基础示例.mjs
 */

import {
  checkLoginStatus,
  listFeeds,
  searchFeeds,
} from '../src/xhs-tools.js';
import { closeBrowser } from '../src/browser.js';

console.log('🧪 小红书MCP服务 - 基础示例\n');
console.log('💡 提示: 请在项目根目录下运行此脚本\n');

// 1. 检查登录
console.log('1. 检查登录状态...');
const loginStatus = await checkLoginStatus();
console.log('   结果:', loginStatus.message);

if (!loginStatus.logged_in) {
  console.log('\n❌ 请先登录');
  console.log('运行: npm run login');
  await closeBrowser();
  process.exit(1);
}

// 2. 获取首页推荐
console.log('\n2. 获取首页推荐...');
const feeds = await listFeeds();
console.log(`   获取到 ${feeds.feeds.length} 条推荐`);

// 显示前3条
console.log('\n   前3条推荐:');
feeds.feeds.slice(0, 3).forEach((feed, i) => {
  console.log(`   ${i + 1}. ${feed.title || '(无标题)'}`);
  console.log(`      作者: ${feed.author || '未知'}`);
  console.log(`      点赞: ${feed.like_count || 0}`);
});

// 3. 搜索笔记
console.log('\n3. 搜索笔记（关键词: 咖啡）...');
const results = await searchFeeds('咖啡');
console.log(`   搜索到 ${results.feeds.length} 条结果`);

// 显示前3条
console.log('\n   前3条搜索结果:');
results.feeds.slice(0, 3).forEach((feed, i) => {
  console.log(`   ${i + 1}. ${feed.title || '(无标题)'}`);
  console.log(`      作者: ${feed.author || '未知'}`);
});

await closeBrowser();
console.log('\n✅ 示例完成！');
console.log('\n📚 更多示例:');
console.log('   - examples/02-互动示例.mjs');
console.log('   - examples/03-发布示例.mjs');
