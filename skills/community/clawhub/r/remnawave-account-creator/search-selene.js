const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

function callApi(method, endpoint) {
  return new Promise((resolve) => {
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
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch(e) { resolve({}); }
      });
    });
    req.on('error', () => resolve({}));
    req.end();
  });
}

async function main() {
  console.log('🔍 全面搜索所有包含 "selene" 的账号...\n');
  
  const allUsers = [];
  let page = 1;
  
  // 遍历所有用户
  while (true) {
    const resp = await callApi('GET', `/api/users?page=${page}&limit=500`);
    const users = resp.response?.users || [];
    if (users.length === 0) break;
    allUsers.push(...users);
    console.log(`第 ${page} 页：${users.length} 个用户`);
    if (users.length < 500) break;
    page++;
  }
  
  console.log(`\n总用户数：${allUsers.length}`);
  
  // 筛选 selene
  const seleneFromList = allUsers.filter(u => 
    u.username.toLowerCase().includes('selene') ||
    (u.email && u.email.toLowerCase().includes('selene'))
  );
  
  // 直接查询 selene 用户名
  const directQuery = await callApi('GET', '/api/users/by-username/selene');
  
  // 合并结果（去重）
  const allSelene = new Map();
  seleneFromList.forEach(u => allSelene.set(u.uuid, u));
  if (directQuery.response?.uuid) {
    allSelene.set(directQuery.response.uuid, directQuery.response);
  }
  
  console.log(`\n✅ 找到 ${allSelene.size} 个包含 "selene" 的账号:\n`);
  
  let i = 1;
  for (const u of allSelene.values()) {
    console.log(`${i++}. ${u.username}`);
    console.log(`   UUID: ${u.uuid}`);
    console.log(`   邮箱：${u.email || '无'}`);
    console.log(`   分组：${u.activeInternalSquads?.[0]?.name || '未知'}`);
    console.log(`   状态：${u.status}`);
    console.log(`   流量：${Math.round(u.trafficLimitBytes / (1024*1024*1024))}GB (${u.trafficLimitStrategy})`);
    console.log(`   过期：${u.expireAt?.split('T')[0]}`);
    console.log(`   创建：${u.createdAt?.split('T')[0]}`);
    console.log();
  }
}

main();
