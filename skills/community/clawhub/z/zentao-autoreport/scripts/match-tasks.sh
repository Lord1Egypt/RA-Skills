#!/bin/bash
#
# zentao-autoreport - 获取所有任务并匹配用户描述
# Usage: ./match-tasks.sh "<user_description>"
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

USER_DESC=$1
MATCH_FLAG=$2

if [ -z "$USER_DESC" ]; then
    echo "Usage: $0 \"<user_description>\""
    exit 1
fi

# 如果 ZENTAO_SID 未设置，尝试通过登录获取
if [ -z "$ZENTAO_SID" ]; then
    echo ">>> ZENTAO_SID not set, re-login to get fresh zentaosid..."
    curl -c /tmp/cookies.txt "$ZENTAO_URL/user-login.html" -s > /dev/null
    curl -b /tmp/cookies.txt -c /tmp/cookies.txt "$ZENTAO_URL/index.php?m=user&f=login&t=json" \
      -X POST \
      -d "account=$ZENTAO_ACCOUNT&password=$ZENTAO_PASSWORD&remember=on" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -s > /dev/null

    ZENTAO_SID=$(grep 'zentaosid' /tmp/cookies.txt | tail -1 | awk '{print $7}')
    echo ">>> Got fresh zentaosid: $ZENTAO_SID"
fi

# 获取当前用户所有任务
echo ">>> Fetching all tasks..."
RESPONSE=$(curl -b "zentaosid=$ZENTAO_SID" "$ZENTAO_URL/index.php?m=my&f=task&t=json&onlybody=yes" \
  -H "X-Requested-With: XMLHttpRequest" \
  -s)

# 解析输出，格式化任务列表
echo "$RESPONSE" | python3 -c "
import json
import sys
import re

data = json.loads(open(0).read())
tasks = data.get('data', {}).get('tasks', [])

print(f'# Found {len(tasks)} tasks:')
print()
print('| Task ID | Task Name | Consumed | Left |')
print('|---------|-----------|----------|------|')
for t in tasks:
    tid = t.get('id')
    name = t.get('name', '').replace('|', '\\|')
    consumed = t.get('consumed', '0')
    left = t.get('left', '0')
    print(f'| {tid} | {name} | {consumed}h | {left}h |')
print()
print('## Full task list JSON:')
print('```')
for t in tasks:
    print(f'- {t.get(\"id\")}: {t.get(\"name\")}')
print('```')

# 如果有--match 参数，进行智能匹配
if len(sys.argv) > 1 and sys.argv[1] == '--match':
    user_desc = '''$USER_DESC'''.lower()
    matches = []
    for task in tasks:
        task_name = task.get('name', '').lower()
        score = 0
        desc_words = re.split(r'[\s,,.]+', user_desc)
        for word in desc_words:
            if len(word) > 1 and word in task_name:
                score += 1
        if score > 0:
            matches.append((task, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    print()
    print('>>> Matching tasks...')
    if matches:
        print(f'# Matched {len(matches)} tasks:')
        for task, score in matches:
            print(f'- Task {task.get(\"id\")}: {task.get(\"name\")} (score: {score})')
    else:
        print('# No matching tasks found')
" $MATCH_FLAG
