#!/bin/bash
# 每日上下班打卡提醒脚本
# 早上提醒时间：09:00
# 晚上提醒时间：18:30

WEBHOOK_KEY="${WEBHOOK_KEY:-}"
if [[ -z "$WEBHOOK_KEY" ]]; then
    echo "警告：未设置 WEBHOOK_KEY 环境变量" >&2
    exit 1
fi

MESSAGE="【温馨提醒】亲爱的同事，请记得：
- 📋 上班打卡（如未打卡）
- 📝 下班打卡（如未打卡）

工作愉快！🌈"

# 发送企业微信群消息
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WEBHOOK_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"$MESSAGE\"}}"

echo "打卡提醒已发送 $(date)" >> ~/openclaw/checkin-reminder.log 2>&1