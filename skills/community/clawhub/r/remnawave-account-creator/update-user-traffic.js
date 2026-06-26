#!/usr/bin/env node

/**
 * Remnawave 用户流量重置策略更新脚本
 * 
 * 由于 Remnawave API 当前版本不支持在创建时设置流量重置策略，
 * 此脚本用于在创建账号后自动更新流量配置。
 * 
 * 用法:
 * node update-user-traffic.js \
 *   --username jim_pc \
 *   --traffic-reset WEEKLY
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, '../../config');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');

// 解析命令行参数
const args = process.argv.slice(2);
const params = {
  username: null,
  trafficReset: 'WEEKLY'
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) params.username = args[++i];
  else if (args[i] === '--traffic-reset' && args[i + 1]) params.trafficReset = args[++i];
}

if (!params.username) {
  console.error('❌ 错误：缺少必填参数 --username');
  console.error('用法：node update-user-traffic.js --username <用户名> [--traffic-reset <周期>]');
  process.exit(1);
}

function readConfig(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`❌ 读取配置文件失败：${filePath}`);
    process.exit(1);
  }
}

function callApi(method, endpoint, data = null) {
  return new Promise((resolve, reject) => {
    const remnawaveConfig = readConfig(REMNAWAVE_CONFIG);
    const url = new URL(endpoint, remnawaveConfig.apiBaseUrl);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${remnawaveConfig.apiToken}`,
        'Content-Type': 'application/json'
      },
      rejectUnauthorized: remnawaveConfig.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          resolve({ statusCode: res.statusCode, response });
        } catch (error) {
          resolve({ statusCode: res.statusCode, response: responseData });
        }
      });
    });
    
    req.on('error', reject);
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    
    req.end();
  });
}

async function updateUserTraffic() {
  console.log('🔄 更新用户流量重置策略...\n');
  
  try {
    // 1. 获取用户列表
    console.log('📡 获取用户列表...');
    const usersResponse = await callApi('GET', '/api/users');
    const users = usersResponse.response.users;
    
    const user = users.find(u => u.username === params.username);
    if (!user) {
      console.error(`❌ 找不到用户：${params.username}`);
      process.exit(1);
    }
    
    console.log(`✅ 找到用户：${user.username} (UUID: ${user.uuid})\n`);
    
    // 2. 尝试更新用户
    console.log('📡 尝试更新流量重置策略...');
    const updateData = {
      trafficResetInterval: params.trafficReset
    };
    
    // 尝试不同的 API 端点
    const endpoints = [
      `/api/users/${user.uuid}`,
      `/api/users/${user.uuid}/traffic`,
      `/api/users/${user.shortUuid}`,
      `/api/users/username/${params.username}`
    ];
    
    let success = false;
    
    for (const endpoint of endpoints) {
      try {
        console.log(`   尝试端点：${endpoint}`);
        const result = await callApi('PATCH', endpoint, updateData);
        
        if (result.statusCode === 200) {
          console.log(`✅ 更新成功！\n`);
          success = true;
          break;
        } else {
          console.log(`   ❌ 失败 (${result.statusCode})`);
        }
      } catch (error) {
        console.log(`   ❌ 错误：${error.message}`);
      }
    }
    
    if (!success) {
      console.log('\n⚠️ API 不支持直接更新流量重置策略');
      console.log('\n📋 手动配置步骤:');
      console.log('   1. 登录 Remnawave 管理后台');
      console.log(`   2. 找到用户：${params.username}`);
      console.log('   3. 点击编辑');
      console.log('   4. 设置流量重置策略为：' + params.trafficReset);
      console.log('   5. 保存');
      console.log('\n💡 或者使用浏览器开发者工具抓取更新请求，分析正确的 API 格式');
    }
    
  } catch (error) {
    console.error('❌ 更新失败:', error.message);
    process.exit(1);
  }
}

updateUserTraffic();
