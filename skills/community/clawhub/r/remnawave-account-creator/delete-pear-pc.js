const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

// 要删除的两个 pear_pc 账号 UUID
const uuidsToDelete = [
  { uuid: '3024f8fa-e5a2-4ef8-83a6-a6750d43ceed', note: '旧版 (2026-03-10)' },
  { uuid: 'f98edff1-7979-43ca-86e5-a13a06c78e7b', note: '新版 (2026-03-17)' }
];

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

async function deleteAccount(uuid, note) {
  console.log(`🗑️  准备删除：${note}`);
  console.log(`   UUID: ${uuid}\n`);
  
  // 确认账号存在
  console.log('🔍 确认账号信息...');
  const info = await callApi('GET', `/api/users/${uuid}`);
  
  if (info.status !== 200 || !info.response?.uuid) {
    console.log('⚠️  账号不存在或查询失败 (可能已删除)');
    console.log();
    return false;
  }
  
  console.log(`   用户名：${info.response.username}`);
  console.log(`   邮箱：${info.response.email || '无'}`);
  console.log();
  
  // 执行删除
  console.log('🗑️  执行删除...');
  const deleteResult = await callApi('DELETE', `/api/users/${uuid}`);
  
  if (deleteResult.status === 200) {
    console.log('✅ 删除成功!\n');
    return true;
  } else {
    console.log(`❌ 删除失败：状态码 ${deleteResult.status}`);
    console.log(`   响应：${JSON.stringify(deleteResult.response)}\n`);
    return false;
  }
}

async function main() {
  console.log('=== 删除 pear_pc 旧账号 ===\n');
  
  let successCount = 0;
  for (const { uuid, note } of uuidsToDelete) {
    const result = await deleteAccount(uuid, note);
    if (result) successCount++;
  }
  
  console.log(`\n=== 删除完成 ===`);
  console.log(`成功：${successCount}/${uuidsToDelete.length}`);
}

main();
