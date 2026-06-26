#!/usr/bin/env node

/**
 * Remnawave Squad 同步脚本
 * 
 * 用途：从 Remnawave API 同步最新的组信息到本地配置
 * 
 * 用法:
 * node sync-squads.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 配置文件路径
const CONFIG_DIR = path.join(__dirname, '../../config');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(color, message) {
  console.log(`${color}${message}${colors.reset}`);
}

function success(message) {
  log(colors.green, `✅ ${message}`);
}

function error(message) {
  log(colors.red, `❌ ${message}`);
}

function warning(message) {
  log(colors.yellow, `⚠️  ${message}`);
}

function info(message) {
  log(colors.blue, `ℹ️  ${message}`);
}

// 读取 JSON 配置
function readJsonConfig(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
}

// 调用 Remnawave API
function callApi(method, endpoint) {
  return new Promise((resolve, reject) => {
    const remnawaveConfig = readJsonConfig(REMNAWAVE_CONFIG);
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
    req.end();
  });
}

// 同步组信息
async function syncSquads() {
  console.log('');
  log(colors.cyan, '╔════════════════════════════════════════════════════════╗');
  log(colors.cyan, '║   Remnawave Squad 同步                                  ║');
  log(colors.cyan, '╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  info('从 API 获取组列表...\n');
  
  try {
    const response = await callApi('GET', '/api/internal-squads');
    const squads = response.response.internalSquads;
    
    info(`找到 ${squads.length} 个组\n`);
    
    // 构建新的组映射
    const newSquads = {};
    const squadMapping = {};
    
    console.log('组列表:');
    for (const squad of squads) {
      const name = squad.name.trim();
      const uuid = squad.uuid;
      
      newSquads[name] = uuid;
      
      const memberCount = squad.info.membersCount;
      console.log(`  - ${name}: ${uuid} (${memberCount} 成员)`);
    }
    
    // 读取现有配置（保留分组说明）
    const existingConfig = readJsonConfig(SQUADS_CONFIG);
    const existingNotes = existingConfig?._分组说明 || {};
    
    // 创建新配置
    const newConfig = {
      squads: newSquads,
      _updatedAt: new Date().toISOString(),
      _syncedFrom: 'Remnawave API',
      _note: '此文件由 sync-squads.js 自动同步，不要手动编辑',
      _分组说明: existingNotes
    };
    
    // 写入配置文件
    const backupPath = SQUADS_CONFIG + '.backup';
    fs.copyFileSync(SQUADS_CONFIG, backupPath);
    warning(`备份已保存：${backupPath}`);
    
    fs.writeFileSync(SQUADS_CONFIG, JSON.stringify(newConfig, null, 2), 'utf-8');
    console.log('');
    success(`组配置已更新：${SQUADS_CONFIG}`);
    
    console.log('');
    log(colors.cyan, '╔════════════════════════════════════════════════════════╗');
    log(colors.cyan, '║   同步完成                                             ║');
    log(colors.cyan, '╚════════════════════════════════════════════════════════╝');
    console.log('');
    
    // 显示更新后的配置
    info('更新后的组配置:');
    console.log('');
    console.log(JSON.stringify(newConfig.squads, null, 2));
    console.log('');
    
  } catch (error) {
    error(`同步失败：${error.message}`);
    process.exit(1);
  }
}

// 运行主函数
syncSquads();
