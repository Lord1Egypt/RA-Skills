#!/bin/bash
# JWT 过期检查脚本
# 用法：./check_jwt.sh [cookies文件路径]
# 默认：.lovart_cookies.json

COOKIES_FILE="${1:-.lovart_cookies.json}"

if [ ! -f "$COOKIES_FILE" ]; then
    echo "❌ 未找到 cookies 文件: $COOKIES_FILE"
    echo "请先获取 Lovart cookies 并保存为 JSON 文件"
    exit 1
fi

node -e "
const fs = require('fs');
const cookies = JSON.parse(fs.readFileSync('$COOKIES_FILE', 'utf8'));
const token = cookies.find(c => c.name === 'usertoken');
if (!token) { console.log('❌ 未找到 usertoken cookie'); process.exit(1); }
try {
    const payload = JSON.parse(Buffer.from(token.value.split('.')[1], 'base64').toString());
    const exp = new Date(payload.exp * 1000);
    const now = new Date();
    const hoursLeft = (exp - now) / 3600000;
    console.log('📋 Cookies 文件:', '$COOKIES_FILE');
    console.log('⏰ JWT 过期时间:', exp.toISOString());
    console.log('⏳ 剩余时间:', hoursLeft.toFixed(1), '小时');
    if (hoursLeft <= 0) {
        console.log('❌ JWT 已过期！需要重新登录 Lovart 并提供新 cookies');
        process.exit(1);
    } else if (hoursLeft <= 24) {
        console.log('⚠️  JWT 将在 24 小时内过期，建议尽快更新');
    } else {
        console.log('✅ JWT 有效');
    }
} catch (e) {
    console.log('❌ JWT 解析失败:', e.message);
    process.exit(1);
}
"
