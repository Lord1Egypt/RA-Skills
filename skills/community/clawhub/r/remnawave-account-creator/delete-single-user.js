const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

const uuidToDelete = process.argv[2];

if (!uuidToDelete) {
  console.error('用法：node delete-single-user.js <UUID>');
  process.exit(1);
}

function callApi(method, endpoint) {
  return new Promise((resolve) => {
    const apiToken = getRemnawaveToken();
    const url = new URL(endpoint, config.apiBaseUrl);
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
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, response: JSON.parse(data) }); } 
        catch(e) { resolve({ status: res.statusCode, response: data }); }
      });
    });
    req.on('error', () => resolve({ status: 0, response: 'network error' }));
    req.end();
  });
}

async function main() {
  console.log(`🗑️  准备删除账号 UUID: ${uuidToDelete}\n`);
  
  console.log('🔍 确认账号信息...');
  const info = await callApi('GET', `/api/users/${uuidToDelete}`);
  
  if (info.status !== 200 || !info.response?.uuid) {
    console.log('❌ 账号不存在或查询失败');
    process.exit(1);
  }
  
  console.log(`   用户名：${info.response.username}`);
  console.log(`   邮箱：${info.response.email || '无'}`);
  console.log(`   分组：${info.response.activeInternalSquads?.[0]?.name || '未知'}`);
  console.log();
  
  console.log('🗑️  执行删除...');
  const deleteResult = await callApi('DELETE', `/api/users/${uuidToDelete}`);
  
  if (deleteResult.status === 200) {
    console.log('✅ 删除成功!');
  } else {
    console.log(`❌ 删除失败：状态码 ${deleteResult.status}`);
    console.log(`   响应：${JSON.stringify(deleteResult.response)}`);
    process.exit(1);
  }
}

main();
