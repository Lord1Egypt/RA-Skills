/**
 * 测试脚本 - 完整测试所有功能
 * 使用方法：node test_all.js
 */

import {
  checkLoginStatus,
  getLoginQRCode,
  deleteCookies,
  listFeeds,
  searchFeeds,
  getFeedDetail,
  likeFeed,
  favoriteFeed,
  postComment,
  userProfile,
  publishContent,
  publishWithVideo
} from './src/xhs-tools.js';

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function runTests() {
  console.log('🧪 开始测试 xhs-mcp-service 所有功能\n');
  console.log('='.repeat(60));

  // 1. 测试检查登录状态
  console.log('\n📝 1. 测试 check_login_status');
  const loginStatus = await checkLoginStatus();
  console.log('结果:', JSON.stringify(loginStatus, null, 2));

  if (!loginResult.logged_in) {
    console.log('\n⚠️ 未登录！请先运行: npm run login');
    console.log('其他功能需要登录后才能测试\n');
  }

  // 2. 测试搜索
  console.log('\n📝 2. 测试 search_feeds');
  const searchResult = await searchFeeds('美食');
  console.log(`找到 ${searchResult.feeds?.length || 0} 条结果`);
  if (searchResult.feeds?.[0]) {
    console.log('第一条:', searchResult.feeds[0].title);
  }

  // 3. 测试首页推荐
  console.log('\n📝 3. 测试 list_feeds');
  const feedsResult = await listFeeds();
  console.log(`获取到 ${feedsResult.feeds?.length || 0} 条推荐`);

  // 4. 测试详情 (如果有结果)
  if (searchResult.feeds?.[0]) {
    const firstFeed = searchResult.feeds[0];
    console.log('\n📝 4. 测试 get_feed_detail');
    const detail = await getFeedDetail(firstFeed.id, firstFeed.xsec_token);
    console.log('标题:', detail.title);
    console.log('点赞数:', detail.stats?.likes);
    console.log('评论数:', detail.stats?.comments);

    // 5. 测试点赞
    console.log('\n📝 5. 测试 like_feed');
    const likeResult = await likeFeed(firstFeed.id, firstFeed.xsec_token);
    console.log('结果:', likeResult.message);

    // 6. 测试收藏
    console.log('\n📝 6. 测试 favorite_feed');
    const favResult = await favoriteFeed(firstFeed.id, firstFeed.xsec_token);
    console.log('结果:', favResult.message);

    // 7. 测试评论
    console.log('\n📝 7. 测试 post_comment');
    const commentResult = await postComment(firstFeed.id, firstFeed.xsec_token, '很棒的分享！👍');
    console.log('结果:', commentResult.message);
  }

  // 8. 测试用户主页
  if (searchResult.feeds?.[0]?.author_id) {
    console.log('\n📝 8. 测试 user_profile');
    const profile = await userProfile(searchResult.feeds[0].author_id, searchResult.feeds[0].xsec_token);
    console.log('用户名:', profile.nickname);
    console.log('粉丝数:', profile.stats?.fans);
  }

  console.log('\n' + '='.repeat(60));
  console.log('✅ 测试完成！');
  console.log('\n📝 发布功能测试:');
  console.log('  - 发布图文: node test_publish.js');
  console.log('  - 发布视频: node test_video.js');
}

runTests().catch(e => {
  console.error('❌ 测试失败:', e.message);
  process.exit(1);
});
