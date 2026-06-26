#!/usr/bin/env node

/**
 * Remnawave 用户添加分组通用脚本
 * 
 * 用法:
 * node add-user-to-squad-generic.js --username <用户名> --squad <分组名>
 * 
 * 示例:
 * node add-user-to-squad-generic.js --username ivens_pc --squad "Access Gateway"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, '../../config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');

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

// 解析命令行参数
const args = process.argv.slice(2);
const params = {
  username: null,
  uuid: null,  // 新增：支持直接指定 UUID
  squad: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) params.username = args[++i];
  else if (args[i] === '--uuid' && args[i + 1]) params.uuid = args[++i];
  else if (args[i] === '--squad' && args[i + 1]) params.squad = args[++i];
}

if (!params.squad || (!params.username && !params.uuid)) {
  console.error('❌ 错误：缺少必填参数');
  console.error('用法 1: node add-user-to-squad-generic.js --username <用户名> --squad <分组名>');
  console.error('用法 2: node add-user-to-squad-generic.js --uuid <用户 UUID> --squad <分组名>');
  console.error('\n推荐：优先使用 --uuid 参数，避免 by-username 接口不稳定问题');
  process.exit(1);
}

// 读取配置文件
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
          const apiResponse = JSON.parse(responseData);
          // ✅ 关键修复：直接返回 API 的 response 字段，避免双重嵌套
          // API 返回：{ response: {...} }
          // 我们返回：{ status, response: {...} } 其中 response 是 API 的 response 字段
          resolve({ status: res.statusCode, response: apiResponse.response });
        } catch (error) {
          resolve({ status: res.statusCode, response: responseData });
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

// 获取组 UUID
function getSquadUuid(squadName) {
  const squadsConfig = readConfig(SQUADS_CONFIG);
  const squadUuid = squadsConfig.squads[squadName];
  
  if (!squadUuid) {
    throw new Error(`找不到分组 "${squadName}"，请先运行 sync-squads.js 同步最新分组列表`);
  }
  
  return squadUuid;
}

// 获取所有用户（分页遍历）
// Remnawave API: page 从 0 开始，使用 size 参数
async function getAllUsers() {
  let allUsers = [];
  let page = 0;
  
  while (true) {
    const resp = await callApi('GET', `/api/users?page=${page}&size=200`);
    // ✅ callApi 现在直接返回 API 的 response 字段
    // API 返回：{ response: { users: [...] } }
    const users = resp.response?.users || [];
    allUsers = allUsers.concat(users);
    if (users.length < 200) break;
    page++;
    if (page > 20) {
      console.warn('⚠️ 达到最大分页数 (20 页)');
      break;
    }
  }
  
  return allUsers;
}

// 查找用户
async function findUser(username) {
  // 先尝试 by-username 接口
  try {
    const directResp = await callApi('GET', `/api/users/by-username/${username}`);
    // ✅ callApi 现在直接返回 API 的 response 字段
    if (directResp.status === 200 && directResp.response?.uuid) {
      return directResp.response;
    }
  } catch (e) {
    // 继续全局搜索
  }
  
  // 全局搜索
  const allUsers = await getAllUsers();
  return allUsers.find(u => u.username === username);
}

// 主函数
async function main() {
  let user = null;
  
  // 如果提供了 UUID，直接使用；否则通过用户名查找
  if (params.uuid) {
    console.log(`🔍 使用 UUID 查找用户：${params.uuid}...\n`);
    
    // 通过分页列表验证 UUID 并获取用户信息
    const allUsers = await getAllUsers();
    user = allUsers.find(u => u.uuid === params.uuid);
    
    if (!user) {
      console.log('❌ 找不到该 UUID 的用户');
      return;
    }
  } else {
    console.log(`🔍 查找用户：${params.username}...\n`);
    user = await findUser(params.username);
  }
  
  if (!user) {
    console.log('❌ 用户不存在');
    return;
  }
  
  console.log(`✅ 找到用户：${user.username}`);
  console.log(`   UUID: ${user.uuid}`);
  console.log(`   邮箱：${user.email || '无'}`);
  console.log(`   当前分组：${user.activeInternalSquads?.map(s => s.name).join(', ') || '无'}`);
  console.log(`   订阅地址：${user.subscriptionUrl}`);
  console.log();
  
  // 获取目标分组 UUID
  let targetSquadUuid;
  try {
    targetSquadUuid = getSquadUuid(params.squad);
  } catch (error) {
    console.error('❌ 错误:', error.message);
    return;
  }
  
  // 获取当前分组 UUID 列表
  const currentSquads = user.activeInternalSquads || [];
  const currentSquadUuids = currentSquads.map(s => s.uuid);
  
  // 检查是否已在目标分组中
  if (currentSquadUuids.includes(targetSquadUuid)) {
    console.log(`✅ 用户已在 "${params.squad}" 分组中，无需添加`);
    return;
  }
  
  // 添加新分组
  const newSquadUuids = [...currentSquadUuids, targetSquadUuid];
  
  console.log(`➕ 准备添加分组：${params.squad}`);
  console.log(`   当前分组：${currentSquads.map(s => s.name).join(', ') || '无'}`);
  console.log(`   添加后分组：${newSquadUuids.length} 个`);
  console.log();
  
  // ✅ 调用 API 更新用户分组 - PATCH /api/users，传递完整用户数据
  const updateData = {
    uuid: user.uuid,
    username: user.username,
    email: user.email,
    status: user.status,
    trafficLimitBytes: user.trafficLimitBytes,
    trafficLimitStrategy: user.trafficLimitStrategy,
    expireAt: user.expireAt,
    hwidDeviceLimit: user.hwidDeviceLimit,
    activeInternalSquads: newSquadUuids,
    description: user.description,
    tag: user.tag,
    telegramId: user.telegramId,
    externalSquadUuid: user.externalSquadUuid
  };
  
  console.log(`📡 调用 API 更新用户分组...`);
  console.log(`   端点：PATCH /api/users`);
  console.log();
  
  const updateResp = await callApi('PATCH', '/api/users', updateData);
  
  if (updateResp.status === 200) {
    console.log('✅ 分组添加成功!');
    console.log();
    
    // 验证更新结果
    const verifyResp = await callApi('GET', `/api/users/by-username/${params.username || params.uuid}`);
    const updatedUser = verifyResp.response;
    
    console.log('📋 更新后的分组信息:');
    console.log(`   分组数：${updatedUser.activeInternalSquads?.length || 0}`);
    console.log(`   分组列表:`);
    updatedUser.activeInternalSquads?.forEach((s, i) => {
      console.log(`     ${i + 1}. ${s.name} (${s.uuid})`);
    });
    console.log(`   订阅地址：${updatedUser.subscriptionUrl}（未变化）`);
  } else {
    console.log(`❌ 更新失败：状态码 ${updateResp.status}`);
    console.log(`   响应：${JSON.stringify(updateResp.response)}`);
  }
}

main();
