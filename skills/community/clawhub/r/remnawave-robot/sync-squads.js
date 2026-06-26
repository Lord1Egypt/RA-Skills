#!/usr/bin/env node

/**
 * Remnawave Robot - 同步分组列表
 * 
 * 用法:
 * node sync-squads.js
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

function callApi(method, endpoint) {
  return new Promise((resolve, reject) => {
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
  console.log('🔄 同步分组列表...\n');
  
  const resp = await callApi('GET', '/api/internal-squads');
  const squads = resp.response?.response?.internalSquads || resp.response?.internalSquads || [];
  
  if (squads.length === 0) {
    console.log('❌ 未找到分组');
    return;
  }
  
  console.log(`✅ 找到 ${squads.length} 个分组:\n`);
  
  const newSquads = {};
  squads.forEach(squad => {
    const name = squad.name.trim();
    newSquads[name] = squad.uuid;
    console.log(`  - ${name}: ${squad.uuid} (${squad.info?.membersCount || 0} 成员)`);
  });
  
  const config = {
    squads: newSquads,
    _updatedAt: new Date().toISOString(),
    _syncedFrom: 'Remnawave API'
  };
  
  // 备份旧配置
  if (fs.existsSync(SQUADS_CONFIG)) {
    fs.copyFileSync(SQUADS_CONFIG, SQUADS_CONFIG + '.bak');
  }
  
  fs.writeFileSync(SQUADS_CONFIG, JSON.stringify(config, null, 2), 'utf-8');
  fs.chmodSync(SQUADS_CONFIG, 0o600);
  
  console.log('');
  console.log('✅ 配置已保存:', SQUADS_CONFIG);
}

main();
