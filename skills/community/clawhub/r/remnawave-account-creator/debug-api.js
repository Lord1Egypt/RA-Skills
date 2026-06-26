const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

console.log('API 配置:', config.apiBaseUrl);

function callApi(method, endpoint) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, config.apiBaseUrl);
    console.log(`\n请求：${method} ${url.href}`);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${config.apiToken}`,
        'Content-Type': 'application/json'
      },
      rejectUnauthorized: config.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        console.log(`状态码：${res.statusCode}`);
        try { 
          const json = JSON.parse(data);
          console.log(`响应：${JSON.stringify(json, null, 2).substring(0, 500)}...`);
          resolve(json);
        } catch(e) { 
          console.log(`响应（原始）: ${data.substring(0, 200)}...`);
          resolve(data);
        }
      });
    });
    req.on('error', (e) => {
      console.log(`错误：${e.message}`);
      resolve({ error: e.message });
    });
    req.end();
  });
}

async function main() {
  console.log('=== 测试 1: 列表查询 ===');
  const list = await callApi('GET', '/api/users?page=1&limit=10');
  
  console.log('\n=== 测试 2: 按用户名查询 selene ===');
  const byName = await callApi('GET', '/api/users/by-username/selene');
  
  console.log('\n=== 测试 3: 按 UUID 查询 ===');
  const byUuid = await callApi('GET', '/api/users/23a67068-3f16-4d04-ac87-ded3027aade2');
}

main();
