#!/usr/bin/env node

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const SMTP_CONFIG = path.join(__dirname, 'config/smtp.json');
const TEMPLATE_DIR = path.join(__dirname, 'templates');

const smtpConfig = JSON.parse(fs.readFileSync(SMTP_CONFIG, 'utf-8'));

console.log('📧 测试邮件发送...\n');

const transporter = nodemailer.createTransport({
  host: smtpConfig.host,
  port: smtpConfig.port,
  secure: smtpConfig.secure,
  auth: smtpConfig.auth,
  tls: smtpConfig.tls
});

const template = fs.readFileSync(path.join(TEMPLATE_DIR, 'account-created.md'), 'utf-8');
const htmlContent = template
  .replace('{{recipient_name}}', 'jung')
  .replace('{{account_name}}', 'jung_pc')
  .replace('{{subscription_url}}', 'https://46force235a-6cb1-crypto-link.datat.cc/api/sub/wBMXavTEzFbxxY57')
  .replace('{{tutorial_url}}', 'https://example.com/tutorial')
  .replace('{{send_date}}', new Date().toLocaleString('zh-CN'));

const mailOptions = {
  from: smtpConfig.from,
  to: 'jung@bydfi.com',
  cc: 'crads@codeforce.tech',
  subject: 'Remnawave 账号开通通知 - jung_pc',
  html: htmlContent
};

transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    console.log('❌ 邮件发送失败:', error.message);
    console.log('错误代码:', error.code);
    console.log('响应:', error.response);
  } else {
    console.log('✅ 邮件发送成功!');
    console.log('Message ID:', info.messageId);
  }
  process.exit(0);
});
