#!/usr/bin/env node

/**
 * 验证 Remnawave 用户配置
 * 
 * 用法：node verify-user-config.js --username jim_pc
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, '../../config');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');

// 解析命令行参数
const args = process.argv.slice(2);
let username = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) username = args[++i];
}

if (!username) {
  console.error('❌ 错误：缺少必填参数 --username');
  console.error('用法：node verify-user-config.js --username <用户名>');
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

function callApi(method, endpoint) {
  return new Promise((resolve, reject) => {
    const remnawaveConfig = readConfig(REMNAWAVE_CONFIG);
    const url = new URL(endpoint, remnawaveConfig.apiBaseUrl);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${remnawaveConfig.apiToken}`
      },
      rejectUnauthorized: remnawaveConfig.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          resolve(response);
        } catch (error) {
          reject(new Error('解析响应失败'));
        }
      });
    });
    
    req.on('error', reject);
    req.end();
  });
}

async function verifyUserConfig() {
  console.log(`🔍 验证用户配置：${username}\n`);
  
  try {
    const usersResponse = await callApi('GET', '/api/users');
    const users = usersResponse.response?.users || [];
    
    console.log(`📊 总共 ${users.length} 个用户\n`);
    
    const user = users.find(u => u.username === username);
    if (!user) {
      console.error(`❌ 找不到用户：${username}`);
      console.log('\n可用用户列表:');
      users.slice(0, 10).forEach(u => console.log(`  - ${u.username}`));
      if (users.length > 10) console.log(`  ... 还有 ${users.length - 10} 个用户`);
      process.exit(1);
    }
    
    console.log('📋 用户信息:');
    console.log(`  用户名：${user.username}`);
    console.log(`  状态：${user.status}`);
    console.log(`  邮箱：${user.email}`);
    console.log('');
    
    console.log('📊 流量配置:');
    console.log(`  流量限制：${(user.trafficLimitBytes / 1024 / 1024 / 1024).toFixed(2)} GB`);
    const trafficReset = user.trafficResetInterval || user.trafficLimitStrategy || '未设置';
    console.log(`  流量重置：${trafficReset}${trafficReset === 'NO_RESET' || trafficReset === '未设置' ? ' ⚠️ 需手动配置' : ' ✅'}`);
    console.log(`  已用流量：${(user.userTraffic?.usedTrafficBytes || 0) / 1024 / 1024} MB`);
    console.log('');
    
    console.log('🔐 设备配置:');
    console.log(`  设备限制：${user.hwidDeviceLimit} 台`);
    console.log('');
    
    console.log('📅 过期时间:');
    console.log(`  过期日期：${user.expireAt.split('T')[0]}`);
    const expireDate = new Date(user.expireAt);
    const now = new Date();
    const daysLeft = Math.ceil((expireDate - now) / (1000 * 60 * 60 * 24));
    console.log(`  剩余天数：${daysLeft} 天`);
    console.log('');
    
    console.log('👥 内部分组:');
    if (user.activeInternalSquads && user.activeInternalSquads.length > 0) {
      user.activeInternalSquads.forEach(squad => {
        console.log(`  ✅ ${squad.name}`);
      });
    } else {
      console.log('  ❌ 未分配任何组');
    }
    console.log('');
    
    console.log('🔑 认证信息:');
    console.log(`  VLESS UUID: ${user.vlessUuid}`);
    console.log(`  Trojan 密码：${user.trojanPassword}`);
    console.log(`  SS 密码：${user.ssPassword}`);
    console.log('');
    
    console.log('🌐 订阅地址:');
    console.log(`  ${user.subscriptionUrl}`);
    console.log('');
    
    // 检查结果
    console.log('✅ 配置检查完成\n');
    
    const issues = [];
    if (!user.trafficResetInterval) issues.push('⚠️  流量重置策略未设置');
    if (!user.activeInternalSquads || user.activeInternalSquads.length === 0) issues.push('⚠️  未分配内部分组');
    if (daysLeft < 30) issues.push(`⚠️  账号即将过期（剩余 ${daysLeft} 天）`);
    
    if (issues.length > 0) {
      console.log('⚠️  发现以下问题:');
      issues.forEach(issue => console.log(`  ${issue}`));
      console.log('\n💡 建议：请在管理后台手动配置未完成的项目');
    } else {
      console.log('✅ 所有配置正常！');
    }
    
  } catch (error) {
    console.error('❌ 验证失败:', error.message);
    process.exit(1);
  }
}

verifyUserConfig();
