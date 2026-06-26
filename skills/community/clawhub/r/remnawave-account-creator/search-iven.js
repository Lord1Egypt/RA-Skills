const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

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
        try { resolve(JSON.parse(data)); } catch(e) { resolve({ raw: data }); }
      });
    });
    req.on('error', () => resolve({ error: 'network error' }));
    req.end();
  });
}

async function main() {
  console.log('🔍 搜索所有包含 "Iven" 的账号...\n');
  
  // 遍历所有用户
  const allUsers = [];
  let page = 1;
  
  while (true) {
    const resp = await callApi('GET', `/api/users?page=${page}&limit=500`);
    const users = resp.response?.users || [];
    if (users.length === 0) break;
    allUsers.push(...users);
    if (users.length < 500) break;
    page++;
  }
  
  console.log(`总用户数：${allUsers.length}\n`);
  
  // 筛选 Iven
  const ivens = allUsers.filter(u => 
    u.username.toLowerCase().includes('iven') ||
    (u.email && u.email.toLowerCase().includes('iven'))
  );
  
  if (ivens.length === 0) {
    console.log('❌ 未找到包含 "Iven" 的账号');
    return;
  }
  
  console.log(`✅ 找到 ${ivens.length} 个包含 "Iven" 的账号:\n`);
  console.log('='.repeat(100));
  
  ivens.forEach((u, i) => {
    console.log(`${i + 1}. ${u.username}`);
    console.log(`   UUID: ${u.uuid}`);
    console.log(`   邮箱：${u.email || '无'}`);
    console.log(`   分组：${u.activeInternalSquads?.[0]?.name || '未知'}`);
    console.log(`   状态：${u.status}`);
    console.log(`   流量：${Math.round(u.trafficLimitBytes / (1024*1024*1024))}GB (${u.trafficLimitStrategy})`);
    console.log(`   过期：${u.expireAt?.split('T')[0]}`);
    console.log(`   创建：${u.createdAt?.split('T')[0]}`);
    console.log('─'.repeat(100));
  });
}

main();
