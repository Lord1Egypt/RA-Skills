#!/bin/bash

# Zoho SMTP 修复脚本
# 用途：检查和修复 Zoho SMTP 配置问题

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Zoho SMTP 修复工具                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

SMTP_CONFIG="/root/.openclaw/workspace/skills/remnawave-robot/config/smtp.json"

echo "📋 当前 SMTP 配置:"
echo ""
cat $SMTP_CONFIG
echo ""

echo "🔍 检查项目:"
echo ""

# 检查 1: 配置文件是否存在
if [ -f "$SMTP_CONFIG" ]; then
    echo "✅ 配置文件存在"
else
    echo "❌ 配置文件不存在"
    exit 1
fi

# 检查 2: 权限是否正确
PERMS=$(stat -c %a $SMTP_CONFIG 2>/dev/null || stat -f %A $SMTP_CONFIG)
if [ "$PERMS" = "600" ]; then
    echo "✅ 文件权限正确 (600)"
else
    echo "⚠️  文件权限：$PERMS (建议：600)"
    chmod 600 $SMTP_CONFIG
    echo "✅ 已修复权限为 600"
fi

# 检查 3: 测试 Node.js 连接
echo ""
echo "🧪 测试 SMTP 连接..."
cd /root/.openclaw/workspace/skills/remnawave-robot
node -e "
const nodemailer = require('nodemailer');
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('config/smtp.json', 'utf-8'));

const transporter = nodemailer.createTransport({
  host: config.host,
  port: config.port,
  secure: config.secure,
  auth: config.auth,
  tls: config.tls
});

transporter.verify((error, success) => {
  if (error) {
    console.log('❌ SMTP 连接失败:', error.message);
    console.log('');
    console.log('可能原因:');
    console.log('  1. 邮箱密码错误或已过期');
    console.log('  2. SMTP 权限未开启');
    console.log('  3. 发件人邮箱未验证');
    console.log('');
    console.log('解决方案:');
    console.log('  1. 登录 https://mail.zoho.com 重置密码');
    console.log('  2. 设置 → 邮件 → POP/IMAP → 启用 SMTP');
    console.log('  3. 或使用应用专用密码');
    process.exit(1);
  } else {
    console.log('✅ SMTP 连接成功!');
    process.exit(0);
  }
});
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SMTP 配置正确！"
    echo ""
    echo "📧 测试发送邮件..."
    node test-email.js
else
    echo ""
    echo "❌ SMTP 配置有问题"
    echo ""
    echo "📋 请按以下步骤修复:"
    echo ""
    echo "1. 登录 Zoho Mail: https://mail.zoho.com"
    echo "2. 设置 → 安全 → 更改密码（或使用应用专用密码）"
    echo "3. 设置 → 邮件 → POP/IMAP → 确保启用 SMTP"
    echo "4. 更新密码后运行：node test-config.js"
    echo ""
fi

echo ""
echo "══════════════════════════════════════════════════════════"
