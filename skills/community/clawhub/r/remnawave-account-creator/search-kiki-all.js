const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(require('fs').readFileSync(CONFIG_FILE, 'utf-8'));

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
  console.log('🔍 全局搜索所有包含 "kiki" 的账号（遍历所有 84 个用户）...\n');
  
  const allUsers = [];
  let page = 1;
  
  while (true) {
    const resp = await callApi('GET', `/api/users?page=${page}&limit=100`);
    const users = resp.response?.users || [];
    const total = resp.response?.total || 0;
    
    if (users.length === 0) break;
    
    allUsers.push(...users);
    console.log(`第 ${page} 页：${users.length} 个用户 (累计：${allUsers.length}/${total})`);
    
    if (allUsers.length >= total) break;
    page++;
    
    if (page > 50) {
      console.log('⚠️  达到安全限制');
      break;
    }
  }
  
  console.log(`\n✅ 总用户数：${allUsers.length}\n`);
  
  const kikis = allUsers.filter(u => 
    u.username.toLowerCase().includes('kiki') ||
    (u.email && u.email.toLowerCase().includes('kiki'))
  );
  
  if (kikis.length === 0) {
    console.log('❌ 未找到包含 "kiki" 的账号');
  } else {
    console.log(`✅ 找到 ${kikis.length} 个包含 "kiki" 的账号:\n`);
    kikis.forEach((u, i) => {
      console.log(`${i + 1}. ${u.username}`);
      console.log(`   邮箱：${u.email || '无'}`);
      console.log(`   分组：${u.activeInternalSquads?.[0]?.name || '未知'}`);
      console.log(`   创建：${u.createdAt?.split('T')[0]}`);
      console.log();
    });
  }
}

main();
