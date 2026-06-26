#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

const searchTerm = process.argv[2] || '';

if (!searchTerm) {
  console.error('用法：node search-users.js <搜索关键词>');
  process.exit(1);
}

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
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API 错误：${res.statusCode}`));
          }
        } catch (error) {
          reject(new Error(`解析响应失败：${responseData}`));
        }
      });
    });
    
    req.on('error', reject);
    req.end();
  });
}

async function getAllUsers() {
  let allUsers = [];
  let page = 1;
  let hasMore = true;
  
  while (hasMore) {
    const response = await callApi('GET', `/api/users?page=${page}&limit=500`);
    const users = response.response.users || [];
    allUsers = allUsers.concat(users);
    hasMore = users.length === 500;
    page++;
    
    if (page > 20) {
      console.warn('⚠️  达到最大分页数 (20 页)');
      break;
    }
  }
  
  return allUsers;
}

async function searchUsers() {
  console.log(`🔍 全面搜索包含 "${searchTerm}" 的用户（用户名/邮箱/UUID）...\n`);
  
  const allUsers = await getAllUsers();
  const matchedUsers = allUsers.filter(u => 
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.uuid.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.shortUuid.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  if (matchedUsers.length === 0) {
    console.log('❌ 未找到匹配的用户');
    return;
  }
  
  console.log(`✅ 找到 ${matchedUsers.length} 个匹配的用户:\n`);
  console.log('| 用户名 | 邮箱 | UUID | 内部分组 | 状态 |');
  console.log('|--------|------|------|----------|------|');
  
  matchedUsers.forEach(user => {
    const squad = user.activeInternalSquads?.[0]?.name || 'Default-Squad';
    const status = user.status || 'UNKNOWN';
    
    console.log(`| ${user.username} | ${user.email} | ${user.uuid} | ${squad} | ${status} |`);
  });
}

searchUsers();
