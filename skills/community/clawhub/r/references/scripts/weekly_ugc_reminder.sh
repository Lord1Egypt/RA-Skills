#!/bin/bash
# 每周 UGC 数据收集提醒脚本
# 触发时间：每周周一上午 10:00

WEEKDAY=$(date +%u)  # 1=周一, 7=周日
CURRENT_HOUR=$(date +%H)
CURRENT_MINUTE=$(date +%M)

if [[ $WEEKDAY -ne 1 ]] || [[ $CURRENT_HOUR -lt 10 ]] || [[ $CURRENT_HOUR -eq 10 && $CURRENT_MINUTE -lt 45 ]]; then
    exit 0
fi

MESSAGE="各位好，请提供上周 UGC 数据给我。数据格式自行整理即可，收到后会统一汇总。谢谢！"

# 发送企业微信群消息
curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5cf9f411-d581-41ab-a899-304a418bb176" \
  -H "Content-Type: application/json" \
  -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"$MESSAGE\"}}"

echo "UGC 数据收集提醒已发送"