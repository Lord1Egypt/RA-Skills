#!/usr/bin/env bash
# 澍脉投放驾驶舱查询脚本(只读)。用法: shumai.sh overview|alerts [high|warn|good]|geo
set -euo pipefail
if [ -z "${SHUMAI_API_KEY:-}" ]; then
  echo "未配置 SHUMAI_API_KEY。请到 https://www.shumai.com.cn/admin/ 「设置→API Key」生成后配置环境变量。" >&2
  exit 1
fi
TOOL="${1:-overview}"; LEVEL="${2:-}"
case "$TOOL" in
  overview) NAME=shumai_overview; ARGS='{}' ;;
  alerts)   NAME=shumai_alerts;   ARGS='{}'; [ -n "$LEVEL" ] && ARGS="{\"level\":\"$LEVEL\"}" ;;
  geo)      NAME=shumai_geo_report; ARGS='{}' ;;
  *) echo "用法: shumai.sh overview|alerts [high|warn|good]|geo" >&2; exit 2 ;;
esac
RESP=$(curl -sS --max-time 30 -X POST https://www.shumai.com.cn/mcp \
  -H 'content-type: application/json' \
  -H "Authorization: Bearer $SHUMAI_API_KEY" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$NAME\",\"arguments\":$ARGS}}")
# 优先用 python3 抽取正文;没有 python3 就原样输出 JSON(Agent 自己能读)
echo "$RESP" | python3 -c "import json,sys
d=json.load(sys.stdin)
if 'error' in d: print('错误: '+d['error'].get('message','')); sys.exit(1)
c=(d.get('result',{}).get('content') or [{}])[0].get('text','')
print(c if c else json.dumps(d,ensure_ascii=False))" 2>/dev/null || echo "$RESP"
