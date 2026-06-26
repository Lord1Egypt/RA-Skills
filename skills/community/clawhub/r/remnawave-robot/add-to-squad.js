#!/usr/bin/env node

/**
 * Remnawave Robot - 添加用户到分组
 * 
 * 用法:
 * node add-to-squad.js --username <用户名> --squad "<分组名>"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, 'config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');

function getRemnawaveToken() {
  const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
  const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
  return match ? match[1].trim() : null;
}

function readConfig(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function callApi(method, endpoint, data = null) {
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
    
    if (data) req.write(JSON.stringify(data));
    req.on('error', () => resolve({ status: 0, response: 'network error' }));
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);
  let username = null, squadName = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--username' && args[i + 1]) username = args[++i];
    else if (args[i] === '--squad' && args[i + 1]) squadName = args[++i];
  }
  
  if (!username || !squadName) {
    console.error('用法：node add-to-squad.js --username <用户名> --squad <分组名>');
    process.exit(1);
  }
  
  console.log(`🔍 查找用户：${username}...\n`);
  
  const userResp = await callApi('GET', `/api/users/by-username/${username}`);
  const user = userResp.response?.response || userResp.response;
  
  if (!user || !user.uuid) {
    console.log('❌ 用户不存在');
    return;
  }
  
  console.log(`✅ 找到用户：${user.username}`);
  console.log(`   当前分组：${user.activeInternalSquads?.map(s => s.name).join(', ') || '无'}`);
  console.log();
  
  const squadsConfig = readConfig(SQUADS_CONFIG);
  const squadUuid = squadsConfig.squads[squadName];
  
  if (!squadUuid) {
    console.log(`❌ 找不到分组 "${squadName}"`);
    console.log('   请先运行：node sync-squads.js');
    return;
  }
  
  const currentSquads = user.activeInternalSquads || [];
  const currentUuids = currentSquads.map(s => s.uuid);
  
  if (currentUuids.includes(squadUuid)) {
    console.log(`✅ 用户已在 "${squadName}" 分组中`);
    return;
  }
  
  const newUuids = [...currentUuids, squadUuid];
  
  console.log(`➕ 添加分组：${squadName}`);
  console.log(`   添加后分组：${newUuids.length} 个\n`);
  
  const updateData = {
    uuid: user.uuid,
    username: user.username,
    email: user.email,
    hwidDeviceLimit: user.hwidDeviceLimit,
    trafficLimitBytes: user.trafficLimitBytes,
    trafficLimitStrategy: user.trafficLimitStrategy,
    expireAt: user.expireAt,
    activeInternalSquads: newUuids
  };
  
  const updateResp = await callApi('PATCH', '/api/users', updateData);
  
  if (updateResp.status === 200) {
    console.log('✅ 分组添加成功!\n');
    
    const verifyResp = await callApi('GET', `/api/users/by-username/${username}`);
    const updatedUser = verifyResp.response?.response || verifyResp.response;
    
    console.log('📋 更新后的分组:');
    updatedUser.activeInternalSquads?.forEach((s, i) => {
      console.log(`   ${i + 1}. ${s.name}`);
    });
  } else {
    console.log(`❌ 更新失败：${updateResp.status}`);
  }
}

main();
