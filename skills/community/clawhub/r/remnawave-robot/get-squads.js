#!/usr/bin/env node

/**
 * Remnawave Robot - 查询用户分组
 * 
 * 用法:
 * node get-squads.js --username <用户名>
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, 'config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');

function getRemnawaveToken() {
  const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
  const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
  return match ? match[1].trim() : null;
}

function readConfig(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function callApi(method, endpoint) {
  return new Promise((resolve) => {
    const config = readConfig(REMNAWAVE_CONFIG);
    const token = getRemnawaveToken();
    const url = new URL(endpoint, config.apiBaseUrl);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
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
  const args = process.argv.slice(2);
  let username = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--username' && args[i + 1]) username = args[++i];
  }
  
  if (!username) {
    console.error('用法：node get-squads.js --username <用户名>');
    process.exit(1);
  }
  
  console.log(`🔍 查询用户：${username}\n`);
  
  const resp = await callApi('GET', `/api/users/by-username/${username}`);
  const user = resp.response?.response || resp.response;
  
  if (!user || !user.uuid) {
    console.log('❌ 用户不存在');
    return;
  }
  
  console.log(`✅ 找到用户：${user.username}`);
  console.log(`   UUID: ${user.uuid}`);
  console.log(`   订阅地址：${user.subscriptionUrl}`);
  console.log();
  
  if (user.activeInternalSquads && user.activeInternalSquads.length > 0) {
    console.log(`📋 当前分组 (${user.activeInternalSquads.length} 个):`);
    user.activeInternalSquads.forEach((squad, i) => {
      console.log(`   ${i + 1}. ${squad.name} (${squad.uuid})`);
    });
  } else {
    console.log('⚠️  用户未分配任何分组');
  }
}

main();
