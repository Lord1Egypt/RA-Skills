#!/bin/bash
# fetch_data.sh - 获取家清人群宇宙看板数据并保存为 CSV
# 用法: bash fetch_data.sh <workspace_dir> <output_dir>
# 依赖: data-fe-common-sso skill

WORKSPACE="${1:-/home/node/.openclaw/workspace}"
OUTPUT_DIR="${2:-/tmp}"

echo "=== 获取 SSO Cookie ==="
COOKIE=$(bash /app/skills/data-fe-common-sso/script/run-sso.sh "$WORKSPACE" 2>/dev/null)
if [ -z "$COOKIE" ]; then
  echo "ERROR: 获取 Cookie 失败"
  exit 1
fi

echo "=== 查询最新下载任务 ==="
TASKS=$(curl -s -X POST "https://redbi.devops.xiaohongshu.com/api/download/task/list" \
  -H "Cookie: $COOKIE" \
  -H "Content-Type: application/json" \
  -d '{"pageNo":1,"pageSize":20}')

# 提取各分析的最新下载URL
for AID in 42623804 42626327 42701238; do
  URL=$(echo "$TASKS" | python3 -c "
import json,sys
d=json.load(sys.stdin)
tasks=d.get('data',{}).get('downloadTasks',[])
for t in tasks:
    if str(t.get('resourceId','')) == '$AID' and t.get('status') == 'FINISHED':
        print(t.get('fileUrl',''))
        break
" 2>/dev/null)
  if [ -n "$URL" ]; then
    NAME="data_${AID}.csv"
    curl -s "$URL" -H "Cookie: $COOKIE" -o "$OUTPUT_DIR/$NAME"
    echo "下载完成: $NAME ($(wc -l < $OUTPUT_DIR/$NAME) 行)"
  else
    echo "WARN: analysisId=$AID 没有可用的下载任务，请在看板页面手动触发导出"
  fi
done
