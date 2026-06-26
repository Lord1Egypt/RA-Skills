const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

function callApi(method, endpoint) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, config.apiBaseUrl);
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
        try { resolve(JSON.parse(data)); } catch(e) { resolve(data); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function main() {
  console.log('🔍 获取所有用户并筛选 selene...\n');
  const resp = await callApi('GET', '/api/users?page=1&limit=500');
  const users = resp.response.users || [];
  
  const seleneUsers = users.filter(u => u.username.includes('selene') || u.email.includes('selene'));
  
  console.log(`找到 ${seleneUsers.length} 个用户:\n`);
  seleneUsers.forEach(u => {
    console.log(`用户名：${u.username}`);
    console.log(`邮箱：${u.email || '无'}`);
    console.log(`UUID: ${u.uuid}`);
    console.log(`分组：${u.activeInternalSquads?.[0]?.name || '未知'}`);
    console.log(`状态：${u.status}`);
    console.log('---');
  });
}

main();
