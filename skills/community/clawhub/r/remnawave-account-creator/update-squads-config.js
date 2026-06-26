#!/usr/bin/env node

/**
 * 获取 Remnawave 内部组列表并更新配置
 * 
 * 用法：node update-squads-config.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, '../../config');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');

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
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API 错误：${res.statusCode}`));
          }
        } catch (error) {
          reject(new Error(`解析响应失败`));
        }
      });
    });
    
    req.on('error', reject);
    req.end();
  });
}

async function updateSquadsConfig() {
  console.log('🔄 获取内部组列表...\n');
  
  try {
    const response = await callApi('GET', '/api/internal-squads');
    const squads = response.response.internalSquads;
    
    console.log(`✅ 获取到 ${squads.length} 个内部组\n`);
    
    const squadsConfig = {
      squads: {},
      _updatedAt: new Date().toISOString(),
      _note: 'UUID 必须是完整格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    };
    
    console.log('📋 组列表:');
    squads.forEach((squad, index) => {
      squadsConfig.squads[squad.name.trim()] = squad.uuid;
      console.log(`  ${index + 1}. ${squad.name.trim()}`);
      console.log(`     UUID: ${squad.uuid}`);
      console.log(`     成员：${squad.info.membersCount} 人`);
      console.log(`     入站：${squad.info.inboundsCount} 个`);
      console.log('');
    });
    
    // 保存配置
    fs.writeFileSync(
      SQUADS_CONFIG,
      JSON.stringify(squadsConfig, null, 2),
      'utf-8'
    );
    
    console.log(`✅ 配置已更新：${SQUADS_CONFIG}`);
    console.log('\n💡 提示：现在可以使用这些组名创建账号了');
    
  } catch (error) {
    console.error('❌ 更新失败:', error.message);
    process.exit(1);
  }
}

updateSquadsConfig();
