#!/bin/bash
#
# zentao-autoreport - 自动记录一条工时
# Usage: ./report.sh <task_id> <consumed> "<work_desc>" [date]
#

set -e

# 加载配置
CONFIG_FILE="$HOME/.config/zentao/.env"
if [ -f "$CONFIG_FILE" ]; then
    export $(cat "$CONFIG_FILE" | xargs)
else
    echo "ERROR: Config file $CONFIG_FILE not found"
    exit 1
fi

TASK_ID=$1
CONSUMED=$2
WORK_DESC=$3
DATE=${4:-$(date +%Y-%m-%d)}

if [ -z "$TASK_ID" ] || [ -z "$CONSUMED" ] || [ -z "$WORK_DESC" ]; then
    echo "Usage: $0 <task_id> <consumed> \"<work_desc>\" [date]"
    exit 1
fi

# 重新登录获取最新有效的zentaosid
echo ">>> Re-login to get fresh zentaosid..."
curl -c /tmp/cookies.txt "$ZENTAO_URL/user-login.html" -s > /dev/null
curl -b /tmp/cookies.txt -c /tmp/cookies.txt "$ZENTAO_URL/index.php?m=user&f=login&t=json" \
  -X POST \
  -d "account=$ZENTAO_ACCOUNT&password=$ZENTAO_PASSWORD&remember=on" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -s > /dev/null

ZENTAO_SID=$(grep 'zentaosid' /tmp/cookies.txt | tail -1 | awk '{print $7}')
echo ">>> Got fresh zentaosid: $ZENTAO_SID"

# 获取当前任务信息，计算新的left
echo ">>> Getting task info for $TASK_ID..."
TASK_INFO=$(curl "$ZENTAO_URL/api.php/v1/tasks/$TASK_ID" \
  -H "Token: $ZENTAO_TOKEN" -s)

CURRENT_LEFT=$(echo "$TASK_INFO" | python3 -c "
import json
data = json.loads(open(0).read())
print(data.get('left', '0'))
")

CURRENT_CONSUMED=$(echo "$TASK_INFO" | python3 -c "
import json
data = json.loads(open(0).read())
print(data.get('consumed', '0'))
")

NEW_LEFT=$(echo "$CURRENT_LEFT - $CONSUMED" | bc -l)
NEW_CONSUMED=$(echo "$CURRENT_CONSUMED + $CONSUMED" | bc -l)

# 去掉小数后面的多余0
NEW_LEFT=$(printf "%.1f" "$NEW_LEFT" | sed 's/\.0$//')
NEW_CONSUMED=$(printf "%.1f" "$NEW_CONSUMED" | sed 's/\.0$//')

echo ">>> Current: consumed=$CURRENT_CONSUMED, left=$CURRENT_LEFT"
echo ">>> New: consumed=$NEW_CONSUMED, left=$NEW_LEFT"

# 调用recordworkhour接口记录
echo ">>> Recording... date=$DATE, consumed=$CONSUMED, left=$NEW_LEFT"

RESPONSE=$(curl -X POST "$ZENTAO_URL/index.php?m=task&f=recordworkhour&taskID=$TASK_ID" \
  -H "Content-Type: multipart/form-data" \
  -H "X-Requested-With: XMLHttpRequest" \
  -b "zentaosid=$ZENTAO_SID" \
  -F "date[0]=$DATE" \
  -F "consumed[0]=$CONSUMED" \
  -F "left[0]=$NEW_LEFT" \
  -F "work[0]=$WORK_DESC" \
  -s)

echo ">>> Response: $RESPONSE"

# 检查结果
if echo "$RESPONSE" | grep -q '"result":"success"'; then
    echo "✅ SUCCESS: Recorded successfully!"
    echo "RESULT: task=$TASK_ID, consumed=$CONSUMED, date=$DATE, work=\"$WORK_DESC\""
    echo "UPDATED: consumed=$NEW_CONSUMED, left=$NEW_LEFT"
    exit 0
else
    echo "❌ FAILED: $RESPONSE"
    exit 1
fi
