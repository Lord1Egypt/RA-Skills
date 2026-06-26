#!/usr/bin/env node

/**
 * Remnawave Robot - 发送账号开通邮件
 * 
 * 直接复制旧脚本 /root/.openclaw/workspace/config/send-template-email.js
 * 确保与旧脚本完全一致
 * 
 * 用法:
 * node send-account-email.js \
 *   --to jung@bydfi.com \
 *   --cc crads@codeforce.tech \
 *   --subscription-url https://... \
 *   --username jung_pc
 */

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, 'config');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');
const TEMPLATE_DIR = path.join(__dirname, 'templates');

// 解析命令行参数
const args = process.argv.slice(2);
let to = '', cc = '', username = '', subscriptionUrl = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--to' && args[i + 1]) { to = args[++i]; }
  else if (args[i] === '--cc' && args[i + 1]) { cc = args[++i]; }
  else if (args[i] === '--username' && args[i + 1]) { username = args[++i]; }
  else if (args[i] === '--subscription-url' && args[i + 1]) { subscriptionUrl = args[++i]; }
}

if (!to || !username || !subscriptionUrl) {
  console.error('用法：node send-account-email.js --to <邮箱> --username <用户名> --subscription-url <订阅地址> [--cc <抄送>]');
  process.exit(1);
}

// 读取 SMTP 配置
const smtpConfig = JSON.parse(fs.readFileSync(SMTP_CONFIG, 'utf-8'));

// 读取模板
const templatePath = path.join(TEMPLATE_DIR, 'account-created.md');
const templateContent = fs.readFileSync(templatePath, 'utf-8');

// 提取 HTML 和纯文本部分
const htmlMatch = templateContent.match(/### 正文 \(HTML\)\s*\n```html([\s\S]*?)```/);
const textMatch = templateContent.match(/### 正文 \(纯文本\)\s*\n```([\s\S]*?)```/);

let htmlContent, textContent;

if (htmlMatch && textMatch) {
  // 模板包含 HTML 和纯文本部分
  htmlContent = htmlMatch[1].trim();
  textContent = textMatch[1].trim();
} else {
  // 模板是纯 HTML
  htmlContent = templateContent;
  textContent = `账号 ${username} 已创建成功，订阅地址：${subscriptionUrl}`;
}

// 替换变量
const vars = {
  recipient_name: username.split('_')[0] || username,
  recipient_email: to,
  account_name: username,
  subscription_url: subscriptionUrl,
  tutorial_url: 'https://rjdx19yd9zo.sg.larksuite.com/docx/EwMLdN3asoQ44FxOlN6lQ6frgdh?from=from_copylink',
  download_url: 'https://v2raytun.com/',
  download_backup: 'https://testappdownload-bydtmscom.oss-cn-hongkong.aliyuncs.com/OPSFILE/v2RayTun_Setup.zip',
  appstore_url: 'https://apps.apple.com/us/app/v2raytun/id6476628951',
  send_date: new Date().toLocaleString('zh-CN')
};

Object.keys(vars).forEach(key => {
  const regex = new RegExp(`{{${key}}}`, 'g');
  htmlContent = htmlContent.replace(regex, vars[key]);
  textContent = textContent.replace(regex, vars[key]);
});

async function sendEmail() {
  try {
    console.log('📧 发送模板邮件...');
    console.log(`收件人：${to}`);
    if (cc) console.log(`抄送：${cc}`);
    
    const transporter = nodemailer.createTransport({
      host: smtpConfig.host,
      port: smtpConfig.port,
      secure: smtpConfig.secure,
      auth: smtpConfig.auth,
      tls: smtpConfig.tls
    });
    
    const mailOptions = {
      from: `"${smtpConfig.from.name}" <${smtpConfig.from.email}>`,
      to: to,
      subject: `【VPN】账号已创建 - 运维组 Crads`,
      text: textContent,
      html: htmlContent
    };
    
    if (cc) {
      mailOptions.cc = cc;
    }
    
    const info = await transporter.sendMail(mailOptions);
    
    console.log('✅ 发送成功!');
    console.log('Message ID:', info.messageId);
    
    process.exit(0);
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    console.error(error);
    process.exit(1);
  }
}

sendEmail();
