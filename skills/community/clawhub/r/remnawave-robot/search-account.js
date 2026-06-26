#!/usr/bin/env node

/**
 * Remnawave Robot - 搜索账号
 * 
 * 用法:
 * node search-account.js <关键词>
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

async function searchUsers(keyword) {
  const resp = await callApi('GET', `/api/users?search=${keyword}&size=500`);
  return resp.response?.response?.users || resp.response?.users || [];
}

async function main() {
  const keyword = process.argv[2];
  
  if (!keyword) {
    console.error('用法：node search-account.js <关键词>');
    process.exit(1);
  }
  
  console.log(`🔍 搜索关键词：${keyword}\n`);
  
  const users = await searchUsers(keyword);
  
  if (users.length === 0) {
    console.log('❌ 未找到匹配的账号');
    return;
  }
  
  console.log(`📊 找到 ${users.length} 个账号:\n`);
  console.log('='.repeat(90));
  
  users.forEach((user, i) => {
    console.log(`${i + 1}. ${user.username}`);
    console.log(`   UUID: ${user.uuid}`);
    console.log(`   短 UUID: ${user.shortUuid}`);
    console.log(`   邮箱：${user.email || '无'}`);
    console.log(`   状态：${user.status}`);
    console.log(`   订阅：${user.subscriptionUrl}`);
    console.log(`   分组：${user.activeInternalSquads?.map(s => s.name).join(', ') || '无'}`);
    console.log(`   设备限制：${user.hwidDeviceLimit || 1} 台`);
    console.log(`   流量：${(user.trafficLimitBytes / 1073741824).toFixed(0)}GB`);
    console.log(`   过期：${user.expireAt?.split('T')[0]}`);
    console.log('─'.repeat(90));
  });
}

main();
