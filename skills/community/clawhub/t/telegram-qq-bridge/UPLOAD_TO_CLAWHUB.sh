#!/bin/bash
# Telegram → QQ 技能上传到 ClawHub 的辅助脚本
# 使用方法：bash UPLOAD_TO_CLAWHUB.sh

set -e

SKILL_NAME="telegram-qq-bridge"
SKILL_DIR="/home/raolin/.openclaw/skills/$SKILL_NAME"
TARBALL="$SKILL_DIR.tar.gz"
CLAWHUB_URL="https://clawhub.ai/skills/new"

echo "=========================================="
echo "🚀 上传 $SKILL_NAME 到 ClawHub"
echo "=========================================="
echo ""

# 1. 检查文件
echo "1️⃣  检查发布包..."
if [ ! -f "$TARBALL" ]; then
  echo "❌ 发布包不存在：$TARBALL"
  echo "正在创建发布包..."
  cd /home/raolin/.openclaw/skills/
  tar -czf "$TARBALL" "$SKILL_NAME/"
fi
echo "✅ 发布包存在：$TARBALL"
echo "   大小：$(du -h $TARBALL | cut -f1)"
echo ""

# 2. 显示发布信息
echo "2️⃣  发布信息:"
echo "   名称：$SKILL_NAME"
echo "   版本：1.0.0"
echo "   描述：Telegram → QQ 自动转发技能"
echo "   分类：Communication"
echo "   标签：telegram, qq, forward, bridge, automation, nodejs"
echo ""

# 3. 提供上传选项
echo "3️⃣  选择上传方式:"
echo ""
echo "   方法 A: 使用浏览器上传（推荐）"
echo "   方法 B: 使用 curl 上传（如果 API 支持）"
echo ""

read -p "请选择上传方式 (A/B): " choice

case $choice in
  A|a)
    echo ""
    echo "🌐 正在打开 ClawHub 发布页面..."
    echo ""
    echo "请按以下步骤操作:"
    echo "1. 在浏览器中打开：$CLAWHUB_URL"
    echo "2. 填写以下信息:"
    echo "   - 技能名称：$SKILL_NAME"
    echo "   - 版本号：1.0.0"
    echo "   - 描述：Telegram 群组消息自动转发到 QQ"
    echo "   - 分类：Communication"
    echo "   - 标签：telegram, qq, forward, bridge, automation"
    echo "3. 上传文件：$TARBALL"
    echo "4. 点击'提交审核'或'发布'"
    echo ""
    
    # 尝试打开浏览器
    if command -v xdg-open &> /dev/null; then
      xdg-open "$CLAWHUB_URL"
    elif command -v open &> /dev/null; then
      open "$CLAWHUB_URL"
    else
      echo "请手动打开浏览器访问：$CLAWHUB_URL"
    fi
    ;;
    
  B|b)
    echo ""
    echo "📡 使用 curl 上传..."
    echo ""
    
    # 创建元数据
    cat > /tmp/clawhub-metadata.json <<EOF
{
  "name": "$SKILL_NAME",
  "version": "1.0.0",
  "description": "Telegram → QQ 自动转发技能",
  "author": "OpenClaw Community",
  "license": "MIT",
  "tags": ["telegram", "qq", "forward", "bridge", "automation"],
  "category": "Communication",
  "requirements": {
    "openclaw": ">=2026.5.2",
    "node": ">=14.0.0"
  }
}
EOF
    
    # 上传
    RESPONSE=$(curl -s -X POST \
      -F "metadata=@/tmp/clawhub-metadata.json" \
      -F "file=@$TARBALL" \
      -F "description=Telegram 群组消息自动转发到 QQ，事件驱动，Node.js 实现" \
      "https://clawhub.ai/api/skills" \
      -w "\nHTTP_CODE: %{http_code}")
    
    echo "ClawHub 响应:"
    echo "$RESPONSE"
    
    # 清理
    rm -f /tmp/clawhub-metadata.json
    ;;
    
  *)
    echo "无效选择"
    exit 1
    ;;
esac

echo ""
echo "=========================================="
echo "✅ 发布流程完成"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 等待 ClawHub 审核通过（通常 1-3 个工作日）"
echo "2. 审核通过后会收到通知"
echo "3. 在 ClawHub 查看技能页面"
echo "4. 测试安装：openclaw skill install $SKILL_NAME"
echo ""
