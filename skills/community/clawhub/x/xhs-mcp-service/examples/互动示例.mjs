// 示例2: 互动操作
import { searchFeeds, likeFeed, favoriteFeed } from '../src/xhs-tools.js';
import { closeBrowser } from '../src/browser.js';

console.log('🧪 小红书MCP服务 - 互动示例\n');

// 搜索一条笔记用于测试
console.log('搜索测试笔记...');
const results = await searchFeeds('美食', { sort_by: '最新' });

if (!results.success || results.feeds.length === 0) {
  console.log('❌ 未找到测试笔记');
  await closeBrowser();
  process.exit(1);
}

const testFeed = results.feeds[0];
console.log(`\n测试笔记: ${testFeed.title}`);
console.log(`作者: ${testFeed.author}\n`);

// 点赞
console.log('1. 点赞笔记...');
const likeResult = await likeFeed(testFeed.id, testFeed.xsec_token);
if (likeResult.success) {
  console.log('   ✅ 点赞成功');
} else {
  console.log('   ❌ 点赞失败:', likeResult.message);
}

await new Promise((r) => setTimeout(r, 2000));

// 收藏
console.log('\n2. 收藏笔记...');
const favResult = await favoriteFeed(testFeed.id, testFeed.xsec_token);
if (favResult.success) {
  console.log('   ✅ 收藏成功');
} else {
  console.log('   ❌ 收藏失败:', favResult.message);
}

await new Promise((r) => setTimeout(r, 2000));

// 取消点赞
console.log('\n3. 取消点赞...');
const unlikeResult = await likeFeed(testFeed.id, testFeed.xsec_token, true);
if (unlikeResult.success) {
  console.log('   ✅ 取消点赞成功');
}

await new Promise((r) => setTimeout(r, 2000));

// 取消收藏
console.log('\n4. 取消收藏...');
const unfavResult = await favoriteFeed(testFeed.id, testFeed.xsec_token, true);
if (unfavResult.success) {
  console.log('   ✅ 取消收藏成功');
}

await closeBrowser();
console.log('\n✅ 互动示例完成！');
