#!/bin/bash
# ============================================================
# 飞书周报发送脚本
# 使用方式：./send-to-feishu.sh [周报文件路径]
# ============================================================

# ---- 配置区（首次使用请填写以下内容）----
APP_ID="your_app_id"           # 飞书应用 App ID
APP_SECRET="your_app_secret"   # 飞书应用 App Secret
RECEIVE_ID="your_open_id"      # 接收者的 open_id
# -----------------------------------------

REPORT_FILE="${1:-/Users/ai/cline-skills/$(ls /Users/ai/cline-skills/weekly-report-*.md 2>/dev/null | sort | tail -1 | xargs basename 2>/dev/null)}"

# 检查配置
if [[ -z "$APP_ID" || -z "$APP_SECRET" || -z "$RECEIVE_ID" ]]; then
  echo "❌ 请先配置飞书凭证！"
  echo ""
  echo "  编辑此脚本，填写以下三项："
  echo "  APP_ID       - 飞书应用的 App ID"
  echo "  APP_SECRET   - 飞书应用的 App Secret"
  echo "  RECEIVE_ID   - 你的飞书 open_id"
  echo ""
  echo "  获取方式请参考：飞书集成说明.md"
  exit 1
fi

# 检查周报文件
if [[ -z "$REPORT_FILE" || ! -f "$REPORT_FILE" ]]; then
  echo "❌ 找不到周报文件：$REPORT_FILE"
  echo "  请指定文件路径：./send-to-feishu.sh /path/to/weekly-report.md"
  exit 1
fi

echo "📄 读取周报文件：$REPORT_FILE"

# Step 1: 获取 tenant_access_token
echo "🔑 获取飞书访问令牌..."
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tenant_access_token',''))" 2>/dev/null)

if [[ -z "$TOKEN" ]]; then
  echo "❌ 获取令牌失败！请检查 APP_ID 和 APP_SECRET 是否正确。"
  echo "   返回内容：$TOKEN_RESPONSE"
  exit 1
fi
echo "✅ 令牌获取成功"

# Step 2: 构建消息内容（使用 python 生成完整的 JSON）
echo "📤 发送周报到飞书..."

# 导出环境变量供 Python 使用
export REPORT_FILE
export RECEIVE_ID
export TOKEN

# 使用 Python 脚本读取文件并发送
SEND_RESPONSE=$(python3 << 'PYTHON_SCRIPT'
# -*- coding: utf-8 -*-
import sys, json, os
import urllib.request

# 从环境变量读取参数
report_file = os.environ.get('REPORT_FILE')
receive_id = os.environ.get('RECEIVE_ID')
token = os.environ.get('TOKEN')

# 读取周报内容（限制3000字符）
with open(report_file, 'r', encoding='utf-8') as f:
    report_content = f.read()[:3000]

# 构建请求体
payload = {
    'receive_id': receive_id,
    'msg_type': 'text',
    'content': json.dumps({'text': report_content}, ensure_ascii=False)
}

# 发送请求
req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
    data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print(json.dumps({'code': -1, 'msg': str(e)}))
PYTHON_SCRIPT
)

CODE=$(echo "$SEND_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('code','-1'))" 2>/dev/null)

if [[ "$CODE" == "0" ]]; then
  echo "✅ 周报发送成功！"
  echo "   文件：$REPORT_FILE"
else
  echo "❌ 发送失败！"
  echo "   返回内容：$SEND_RESPONSE"
  exit 1
fi
