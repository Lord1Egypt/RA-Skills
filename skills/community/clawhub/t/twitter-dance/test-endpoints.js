require('dotenv').config();
const https = require('https');

async function testEndpoint(endpoint) {
  return new Promise((resolve) => {
    const headers = {
      'apikey': process.env.APIDANCE_API_KEY,
      'authtoken': process.env.TWITTER_AUTH_TOKEN,
      'User-Agent': 'Test/1.0.0'
    };

    const url = `https://api.apidance.pro${endpoint}`;
    const urlObj = new URL(url);

    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        console.log(`  状态: ${res.statusCode}`);
        console.log(`  响应: ${data.substring(0, 100)}`);
        resolve();
      });
    });

    req.on('error', (err) => {
      console.log(`  错误: ${err.message}`);
      resolve();
    });

    req.end();
  });
}

async function test() {
  console.log('测试 apidance.pro 端点...\n');
  
  const endpoints = [
    '/v1.1/account/verify_credentials.json',
    '/v1.1/statuses/update.json?status=test',
    '/health',
    '/2/tweets/search/recent'
  ];

  for (const endpoint of endpoints) {
    console.log(`📍 ${endpoint}`);
    await testEndpoint(endpoint);
    console.log();
  }
}

test();
