require('dotenv').config();
const TwitterDanceEnhanced = require('./src/twitter-api-enhanced');

async function test() {
  const client = new TwitterDanceEnhanced({
    authToken: process.env.TWITTER_AUTH_TOKEN,
    apiKey: process.env.APIDANCE_API_KEY,
    verbose: false
  });

  try {
    console.log('测试 getMyTweets...');
    const result = await client.getMyTweets({ count: 2 });
    
    console.log('返回值类型:', typeof result);
    console.log('是否是数组:', Array.isArray(result));
    console.log('JSON:', JSON.stringify(result, null, 2).substring(0, 1000));
  } catch (err) {
    console.error('错误:', err.message);
  }
}

test();
