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
        try { resolve(JSON.parse(data)); } 
        catch(e) { resolve({ raw: data }); }
      });
    });
    req.on('error', () => resolve({ error: 'network error' }));
    req.end();
  });
}

async function main() {
  console.log('🔍 获取所有内部分组...\n');
  
  const resp = await callApi('GET', '/api/internal-squads');
  
  if (!resp.response?.internalSquads) {
    console.log('❌ 响应格式异常:', JSON.stringify(resp).substring(0, 200));
    return;
  }
  
  const squads = resp.response.internalSquads;
  
  if (squads.length === 0) {
    console.log('❌ 未找到任何分组');
    return;
  }
  
  console.log(`✅ 找到 ${squads.length} 个内部分组:\n`);
  console.log('='.repeat(90));
  
  squads.sort((a, b) => a.viewPosition - b.viewPosition);
  
  squads.forEach((squad, i) => {
    console.log(`${i + 1}. ${squad.name.trim()}`);
    console.log(`   UUID: ${squad.uuid}`);
    console.log(`   成员数：${squad.info?.membersCount || 0}`);
    console.log(`   入站数：${squad.info?.inboundsCount || 0}`);
    console.log(`   创建时间：${squad.createdAt?.split('T')[0]}`);
    console.log('─'.repeat(90));
  });
  
  console.log('\n📊 分组摘要:\n');
  console.log('| # | 分组名称 | 成员数 | 入站数 | 创建时间 |');
  console.log('|---|----------|--------|--------|----------|');
  
  squads.forEach((squad, i) => {
    const name = squad.name.trim().substring(0, 20).padEnd(20);
    const members = String(squad.info?.membersCount || 0).padStart(6);
    const inbounds = String(squad.info?.inboundsCount || 0).padStart(6);
    const created = squad.createdAt?.split('T')[0] || '未知';
    console.log(`| ${String(i + 1).padEnd(2)} | ${name} | ${members} | ${inbounds} | ${created} |`);
  });
}

main();
