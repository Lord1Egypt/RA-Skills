#!/usr/bin/env node

/**
 * Remnawave Robot - 补发邮件
 * 
 * 用途：当创建账号邮件发送失败时，手动补发
 * 
 * 用法:
 * node resend-email.js --username jung_pc --email jung@bydfi.com --subscription-url https://... --cc crads@codeforce.tech
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, 'config');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');
const TEMPLATE_DIR = path.join(__dirname, 'templates');

// 解析命令行参数
const args = process.argv.slice(2);
const params = {
  username: null,
  email: null,
  subscriptionUrl: null,
  cc: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) params.username = args[++i];
  else if (args[i] === '--email' && args[i + 1]) params.email = args[++i];
  else if (args[i] === '--subscription-url' && args[i + 1]) params.subscriptionUrl = args[++i];
  else if (args[i] === '--cc' && args[i + 1]) params.cc = args[++i];
}

if (!params.username || !params.email || !params.subscriptionUrl) {
  console.error('❌ 错误：缺少必填参数');
  console.error('用法：node resend-email.js --username <用户名> --email <邮箱> --subscription-url <订阅地址> [--cc <抄送>]');
  process.exit(1);
}

const smtpConfig = JSON.parse(fs.readFileSync(SMTP_CONFIG, 'utf-8'));

console.log('📧 补发开通邮件...\n');
console.log(`收件人：${params.email}`);
console.log(`账号：${params.username}`);
console.log(`订阅：${params.subscriptionUrl}`);
if (params.cc) console.log(`抄送：${params.cc}`);
console.log('');

const transporter = nodemailer.createTransport({
  host: smtpConfig.host,
  port: smtpConfig.port,
  secure: smtpConfig.secure,
  auth: smtpConfig.auth,
  tls: smtpConfig.tls
});

const template = fs.readFileSync(path.join(TEMPLATE_DIR, 'account-created.md'), 'utf-8');
const htmlContent = template
  .replace('{{recipient_name}}', params.username.split('_')[0] || params.username)
  .replace('{{account_name}}', params.username)
  .replace('{{subscription_url}}', params.subscriptionUrl)
  .replace('{{tutorial_url}}', 'https://example.com/tutorial')
  .replace('{{send_date}}', new Date().toLocaleString('zh-CN'));

const mailOptions = {
  from: `"${smtpConfig.from.name}" <${smtpConfig.from.email}>`,
  to: params.email,
  cc: params.cc,
  subject: `【VPN】账号已创建 - 运维组 Crads`,
  text: `账号 ${params.username} 已创建成功，订阅地址：${params.subscriptionUrl}`,
  html: htmlContent
};

transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    console.log('❌ 邮件发送失败:', error.message);
    console.log('');
    console.log('💡 建议:');
    console.log('   1. 检查 SMTP 配置是否正确');
    console.log('   2. 验证邮箱密码是否过期');
    console.log('   3. 手动发送邮件到:', params.email);
    console.log('');
    console.log('📋 账号信息:');
    console.log(`   订阅地址：${params.subscriptionUrl}`);
    process.exit(1);
  } else {
    console.log('✅ 邮件发送成功!');
    console.log(`Message ID: ${info.messageId}`);
    console.log('');
    console.log('📋 已发送:');
    console.log(`   收件人：${params.email}`);
    if (params.cc) console.log(`   抄送：${params.cc}`);
  }
  process.exit(0);
});
