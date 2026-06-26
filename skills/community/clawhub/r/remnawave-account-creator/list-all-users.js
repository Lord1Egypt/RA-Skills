const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

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
  console.log('🔍 遍历所有用户查找 selene...\n');
  
  let allUsers = [];
  let page = 0;  // Remnawave 使用 0-based 页码
  let hasMore = true;
  
  while (hasMore) {
    const resp = await callApi('GET', `/api/users?page=${page}&size=200`);
    const users = resp.response.users || [];
    allUsers = allUsers.concat(users);
    console.log(`第 ${page} 页：${users.length} 个用户`);
    hasMore = users.length === 200;  // 每页 200 个
    page++;
    if (page > 20) break;
  }
  
  console.log(`\n总用户数：${allUsers.length}`);
  
  const seleneUsers = allUsers.filter(u => u.username.includes('selene') || u.email.includes('selene'));
  console.log(`\n包含 selene 的用户：${seleneUsers.length}\n`);
  
  seleneUsers.forEach(u => {
    console.log(`用户名：${u.username} | 邮箱：${u.email || '无'} | 分组：${u.activeInternalSquads?.[0]?.name || '未知'}`);
  });
}

main();
