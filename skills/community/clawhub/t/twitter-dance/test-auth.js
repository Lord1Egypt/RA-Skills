require('dotenv').config();
const TwitterDanceEnhanced = require('./src/twitter-api-enhanced');

async function test() {
  const client = new TwitterDanceEnhanced({
    authToken: process.env.TWITTER_AUTH_TOKEN,
    apiKey: process.env.APIDANCE_API_KEY,
    verbose: false
  });

  console.log('测试认证和账户信息...\n');
  
  try {
    console.log('1️⃣ 获取账户统计信息...');
    const stats = await client.getAccountStats();
    
    if (stats && stats.success) {
      console.log('✅ 成功！');
      console.log(`  账户: @${stats.account.handle}`);
      console.log(`  粉丝: ${stats.stats.followers}`);
      console.log(`  推文: ${stats.stats.tweets}`);
      console.log(`  点赞: ${stats.stats.likes}\n`);

      // 获取最近推文
      if (stats.stats.tweets > 0) {
        console.log('2️⃣ 获取最近推文信息...');
        // 这里可以添加逻辑来获取最近推文的ID
      }
    } else {
      console.log('❌ 获取统计失败:', JSON.stringify(stats, null, 2));
    }
  } catch (err) {
    console.error('❌ 错误:', err.message);
  }
}

test();
