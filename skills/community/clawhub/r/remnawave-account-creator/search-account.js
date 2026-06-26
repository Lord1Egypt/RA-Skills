#!/usr/bin/env node

/**
 * Remnawave 账号搜索脚本
 * 
 * 用法:
 * node search-account.js lester
 * node search-account.js --username lester
 * node search-account.js --uuid 59095d09-515e-4d75-a496-8df744f760ff
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, '../../config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');

// 从 .env 读取 Remnawave API Token
function getRemnawaveToken() {
  try {
    const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
    const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
    if (match && match[1]) {
      return match[1].trim();
    }
    throw new Error('REMNAWAVE_API_TOKEN not found in .env');
  } catch (error) {
    console.error('❌ 读取 Remnawave API Token 失败:', error.message);
    process.exit(1);
  }
}

// 读取配置
function readConfig(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`❌ 读取配置文件失败：${filePath}`);
    process.exit(1);
  }
}

// 调用 Remnawave API
function callApi(method, endpoint, data = null) {
  return new Promise((resolve, reject) => {
    const remnawaveConfig = readConfig(REMNAWAVE_CONFIG);
    const apiToken = getRemnawaveToken();
    const url = new URL(endpoint, remnawaveConfig.apiBaseUrl);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${apiToken}`,
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
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API 错误：${res.statusCode} - ${JSON.stringify(response)}`));
          }
        } catch (error) {
          reject(new Error(`解析响应失败：${responseData}`));
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

// 获取所有用户（分页遍历）- SOP 关键修复
// Remnawave API 分页参数：page 从 0 开始，使用 size 而不是 limit
async function getAllUsers() {
  let allUsers = [];
  let page = 0;  // Remnawave 使用 0-based 页码
  let hasMore = true;
  
  while (hasMore) {
    const response = await callApi('GET', `/api/users?page=${page}&size=200`);
    const users = response.response.users || [];
    allUsers = allUsers.concat(users);
    hasMore = users.length === 200;  // 每页 200 个
    page++;
    
    // 安全限制
    if (page > 20) {
      console.warn('⚠️  达到最大分页数 (20 页)');
      break;
    }
  }
  
  return allUsers;
}

// 通过用户名搜索（优先使用 by-username 接口）
async function searchByUsername(username) {
  try {
    // 尝试精确匹配
    const response = await callApi('GET', `/api/users/by-username/${username}`);
    return response.response ? [response.response] : [];
  } catch (error) {
    // by-username 不存在，继续模糊搜索
    return [];
  }
}

// 通过 UUID 搜索
async function searchByUuid(uuid) {
  try {
    const response = await callApi('GET', `/api/users/${uuid}`);
    return response.response ? [response.response] : [];
  } catch (error) {
    return [];
  }
}

// 注意：列表 API 不完整，只返回活跃用户，不用于搜索
// 所有搜索都通过 by-username 接口进行

// 智能搜索：尝试多种用户名变体（不依赖列表 API）
async function smartSearch(keyword) {
  const results = new Map();
  const keywordLower = keyword.toLowerCase();
  
  // 可能的用户名变体
  const variations = [
    // 原始关键词
    keyword,
    keywordLower,
    
    // 常见后缀
    `${keywordLower}_pc`,
    `${keywordLower}_ios`,
    `${keywordLower}_android`,
    `${keywordLower}_mac`,
    `${keywordLower}_linux`,
    `${keywordLower}_win`,
    
    // 常见前缀
    `pc_${keywordLower}`,
    `ios_${keywordLower}`,
    `android_${keywordLower}`,
    
    // 无下划线
    keywordLower.replace(/_/g, ''),
    
    // 下划线替换为横杠
    keywordLower.replace(/_/g, '-'),
    
    // 首字母大写
    keyword.charAt(0).toUpperCase() + keywordLower.slice(1),
    `${keyword.charAt(0).toUpperCase() + keywordLower.slice(1)}_pc`,
  ];
  
  // 尝试每个变体
  for (const variation of variations) {
    if (!variation || variation.trim() === '') continue;
    
    try {
      const response = await callApi('GET', `/api/users/by-username/${variation}`);
      if (response.response && response.response.username) {
        // 额外检查：确保用户名包含关键词（避免误匹配）
        const username = response.response.username.toLowerCase();
        if (username.includes(keywordLower)) {
          results.set(response.response.uuid, response.response);
        }
      }
    } catch (error) {
      // 忽略错误，继续尝试下一个
    }
  }
  
  return Array.from(results.values());
}

// 显示用户信息
function displayUser(user, index) {
  console.log(`${index + 1}. ${user.username}`);
  console.log(`   UUID: ${user.uuid}`);
  console.log(`   短 UUID: ${user.shortUuid}`);
  console.log(`   邮箱：${user.email || '⚠️ 未设置'}`);
  console.log(`   订阅：${user.subscriptionUrl}`);
  console.log(`   状态：${user.status}`);
  console.log(`   分组：${user.activeInternalSquads?.[0]?.name || '无'}`);
  console.log(`   设备限制：${user.hwidDeviceLimit} 台`);
  console.log(`   流量限制：${(user.trafficLimitBytes / 1024 / 1024 / 1024).toFixed(0)}GB`);
  console.log(`   流量重置：${user.trafficLimitStrategy}`);
  console.log(`   过期时间：${user.expireAt?.split('T')[0]}`);
  console.log(`   创建时间：${user.createdAt?.split('T')[0]}`);
  console.log(`   最后使用：${user.subLastOpenedAt ? user.subLastOpenedAt.split('T')[0] : '从未'}`);
  if (user.userTraffic) {
    console.log(`   已用流量：${(user.userTraffic.usedTrafficBytes / 1024 / 1024).toFixed(1)}MB (本周) / ${(user.userTraffic.lifetimeUsedTrafficBytes / 1024 / 1024 / 1024).toFixed(2)}GB (总计)`);
  }
  console.log('');
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('❌ 错误：缺少搜索关键词');
    console.error('');
    console.error('用法：');
    console.error('  node search-account.js <关键词>');
    console.error('  node search-account.js --username <用户名>');
    console.error('  node search-account.js --uuid <UUID>');
    console.error('');
    console.error('示例：');
    console.error('  node search-account.js lester');
    console.error('  node search-account.js --username lester_pc');
    console.error('  node search-account.js --uuid 59095d09-515e-4d75-a496-8df744f760ff');
    process.exit(1);
  }
  
  let results = [];
  let searchMethod = '';
  
  // 解析参数
  if (args[0] === '--uuid' && args[1]) {
    searchMethod = 'UUID';
    results = await searchByUuid(args[1]);
  } else if (args[0] === '--username' && args[1]) {
    searchMethod = '用户名精确';
    results = await searchByUsername(args[1]);
    if (results.length === 0) {
      // 精确搜索不到，尝试模糊搜索
      searchMethod = '用户名模糊';
      results = await fuzzySearch(args[1]);
    }
  } else {
    // 默认：智能搜索（尝试多种用户名变体）
    // 不使用列表 API 模糊搜索（因为列表不完整）
    const keyword = args[0];
    
    // 智能搜索：尝试多种用户名变体
    results = await smartSearch(keyword);
    
    searchMethod = '智能搜索（多变体 by-username）';
  }
  
  // 显示结果
  console.log(`🔍 搜索方式：${searchMethod}`);
  console.log(`📊 匹配结果：${results.length} 个账号`);
  console.log('');
  
  if (results.length === 0) {
    console.log('❌ 没有找到匹配的账号');
  } else {
    console.log('✅ 匹配的账号:');
    console.log('='.repeat(80));
    results.forEach((user, index) => displayUser(user, index));
  }
}

main().catch(error => {
  console.error('❌ 错误:', error.message);
  process.exit(1);
});
