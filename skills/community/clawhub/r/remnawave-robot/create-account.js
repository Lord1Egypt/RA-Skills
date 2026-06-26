#!/usr/bin/env node

/**
 * Remnawave Robot - 创建账号并发送邮件
 * 
 * 用法:
 * node create-account.js \
 *   --username jim_pc \
 *   --email jim@codeforce.tech \
 *   --device-limit 1 \
 *   --traffic-gb 100 \
 *   --traffic-reset WEEKLY \
 *   --expire-days 365 \
 *   --squad "Operations Team" \
 *   --cc crads@codeforce.tech
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const CONFIG_DIR = path.join(__dirname, 'config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');
const TEMPLATE_DIR = path.join(__dirname, 'templates');
const LOG_DIR = path.join(__dirname, '../../logs/remnawave-account-creation');

// 确保日志目录存在
const today = new Date();
const logMonthDir = path.join(LOG_DIR, today.toISOString().slice(0, 7));
if (!fs.existsSync(logMonthDir)) {
  fs.mkdirSync(logMonthDir, { recursive: true });
}

// 从 .env 读取 Token
function getRemnawaveToken() {
  try {
    const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
    const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
    if (match && match[1]) {
      return match[1].trim();
    }
    throw new Error('REMNAWAVE_API_TOKEN not found');
  } catch (error) {
    console.error('❌ 读取 API Token 失败:', error.message);
    console.error('   请先运行：node setup.js');
    process.exit(1);
  }
}

// 读取 JSON 配置
function readConfig(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`❌ 读取配置失败：${filePath}`);
    process.exit(1);
  }
}

// 解析命令行参数
const args = process.argv.slice(2);
const params = {
  username: null,
  email: null,
  deviceLimit: 1,
  trafficGb: 100,
  trafficReset: 'WEEK',
  expireDays: 365,
  squad: null,
  cc: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) params.username = args[++i];
  else if (args[i] === '--email' && args[i + 1]) params.email = args[++i];
  else if (args[i] === '--device-limit' && args[i + 1]) params.deviceLimit = parseInt(args[++i]);
  else if (args[i] === '--traffic-gb' && args[i + 1]) params.trafficGb = parseInt(args[++i]);
  else if (args[i] === '--traffic-reset' && args[i + 1]) {
    params.trafficReset = args[++i].toUpperCase();
    // 映射 WEEKLY -> WEEK
    if (params.trafficReset === 'WEEKLY') params.trafficReset = 'WEEK';
  }
  else if (args[i] === '--expire-days' && args[i + 1]) params.expireDays = parseInt(args[++i]);
  else if (args[i] === '--squad' && args[i + 1]) params.squad = args[++i];
  else if (args[i] === '--cc' && args[i + 1]) params.cc = args[++i];
}

// 验证必填参数
if (!params.username || !params.email) {
  console.error('❌ 错误：缺少必填参数');
  console.error('用法：node create-account.js --username <用户名> --email <邮箱> [其他选项]');
  process.exit(1);
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
          const response = JSON.parse(responseData);
          resolve({ status: res.statusCode, response });
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

// 获取分组 UUID
function getSquadUuid(squadName) {
  if (!squadName) return null;
  
  const squadsConfig = readConfig(SQUADS_CONFIG);
  const squadUuid = squadsConfig.squads[squadName];
  
  if (!squadUuid) {
    throw new Error(`找不到分组 "${squadName}"，请先运行 node sync-squads.js`);
  }
  
  return squadUuid;
}

// 渲染邮件模板
function renderTemplate(templateFile, variables) {
  const templatePath = path.join(TEMPLATE_DIR, templateFile);
  let template = fs.readFileSync(templatePath, 'utf-8');
  
  for (const [key, value] of Object.entries(variables)) {
    template = template.replace(new RegExp(`{{${key}}}`, 'g'), value);
  }
  
  return template;
}

// 发送开通邮件（直接复制旧脚本逻辑）
async function sendAccountEmail(accountInfo, ccEmail) {
  const smtpConfig = readConfig(SMTP_CONFIG);
  const templateContent = fs.readFileSync(path.join(TEMPLATE_DIR, 'account-created.md'), 'utf-8');
  
  // 提取 HTML 部分
  const htmlMatch = templateContent.match(/### 正文 \(HTML\)\s*\n```html([\s\S]*?)```/);
  const textMatch = templateContent.match(/### 正文 \(纯文本\)\s*\n```([\s\S]*?)```/);
  
  let htmlContent = htmlMatch ? htmlMatch[1].trim() : templateContent;
  let textContent = textMatch ? textMatch[1].trim() : `账号 ${accountInfo.username} 已创建成功，订阅地址：${accountInfo.subscriptionUrl}`;
  
  // 替换变量
  const vars = {
    recipient_name: accountInfo.username.split('_')[0] || accountInfo.username,
    recipient_email: accountInfo.email,
    account_name: accountInfo.username,
    subscription_url: accountInfo.subscriptionUrl,
    tutorial_url: 'https://rjdx19yd9zo.sg.larksuite.com/docx/EwMLdN3asoQ44FxOlN6lQ6frgdh?from=from_copylink',
    download_url: 'https://v2raytun.com/',
    download_backup: 'https://testappdownload-bydtmscom.oss-cn-hongkong.aliyuncs.com/OPSFILE/v2RayTun_Setup.zip',
    appstore_url: 'https://apps.apple.com/us/app/v2raytun/id6476628951',
    send_date: new Date().toLocaleString('zh-CN')
  };
  
  Object.keys(vars).forEach(key => {
    htmlContent = htmlContent.replace(new RegExp(`{{${key}}}`, 'g'), vars[key]);
    textContent = textContent.replace(new RegExp(`{{${key}}}`, 'g'), vars[key]);
  });
  
  const transporter = nodemailer.createTransport({
    host: smtpConfig.host,
    port: smtpConfig.port,
    secure: smtpConfig.secure,
    auth: smtpConfig.auth,
    tls: smtpConfig.tls
  });
  
  const mailOptions = {
    from: `"${smtpConfig.from.name}" <${smtpConfig.from.email}>`,
    to: accountInfo.email,
    cc: ccEmail,
    subject: `【VPN】账号已创建 - 运维组 Crads`,
    text: textContent,
    html: htmlContent
  };
  
  const info = await transporter.sendMail(mailOptions);
  return info.messageId;
}

// 主函数
async function main() {
  console.log('🚀 开始创建 Remnawave 账号...\n');
  
  // 检查配置
  if (!fs.existsSync(REMNAWAVE_CONFIG) || !fs.existsSync(SMTP_CONFIG)) {
    console.error('❌ 配置不完整，请先运行：node setup.js\n');
    process.exit(1);
  }
  
  console.log('📋 账号信息:');
  console.log(`  用户名：${params.username}`);
  console.log(`  邮箱：${params.email}`);
  console.log(`  设备限制：${params.deviceLimit} 台`);
  console.log(`  流量限制：${params.trafficGb}GB`);
  console.log(`  流量重置：${params.trafficReset}`);
  console.log(`  过期时间：${params.expireDays}天`);
  console.log(`  内部分组：${params.squad || '无'} ${params.squad ? '✅' : ''}`);
  if (params.cc) console.log(`  邮件抄送：${params.cc}`);
  console.log('');
  
  // 检查用户是否存在
  console.log('🔍 检查用户是否存在...');
  const checkResp = await callApi('GET', `/api/users/by-username/${params.username}`);
  if (checkResp.status === 200 && checkResp.response?.uuid) {
    console.log('❌ 用户已存在，无法创建\n');
    process.exit(1);
  }
  console.log('✅ 用户不存在，可以创建\n');
  
  // 获取分组 UUID
  let squadUuids = [];
  if (params.squad) {
    try {
      const squadUuid = getSquadUuid(params.squad);
      squadUuids = [squadUuid];
      console.log(`✅ 分组 UUID: ${squadUuid}`);
    } catch (error) {
      console.error('❌ 错误:', error.message);
      process.exit(1);
    }
  }
  console.log('');
  
  // 调用 API 创建用户
  console.log('📡 调用 Remnawave API...');
  const expireAt = new Date();
  expireAt.setDate(expireAt.getDate() + params.expireDays);
  
  const createData = {
    username: params.username,
    email: params.email,
    hwidDeviceLimit: params.deviceLimit,
    trafficLimitBytes: params.trafficGb * 1073741824,
    trafficLimitStrategy: params.trafficReset,
    expireAt: expireAt.toISOString(),
    activeInternalSquads: squadUuids
  };
  
  const createResp = await callApi('POST', '/api/users', createData);
  
  // 201 Created 也是成功
  if (createResp.status !== 200 && createResp.status !== 201) {
    console.log(`❌ 创建失败：状态码 ${createResp.status}`);
    console.log(`   响应：${JSON.stringify(createResp.response)}`);
    process.exit(1);
  }
  
  const account = createResp.response.response || createResp.response;
  console.log('✅ 账号创建成功!\n');
  
  console.log('📋 账号详情:');
  console.log(`  UUID: ${account.uuid}`);
  console.log(`  短 UUID: ${account.shortUuid}`);
  console.log(`  状态：${account.status}`);
  console.log(`  订阅地址：${account.subscriptionUrl}`);
  console.log('');
  
  // 发送邮件
  console.log('📧 准备发送开通邮件...');
  let messageId = '发送失败';
  try {
    messageId = await sendAccountEmail(account, params.cc);
    console.log('📧 发送模板邮件...');
    console.log(`收件人：${account.email}`);
    if (params.cc) console.log(`抄送：${params.cc}`);
    console.log(`✅ 发送成功!`);
    console.log(`Message ID: ${messageId}\n`);
  } catch (error) {
    console.log(`⚠️  邮件发送失败：${error.message}`);
    console.log('   账号已创建成功，请手动发送邮件\n');
    console.log(`📋 订阅地址：${account.subscriptionUrl}\n`);
  }
  
  // 保存日志
  const timestamp = today.toISOString().replace(/[:.]/g, '-').slice(0, -5);
  const logFile = path.join(logMonthDir, `${timestamp}-${params.username}.md`);
  
  const logContent = `# ✅ Remnawave 账号创建记录

**时间:** ${today.toISOString().replace('T', ' ').slice(0, 19)}
**操作员:** Remnawave Robot

## 请求信息

| 参数 | 值 |
|------|-----|
| 用户名 | ${params.username} |
| 邮箱 | ${params.email} |
| 分组 | ${params.squad || '无'} |
| 设备限制 | ${params.deviceLimit} |
| 流量 | ${params.trafficGb}GB |
| 流量重置 | ${params.trafficReset} |
| 过期天数 | ${params.expireDays} |
| 抄送 | ${params.cc || '无'} |

## 结果

**状态:** success
**UUID:** ${account.uuid}
**短 UUID:** ${account.shortUuid}
**订阅地址:** ${account.subscriptionUrl}
**邮件发送:** ${messageId ? '成功' : '失败'}
${messageId ? `**邮件 ID:** ${messageId}` : ''}
`;
  
  fs.writeFileSync(logFile, logContent, 'utf-8');
  console.log(`✅ 日志已保存：${logFile}`);
  console.log('');
  console.log('✅ 全部完成!\n');
}

main().catch((error) => {
  console.error('❌ 错误:', error.message);
  process.exit(1);
});
