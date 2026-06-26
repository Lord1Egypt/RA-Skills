#!/usr/bin/env node

/**
 * Remnawave Robot - 测试配置
 * 
 * 用法:
 * node test-config.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const CONFIG_DIR = path.join(__dirname, 'config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');

function getRemnawaveToken() {
  const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
  const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
  return match ? match[1].trim() : null;
}

function readConfig(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

async function testApi() {
  console.log('📡 测试 Remnawave API...\n');
  
  const config = readConfig(REMNAWAVE_CONFIG);
  const token = getRemnawaveToken();
  
  return new Promise((resolve) => {
    const url = new URL('/api/users?size=1', config.apiBaseUrl);
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: 'GET',
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
        if (res.statusCode === 200) {
          console.log('✅ API 连接成功');
          console.log(`   地址：${config.apiBaseUrl}`);
          console.log(`   状态码：${res.statusCode}\n`);
          resolve(true);
        } else {
          console.log(`❌ API 连接失败：${res.statusCode}`);
          console.log(`   响应：${data}\n`);
          resolve(false);
        }
      });
    });
    
    req.on('error', (e) => {
      console.log(`❌ API 连接错误：${e.message}\n`);
      resolve(false);
    });
    
    req.end();
  });
}

async function testSmtp() {
  console.log('📧 测试 SMTP 邮箱...\n');
  
  const config = readConfig(SMTP_CONFIG);
  
  const transporter = nodemailer.createTransport({
    host: config.host,
    port: config.port,
    secure: config.secure,
    auth: config.auth,
    tls: config.tls
  });
  
  try {
    await transporter.verify();
    console.log('✅ SMTP 连接成功');
    console.log(`   服务器：${config.host}:${config.port}`);
    console.log(`   发件人：${config.from?.email || config.auth.user}\n`);
    return true;
  } catch (error) {
    console.log(`❌ SMTP 连接失败：${error.message}\n`);
    return false;
  }
}

async function main() {
  console.log('');
  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║   Remnawave Robot 配置测试                             ║');
  console.log('╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  // 检查配置文件
  console.log('📋 检查配置文件...\n');
  
  const files = [
    REMNAWAVE_CONFIG,
    SMTP_CONFIG,
    ENV_FILE
  ];
  
  let allFilesExist = true;
  for (const file of files) {
    if (fs.existsSync(file)) {
      console.log(`✅ ${path.basename(file)}`);
    } else {
      console.log(`❌ ${path.basename(file)} 不存在`);
      allFilesExist = false;
    }
  }
  
  if (!allFilesExist) {
    console.log('\n❌ 配置文件不完整，请先运行：node setup.js\n');
    process.exit(1);
  }
  
  console.log('');
  
  // 测试 API
  const apiOk = await testApi();
  
  // 测试 SMTP
  const smtpOk = await testSmtp();
  
  // 总结
  console.log('══════════════════════════════════════════════════════════');
  console.log('📊 测试结果:');
  console.log('');
  console.log(`   Remnawave API: ${apiOk ? '✅ 正常' : '❌ 失败'}`);
  console.log(`   SMTP 邮箱：${smtpOk ? '✅ 正常' : '❌ 失败'}`);
  console.log('');
  
  if (apiOk && smtpOk) {
    console.log('✅ 所有配置正常，可以开始使用!');
    console.log('');
    console.log('快速开始:');
    console.log('  node create-account.js --username test_pc --email test@example.com --squad "Operations Team"');
    console.log('');
  } else {
    console.log('⚠️  部分配置失败，请检查后重试');
    console.log('');
    console.log('修复配置:');
    console.log('  node setup.js');
    console.log('');
  }
}

main().catch((error) => {
  console.error('❌ 错误:', error.message);
  process.exit(1);
});
