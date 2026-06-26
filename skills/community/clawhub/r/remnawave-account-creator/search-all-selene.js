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
        try { resolve({ status: res.statusCode, response: JSON.parse(data) }); } 
        catch(e) { resolve({ status: res.statusCode, response: data }); }
      });
    });
    req.on('error', () => resolve({ status: 0, response: 'network error' }));
    req.end();
  });
}

async function main() {
  console.log('🔍 全面搜索所有包含 "selene" 的账号...\n');
  
  const results = new Map();
  
  // 方法 1: 列表查询（遍历所有用户）
  console.log('📋 方法 1: 遍历用户列表...');
  let page = 1, hasMore = true;
  while (hasMore) {
    const resp = await callApi('GET', `/api/users?page=${page}&limit=500`);
    const users = resp.response?.users || [];
    users.forEach(u => results.set(u.uuid, u));
    hasMore = users.length === 500;
    page++;
    if (page > 20) break;
  }
  console.log(`   列表查询到 ${results.size} 个用户`);
  
  // 方法 2: 直接按用户名查询 selene
  console.log('📋 方法 2: 直接查询用户名 selene...');
  const byUsername = await callApi('GET', '/api/users/by-username/selene');
  if (byUsername.status === 200 && byUsername.response?.uuid) {
    results.set(byUsername.response.uuid, byUsername.response);
    console.log(`   ✅ 找到 selene (UUID: ${byUsername.response.uuid})`);
  } else {
    console.log(`   ❌ 未找到`);
  }
  
  // 筛选包含 selene 的账号
  const seleneUsers = Array.from(results.values()).filter(u => 
    u.username.toLowerCase().includes('selene') ||
    (u.email && u.email.toLowerCase().includes('selene'))
  );
  
  console.log(`\n✅ 找到 ${seleneUsers.length} 个包含 "selene" 的账号:\n`);
  console.log('='.repeat(100));
  
  seleneUsers.forEach((u, i) => {
    console.log(`${i + 1}. ${u.username}`);
    console.log(`   UUID: ${u.uuid}`);
    console.log(`   邮箱：${u.email || '无'}`);
    console.log(`   分组：${u.activeInternalSquads?.[0]?.name || '未知'}`);
    console.log(`   状态：${u.status}`);
    console.log(`   流量：${Math.round(u.trafficLimitBytes / (1024*1024*1024))}GB (${u.trafficLimitStrategy})`);
    console.log(`   过期：${u.expireAt?.split('T')[0] || '未知'}`);
    console.log(`   创建：${u.createdAt?.split('T')[0] || '未知'}`);
    console.log(`   订阅：${u.subscriptionUrl}`);
    console.log('─'.repeat(100));
  });
}

main();
