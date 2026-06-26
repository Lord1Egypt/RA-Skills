const { getRemnawaveToken } = require('./lib/env-loader');
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/remnawave.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));

const targetUsername = 'iven_pc';
const newSquadName = 'Access Gateway';
const newSquadUuid = '0a19fbb7-1fea-4862-b1b2-603994b3709a';

function callApi(method, endpoint, data = null) {
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
        try { resolve({ status: res.statusCode, response: JSON.parse(data) }); } 
        catch(e) { resolve({ status: res.statusCode, response: data }); }
      });
    });
    req.on('error', () => resolve({ status: 0, response: 'network error' }));
    req.end();
  });
}

async function main() {
  console.log(`🔍 查找用户：${targetUsername}...\n`);
  
  // 遍历所有用户查找 - ✅ 正确的分页参数：page=0, size=200
  let targetUser = null;
  let page = 0;
  
  while (true) {
    const resp = await callApi('GET', `/api/users?page=${page}&size=200`);
    const users = resp.response?.users || [];
    targetUser = users.find(u => u.username === targetUsername);
    if (targetUser) break;
    if (users.length < 200) break;
    page++;
  }
  
  if (!targetUser) {
    console.log('❌ 用户不存在');
    return;
  }
  
  console.log(`✅ 找到用户：${targetUser.username}`);
  console.log(`   UUID: ${targetUser.uuid}`);
  console.log(`   邮箱：${targetUser.email || '无'}`);
  console.log(`   当前分组：${targetUser.activeInternalSquads?.map(s => s.name).join(', ') || '无'}`);
  console.log();
  
  // 获取当前分组 UUID 列表
  const currentSquads = targetUser.activeInternalSquads || [];
  const currentSquadUuids = currentSquads.map(s => s.uuid);
  
  // 检查是否已在新分组中
  if (currentSquadUuids.includes(newSquadUuid)) {
    console.log(`✅ 用户已在 "${newSquadName}" 分组中，无需添加`);
    return;
  }
  
  // 添加新分组
  const newSquadUuids = [...currentSquadUuids, newSquadUuid];
  
  console.log(`➕ 准备添加分组：${newSquadName}`);
  console.log(`   当前分组：${currentSquads.map(s => s.name).join(', ')}`);
  console.log(`   添加后分组：${newSquadUuids.length} 个`);
  console.log();
  
  // 调用 API 更新用户分组 - ✅ PATCH /api/users，传递完整用户数据
  const updateData = {
    uuid: targetUser.uuid,
    username: targetUser.username,
    email: targetUser.email,
    status: targetUser.status,
    trafficLimitBytes: targetUser.trafficLimitBytes,
    trafficLimitStrategy: targetUser.trafficLimitStrategy,
    expireAt: targetUser.expireAt,
    hwidDeviceLimit: targetUser.hwidDeviceLimit,
    activeInternalSquads: newSquadUuids,
    description: targetUser.description,
    tag: targetUser.tag,
    telegramId: targetUser.telegramId,
    externalSquadUuid: targetUser.externalSquadUuid
  };
  
  console.log(`📡 调用 API 更新用户分组...`);
  const updateResp = await callApi('PATCH', '/api/users', updateData);
  
  if (updateResp.status === 200) {
    console.log('✅ 分组添加成功!');
    console.log();
    
    // 验证更新结果
    const verifyResp = await callApi('GET', `/api/users/by-username/${targetUsername}`);
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
