#!/usr/bin/env node

/**
 * Remnawave Robot 配置向导
 * 
 * 用途：交互式配置 API 和邮箱信息
 * 
 * 用法:
 * node setup.js
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_DIR = path.join(__dirname, 'config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
  red: '\x1b[31m',
  gray: '\x1b[90m'
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

function info(message) {
  log(colors.blue, `ℹ️  ${message}`);
}

function warning(message) {
  log(colors.yellow, `⚠️  ${message}`);
}

// 创建 readline 接口
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(question, defaultValue = '') {
  return new Promise((resolve) => {
    const defaultText = defaultValue ? ` [${defaultValue}]` : '';
    rl.question(`${question}${defaultText}: `, (answer) => {
      resolve(answer.trim() || defaultValue);
    });
  });
}

// 确保配置目录存在
function ensureConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
    success(`创建配置目录：${CONFIG_DIR}`);
  }
}

// 保存 Remnawave 配置
function saveRemnawaveConfig(config) {
  fs.writeFileSync(
    REMNAWAVE_CONFIG,
    JSON.stringify(config, null, 2),
    'utf-8'
  );
  fs.chmodSync(REMNAWAVE_CONFIG, 0o600);
}

// 保存 SMTP 配置
function saveSmtpConfig(config) {
  fs.writeFileSync(
    SMTP_CONFIG,
    JSON.stringify(config, null, 2),
    'utf-8'
  );
  fs.chmodSync(SMTP_CONFIG, 0o600);
}

// 保存 API Token 到 .env
function saveApiToken(token) {
  let envContent = '';
  
  if (fs.existsSync(ENV_FILE)) {
    envContent = fs.readFileSync(ENV_FILE, 'utf-8');
    
    // 如果已存在则替换
    if (envContent.includes('REMNAWAVE_API_TOKEN=')) {
      envContent = envContent.replace(
        /^REMNAWAVE_API_TOKEN=.*$/m,
        `REMNAWAVE_API_TOKEN=${token}`
      );
    } else {
      envContent += `\nREMNAWAVE_API_TOKEN=${token}\n`;
    }
  } else {
    envContent = `REMNAWAVE_API_TOKEN=${token}\n`;
  }
  
  fs.writeFileSync(ENV_FILE, envContent, 'utf-8');
  fs.chmodSync(ENV_FILE, 0o600);
}

// 主配置流程
async function setup() {
  console.log('');
  log(colors.blue, '╔════════════════════════════════════════════════════════╗');
  log(colors.blue, '║   Remnawave Robot 配置向导                             ║');
  log(colors.blue, '╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  ensureConfigDir();
  
  info('本向导将帮助您配置以下内容:\n');
  console.log('  1. Remnawave API 配置');
  console.log('  2. SMTP 发件邮箱配置');
  console.log('  3. 默认邮件模板');
  console.log('');
  
  // ===== Remnawave API 配置 =====
  log(colors.blue, '═══ 1. Remnawave API 配置 ═══\n');
  
  const apiBaseUrl = await askQuestion(
    'Remnawave API 地址',
    'https://8.212.8.43'
  );
  
  const apiToken = await askQuestion(
    'Remnawave API Token (从管理后台获取)'
  );
  
  if (!apiToken) {
    error('API Token 不能为空!');
    process.exit(1);
  }
  
  const sslReject = await askQuestion(
    '忽略 SSL 证书验证 (自签名证书选 true)',
    'true'
  );
  
  const remnawaveConfig = {
    apiBaseUrl: apiBaseUrl,
    apiVersion: 'v1',
    sslRejectUnauthorized: sslReject.toLowerCase() === 'true',
    _note: sslReject.toLowerCase() === 'true' ? '自签名证书，需要忽略 SSL 验证' : '正式证书',
    _configuredAt: new Date().toISOString()
  };
  
  saveRemnawaveConfig(remnawaveConfig);
  saveApiToken(apiToken);
  success('Remnawave API 配置已保存');
  console.log('');
  
  // ===== SMTP 配置 =====
  log(colors.blue, '═══ 2. SMTP 发件邮箱配置 ═══\n');
  
  const fromEmail = await askQuestion(
    '发件邮箱地址'
  );
  
  if (!fromEmail) {
    error('发件邮箱不能为空!');
    process.exit(1);
  }
  
  const smtpHost = await askQuestion(
    'SMTP 服务器地址',
    'smtp.zoho.com'
  );
  
  const smtpPort = await askQuestion(
    'SMTP 端口',
    '587'
  );
  
  const smtpUser = await askQuestion(
    'SMTP 用户名 (通常与邮箱相同)',
    fromEmail
  );
  
  const smtpPass = await askQuestion(
    'SMTP 密码/授权码'
  );
  
  if (!smtpPass) {
    error('SMTP 密码不能为空!');
    process.exit(1);
  }
  
  const smtpSecure = await askQuestion(
    '使用 SSL/TLS (true/false)',
    'false'
  );
  
  const smtpConfig = {
    host: smtpHost,
    port: parseInt(smtpPort),
    secure: smtpSecure.toLowerCase() === 'true',
    auth: {
      user: smtpUser,
      pass: smtpPass
    },
    from: {
      email: fromEmail,
      name: 'AI Assistant'
    },
    tls: {
      rejectUnauthorized: sslReject.toLowerCase() === 'true'
    },
    _configuredAt: new Date().toISOString()
  };
  
  saveSmtpConfig(smtpConfig);
  success('SMTP 配置已保存');
  console.log('');
  
  // ===== 验证配置 =====
  log(colors.blue, '═══ 3. 验证配置 ═══\n');
  
  info('配置摘要:\n');
  console.log('📡 Remnawave API:');
  console.log(`   地址：${apiBaseUrl}`);
  console.log(`   SSL 验证：${sslReject}`);
  console.log('');
  console.log('📧 SMTP 邮箱:');
  console.log(`   发件人：${fromEmail}`);
  console.log(`   服务器：${smtpHost}:${smtpPort}`);
  console.log('');
  
  // 创建默认邮件模板
  const templateDir = path.join(__dirname, 'templates');
  if (!fs.existsSync(templateDir)) {
    fs.mkdirSync(templateDir, { recursive: true });
  }
  
  const defaultTemplate = `# Remnawave 账号开通通知

尊敬的 {{recipient_name}}：

您的账号已创建成功！

## 账号信息

- **账号名称:** {{account_name}}
- **订阅地址:** {{subscription_url}}
- **流量限制:** 100GB/周
- **设备限制:** 1 台
- **过期时间:** 365 天

## 使用教程

1. 下载安装客户端
2. 导入订阅链接
3. 选择节点连接

**教程链接:** {{tutorial_url}}

## 注意事项

- 请勿分享订阅链接
- 流量每周重置
- 过期前请续费

---

此邮件由系统自动发送，请勿回复。

**发送时间:** {{send_date}}
`;
  
  fs.writeFileSync(
    path.join(templateDir, 'account-created.md'),
    defaultTemplate,
    'utf-8'
  );
  
  success('默认邮件模板已创建');
  console.log('');
  
  // ===== 完成 =====
  console.log('');
  log(colors.green, '╔════════════════════════════════════════════════════════╗');
  log(colors.green, '║   配置完成！                                           ║');
  log(colors.green, '╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  info('下一步:\n');
  console.log('  1. 测试配置：node test-config.js');
  console.log('  2. 创建账号：node create-account.js --username test_pc --email test@example.com');
  console.log('  3. 查看帮助：node --help');
  console.log('');
  
  rl.close();
}

// 运行配置向导
setup().catch((error) => {
  error(`配置失败：${error.message}`);
  process.exit(1);
});
