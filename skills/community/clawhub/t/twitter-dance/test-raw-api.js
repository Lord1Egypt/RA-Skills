require('dotenv').config();
const TwitterDanceAPIClient = require('./src/twitter-api-client');

async function test() {
  const client = new TwitterDanceAPIClient({
    authToken: process.env.TWITTER_AUTH_TOKEN,
    apiKey: process.env.APIDANCE_API_KEY,
    verbose: true
  });

  console.log('\n测试原始 API 调用...\n');
  
  try {
    console.log('调用 /v1.1/account/verify_credentials.json...\n');
    const result = await client.request('/v1.1/account/verify_credentials.json');
    
    console.log('📊 返回数据:');
    console.log(JSON.stringify(result, null, 2).substring(0, 1000));
  } catch (err) {
    console.error('❌ 错误:', err.message);
  }
}

test();
