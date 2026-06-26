#!/usr/bin/env node

require('dotenv').config();
const TwitterDanceEnhanced = require('../src/twitter-api-enhanced');

const client = new TwitterDanceEnhanced({
  authToken: process.env.TWITTER_AUTH_TOKEN,
  apiKey: process.env.APIDANCE_API_KEY
});

async function testNotifications() {
  try {
    console.log('\n=== 测试 getNotifications() ===\n');
    
    const result = await client.getNotifications({
      max_results: 50,
      types: 'mention,reply,like,retweet,follow'
    });

    console.log('\n📊 通知统计:');
    console.log(`  总数: ${result.summary.total}`);
    console.log(`  @提及: ${result.summary.mentions}`);
    console.log(`  回复: ${result.summary.replies}`);
    console.log(`  点赞: ${result.summary.likes}`);
    console.log(`  转发: ${result.summary.retweets}`);
    console.log(`  关注: ${result.summary.follows}`);
    
    console.log('\n📬 最近通知 (前 5 条):');
    result.notifications.slice(0, 5).forEach((notif, i) => {
      console.log(`  ${i + 1}. [${notif.type}] ${notif.text?.substring(0, 40)}...`);
    });

    if (result.pagination_token) {
      console.log(`\n🔗 分页令牌: ${result.pagination_token.substring(0, 20)}...`);
    }

    console.log(`\n✅ 数据源: ${result.source}`);
    console.log(`✅ 时间: ${result.timestamp}\n`);

  } catch (err) {
    console.error('[❌] 错误:', err.message);
    process.exit(1);
  }
}

testNotifications();
