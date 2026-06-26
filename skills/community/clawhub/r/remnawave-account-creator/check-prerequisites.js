#!/usr/bin/env node

/**
 * Remnawave 账号创建 - 前置检查脚本
 * 
 * 用途：在创建账号前验证所有配置和连接是否正常
 * 
 * 用法:
 * node check-prerequisites.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 配置文件路径
const CONFIG_DIR = path.join(__dirname, '../../config');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');
const EMAIL_TEMPLATE = path.join(CONFIG_DIR, 'email-templates/remnawave-account-created.md');

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

// 检查文件是否存在
function checkFileExists(filePath, description) {
  if (fs.existsSync(filePath)) {
    success(`${description}: ${filePath}`);
    return true;
  } else {
    error(`${description}不存在：${filePath}`);
    return false;
  }
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

// 检查 Remnawave API 配置
function checkRemnawaveConfig() {
  info('检查 Remnawave API 配置...');
  
  const config = readJsonConfig(REMNAWAVE_CONFIG);
  
  if (!config) {
    error('Remnawave 配置文件无效或格式错误');
    return false;
  }
  
  let allValid = true;
  
  // 检查必需字段
  if (!config.apiBaseUrl) {
    error('缺少 apiBaseUrl 配置');
    allValid = false;
  } else {
    success(`API 地址：${config.apiBaseUrl}`);
  }
  
  if (!config.apiToken) {
    error('缺少 apiToken 配置');
    allValid = false;
  } else {
    // 检查 Token 格式（JWT 应该有 3 部分）
    const tokenParts = config.apiToken.split('.');
    if (tokenParts.length === 3) {
      success('API Token 格式正确');
      
      // 尝试解析 Token 信息
      try {
        const payload = JSON.parse(Buffer.from(tokenParts[1], 'base64').toString());
        if (payload.exp) {
          const expiresAt = new Date(payload.exp * 1000);
          const now = new Date();
          const daysUntilExpiry = Math.floor((expiresAt - now) / (1000 * 60 * 60 * 24));
          
          if (daysUntilExpiry > 365) {
            success(`Token 有效期：长期有效 (${daysUntilExpiry}天)`);
          } else if (daysUntilExpiry > 30) {
            warning(`Token 有效期：${daysUntilExpiry}天`);
          } else if (daysUntilExpiry > 0) {
            error(`Token 即将过期：仅剩${daysUntilExpiry}天`);
            allValid = false;
          } else {
            error('Token 已过期');
            allValid = false;
          }
        }
      } catch (e) {
        warning('无法解析 Token  payload');
      }
    } else {
      error('API Token 格式不正确（应为 JWT 格式）');
      allValid = false;
    }
  }
  
  if (config.sslRejectUnauthorized !== undefined) {
    if (config.sslRejectUnauthorized === false) {
      warning('SSL 验证已禁用（使用自签名证书）');
    } else {
      success('SSL 验证已启用');
    }
  }
  
  return allValid;
}

// 测试 Remnawave API 连接
async function testRemnawaveApi() {
  info('测试 Remnawave API 连接...');
  
  const config = readJsonConfig(REMNAWAVE_CONFIG);
  
  if (!config || !config.apiBaseUrl || !config.apiToken) {
    error('配置不完整，无法测试 API 连接');
    return false;
  }
  
  return new Promise((resolve) => {
    const options = {
      hostname: new URL(config.apiBaseUrl).hostname,
      port: 443,
      path: '/api/users',
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${config.apiToken}`,
        'Content-Type': 'application/json'
      },
      rejectUnauthorized: config.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 401) {
          if (res.statusCode === 200) {
            success(`API 连接成功 (状态码：${res.statusCode})`);
            try {
              const response = JSON.parse(responseData);
              if (response.response && Array.isArray(response.response)) {
                success(`当前用户数：${response.response.length}`);
              }
            } catch (e) {
              // 忽略解析错误
            }
            resolve(true);
          } else if (res.statusCode === 401) {
            error('API Token 无效 (401 Unauthorized)');
            resolve(false);
          }
        } else {
          error(`API 连接失败 (状态码：${res.statusCode})`);
          resolve(false);
        }
      });
    });
    
    req.on('error', (error) => {
      error(`API 连接失败：${error.message}`);
      if (error.code === 'UNABLE_TO_VERIFY_LEAF_SIGNATURE' || error.code === 'SELF_SIGNED_CERT') {
        warning('SSL 证书验证失败，请设置 sslRejectUnauthorized: false');
      }
      resolve(false);
    });
    
    req.end();
  });
}

// 检查 SMTP 配置
function checkSmtpConfig() {
  info('检查 SMTP 邮件配置...');
  
  const config = readJsonConfig(SMTP_CONFIG);
  
  if (!config) {
    error('SMTP 配置文件无效或格式错误');
    return false;
  }
  
  let allValid = true;
  
  if (!config.host) {
    error('缺少 SMTP host 配置');
    allValid = false;
  } else {
    success(`SMTP 服务器：${config.host}`);
  }
  
  if (!config.port) {
    error('缺少 SMTP port 配置');
    allValid = false;
  } else {
    success(`SMTP 端口：${config.port}`);
  }
  
  if (!config.auth || !config.auth.user || !config.auth.pass) {
    error('SMTP 认证信息不完整');
    allValid = false;
  } else {
    success(`SMTP 用户：${config.auth.user}`);
  }
  
  if (!config.from || !config.from.email) {
    error('缺少发件人配置');
    allValid = false;
  } else {
    success(`发件人：${config.from.email}`);
  }
  
  return allValid;
}

// 检查组 UUID 映射
function checkSquadsConfig() {
  info('检查组 UUID 映射...');
  
  const config = readJsonConfig(SQUADS_CONFIG);
  
  if (!config) {
    error('组配置文件无效或格式错误');
    return false;
  }
  
  if (!config.squads || typeof config.squads !== 'object') {
    error('缺少 squads 配置');
    return false;
  }
  
  const squadCount = Object.keys(config.squads).length;
  success(`已配置 ${squadCount} 个组`);
  
  // 验证 UUID 格式
  let invalidUuids = 0;
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  
  for (const [squadName, squadUuid] of Object.entries(config.squads)) {
    if (!uuidRegex.test(squadUuid)) {
      warning(`组 "${squadName}" 的 UUID 格式不正确：${squadUuid}`);
      invalidUuids++;
    }
  }
  
  if (invalidUuids === 0) {
    success('所有 UUID 格式正确');
  } else {
    warning(`${invalidUuids} 个 UUID 格式不正确（应为 xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx）`);
  }
  
  // 显示可用组列表
  console.log('\n可用组列表:');
  for (const [squadName, squadUuid] of Object.entries(config.squads)) {
    console.log(`  - ${squadName}: ${squadUuid}`);
  }
  
  return invalidUuids === 0;
}

// 检查邮件模板
function checkEmailTemplate() {
  info('检查邮件模板...');
  
  if (!fs.existsSync(EMAIL_TEMPLATE)) {
    error(`邮件模板不存在：${EMAIL_TEMPLATE}`);
    return false;
  }
  
  const content = fs.readFileSync(EMAIL_TEMPLATE, 'utf-8');
  
  // 检查必需变量
  const requiredVars = [
    '{{recipient_name}}',
    '{{account_name}}',
    '{{subscription_url}}',
    '{{send_date}}'
  ];
  
  let missingVars = [];
  for (const variable of requiredVars) {
    if (!content.includes(variable)) {
      missingVars.push(variable);
    }
  }
  
  if (missingVars.length > 0) {
    error(`邮件模板缺少变量：${missingVars.join(', ')}`);
    return false;
  }
  
  success('邮件模板完整');
  return true;
}

// 检查文件权限
function checkFilePermissions() {
  info('检查文件权限...');
  
  const sensitiveFiles = [
    REMNAWAVE_CONFIG,
    SMTP_CONFIG
  ];
  
  let allValid = true;
  
  for (const filePath of sensitiveFiles) {
    if (fs.existsSync(filePath)) {
      const stats = fs.statSync(filePath);
      const mode = stats.mode & 0o777;
      
      if (mode <= 0o600) {
        success(`${path.basename(filePath)}: 权限 ${mode.toString(8)} (安全)`);
      } else {
        warning(`${path.basename(filePath)}: 权限 ${mode.toString(8)} (建议设置为 600)`);
      }
    }
  }
  
  return allValid;
}

// 主函数
async function main() {
  console.log('');
  log(colors.cyan, '╔════════════════════════════════════════════════════════╗');
  log(colors.cyan, '║   Remnawave 账号创建 - 前置检查                        ║');
  log(colors.cyan, '╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  const results = {
    configFiles: true,
    remnawaveConfig: false,
    remnawaveApi: false,
    smtpConfig: false,
    squadsConfig: false,
    emailTemplate: false,
    filePermissions: true
  };
  
  // 检查配置文件是否存在
  info('检查配置文件...');
  results.configFiles = checkFileExists(REMNAWAVE_CONFIG, 'Remnawave 配置') &&
                        checkFileExists(SMTP_CONFIG, 'SMTP 配置') &&
                        checkFileExists(SQUADS_CONFIG, '组配置');
  console.log('');
  
  // 检查 Remnawave 配置
  results.remnawaveConfig = checkRemnawaveConfig();
  console.log('');
  
  // 测试 Remnawave API 连接
  results.remnawaveApi = await testRemnawaveApi();
  console.log('');
  
  // 检查 SMTP 配置
  results.smtpConfig = checkSmtpConfig();
  console.log('');
  
  // 检查组 UUID 映射
  results.squadsConfig = checkSquadsConfig();
  console.log('');
  
  // 检查邮件模板
  results.emailTemplate = checkEmailTemplate();
  console.log('');
  
  // 检查文件权限
  results.filePermissions = checkFilePermissions();
  console.log('');
  
  // 汇总结果
  console.log('');
  log(colors.cyan, '╔════════════════════════════════════════════════════════╗');
  log(colors.cyan, '║   检查结果汇总                                         ║');
  log(colors.cyan, '╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  const passed = Object.values(results).filter(r => r).length;
  const total = Object.values(results).length;
  
  if (passed === total) {
    success(`所有检查通过 (${passed}/${total})`);
    log(colors.green, '\n🎉 系统已就绪，可以创建账号！\n');
    process.exit(0);
  } else {
    warning(`${passed}/${total} 项检查通过`);
    
    if (!results.remnawaveConfig || !results.remnawaveApi) {
      error('\nRemnawave API 配置或连接有问题，无法创建账号');
    }
    if (!results.smtpConfig) {
      warning('SMTP 配置有问题，可能无法发送邮件');
    }
    if (!results.squadsConfig) {
      warning('组配置有问题，用户可能分配到错误的组');
    }
    
    log(colors.yellow, '\n⚠️  请先修复上述问题后再创建账号\n');
    process.exit(1);
  }
}

// 运行主函数
main().catch((error) => {
  error(`检查过程出错：${error.message}`);
  process.exit(1);
});
