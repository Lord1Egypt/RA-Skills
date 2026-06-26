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
  
  // 先获取用户当前信息
  const userResp = await callApi('GET', `/api/users/by-username/${targetUsername}`);
  
  if (userResp.status !== 200 || !userResp.response?.uuid) {
    console.log('❌ 用户不存在或查询失败');
    return;
  }
  
  const user = userResp.response;
  console.log(`✅ 找到用户：${user.username}`);
  console.log(`   UUID: ${user.uuid}`);
  console.log(`   邮箱：${user.email || '无'}`);
  console.log(`   当前分组：${user.activeInternalSquads?.map(s => s.name).join(', ') || '无'}`);
  console.log();
  
  // 获取当前分组 UUID 列表
  const currentSquads = user.activeInternalSquads || [];
  const currentSquadUuids = currentSquads.map(s => s.uuid);
  
  // 检查是否已在新分组中
  if (currentSquadUuids.includes(newSquadUuid)) {
    console.log(`✅ 用户已在 "${newSquadName}" 分组中，无需添加`);
    return;
  }
  
  // 添加新分组
  const newSquadUuids = [...currentSquadUuids, newSquadUuid];
  
  console.log(`➕ 准备添加分组：${newSquadName}`);
  console.log(`   当前分组数：${currentSquads.length}`);
  console.log(`   添加后分组数：${newSquadUuids.length}`);
  console.log(`   新分组列表：${newSquadUuids.join(', ')}`);
  console.log();
  
  // 调用 API 更新用户分组 - ✅ PATCH /api/users，传递完整用户数据
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
  } else {
    console.log(`❌ 更新失败：状态码 ${updateResp.status}`);
    console.log(`   响应：${JSON.stringify(updateResp.response)}`);
  }
}

main();
