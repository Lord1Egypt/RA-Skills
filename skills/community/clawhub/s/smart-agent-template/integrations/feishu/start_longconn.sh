#!/bin/bash
# 飞书 Bot 启动脚本（自动修复 SSL 问题）

set -e
cd "$(dirname "$0")"

# 检查 .env
if [ ! -f .env ]; then
    echo "❌ 未找到 .env 文件"
    exit 1
fi

# 加载环境变量
export $(grep -v '^#' .env | grep -v '^$' | xargs)

# 检查必需配置
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
    echo "❌ 缺少必需配置"
    exit 1
fi

# 修复 lark-oapi SDK 的 SSL 验证问题
SDK_FILE=$(python3 -c "import lark_oapi.ws.client, inspect; print(inspect.getfile(lark_oapi.ws.client))")
if grep -q "ssl=ssl._create_unverified_context()" "$SDK_FILE"; then
    echo "✅ SDK 已修复 SSL"
else
    echo "🔧 修复 SDK SSL 验证..."
    # 备份
    cp "$SDK_FILE" "${SDK_FILE}.bak" 2>/dev/null || true
    # 修改第 152 行
    python3 <<EOF
import re
with open('$SDK_FILE', 'r') as f:
    content = f.read()
# 在文件开头添加 ssl import（如果没有）
if 'import ssl' not in content[:500]:
    content = 'import ssl\n' + content
# 修改 websockets.connect 调用
content = re.sub(
    r'conn = await websockets\.connect\(conn_url\)',
    'conn = await websockets.connect(conn_url, ssl=ssl._create_unverified_context())',
    content
)
with open('$SDK_FILE', 'w') as f:
    f.write(content)
print('✅ SDK 已修复')
EOF
fi

# 启动 Bot
echo "🚀 启动飞书 Bot..."
python3 bot_longconn.py
