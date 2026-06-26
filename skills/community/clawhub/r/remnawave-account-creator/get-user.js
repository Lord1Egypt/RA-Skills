const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

const uuid = '23a67068-3f16-4d04-ac87-ded3027aade2';

function callApi(method, endpoint) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, config.apiBaseUrl);
    
    const apiToken = getRemnawaveToken();
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${apiToken}`,
        'Content-Type': 'application/json'
      },
      rejectUnauthorized: config.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          resolve({ status: res.statusCode, response });
        } catch (error) {
          resolve({ status: res.statusCode, response: responseData });
        }
      });
    });
    
    req.on('error', (e) => resolve({ status: 0, response: e.message }));
    req.end();
  });
}

async function main() {
  console.log(`🔍 直接查询 UUID: ${uuid}\n`);
  
  // 尝试直接通过 UUID 查询
  const result = await callApi('GET', `/api/users/${uuid}`);
  
  console.log(`状态码：${result.status}`);
  console.log(`响应：${JSON.stringify(result.response, null, 2)}`);
}

main();
