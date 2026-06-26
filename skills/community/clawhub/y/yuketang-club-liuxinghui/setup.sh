#!/bin/bash
set -e

MCP_URL="https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse"
SECRET_URL="https://ykt-env-example.rainclassroom.com/ai-workspace/open-claw-skill"

# ── 计时 ──
now_ms() {
  # GNU coreutils
  ts=$(date +%s%3N 2>/dev/null)
  case "$ts" in *N*|"") ;; *) echo "$ts"; return ;; esac
  # Python fallback
  if command -v python3 >/dev/null 2>&1; then
    python3 -c 'import time; print(int(time.time()*1000))'; return
  fi
  echo $(( $(date +%s) * 1000 ))
}

START=$(now_ms)

echo "🚀 设置雨课堂 Skill..."
echo ""

# ── 1. 检查 Secret ──
if [ -z "$YUKETANG_SECRET" ]; then
    echo "❌ 未检测到 YUKETANG_SECRET 环境变量"
    echo ""
    echo "请先获取 Secret：$SECRET_URL"
    echo ""
    echo "然后用以下任一方式运行："
    echo "  export YUKETANG_SECRET=\"你的Secret\""
    echo "  bash setup.sh"
    echo ""
    echo "  # 或一行搞定："
    echo "  YUKETANG_SECRET=\"你的Secret\" bash setup.sh"
    exit 1
fi
echo "✅ YUKETANG_SECRET 已配置"
echo ""

# ── 2. 注册 MCP 服务 ──
AUTHORIZATION="Bearer $YUKETANG_SECRET"

register_with_mcporter() {
  npx mcporter config add yuketang-mcp \
    --url "https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse" \
    --header "Authorization=$AUTHORIZATION" \
    --scope project
}

print_manual_config() {
  echo ""
  echo "─────────────────────────────────────"
  echo "📋 请手动将以下配置添加到你的 MCP 客户端配置文件中："
  echo ""
  echo "{"
  echo "  \"mcpServers\": {"
  echo "    \"yuketang-mcp\": {"
  echo "      \"url\": \"https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse\","
  echo "      \"headers\": {"
  echo "        \"Authorization\": \"Bearer \${YUKETANG_SECRET}\""
  echo "      }"
  echo "    }"
  echo "  }"
  echo "}"
  echo ""
  echo "常见配置文件位置："
  echo "  OpenClaw  → 项目根目录 .mcp/config.json"
  echo "  Cursor    → 项目根目录 .cursor/mcp.json"
  echo "  CodeBuddy → 参考 CodeBuddy 文档"
  echo "─────────────────────────────────────"
}

if command -v npx >/dev/null 2>&1; then
  echo "🔧 通过 mcporter 注册服务..."
  if register_with_mcporter; then
    echo "✅ 注册成功"
  else
    echo "⚠️  mcporter 注册失败，请手动配置 ↓"
    print_manual_config
  fi
else
  echo "⚠️  未检测到 npx，请手动配置 ↓"
  print_manual_config
fi

echo ""

# ── 3. 验证 ──
if command -v npx >/dev/null 2>&1; then
  echo "🧪 验证配置..."
  if npx mcporter list 2>&1 | grep -q "yuketang-mcp"; then
    echo "✅ 验证通过"
    npx mcporter list | grep -A 1 "yuketang-mcp" || true
  else
    echo "⚠️  验证未通过，但配置可能已写入"
    echo "   你可以直接尝试使用，如果失败请检查 Secret 是否正确"
  fi
fi

# ── 4. 上报（静默） ──
END=$(now_ms)
DURATION=$((END - START))
if command -v npx >/dev/null 2>&1; then
  npx mcporter call yuketang-mcp claw_report \
    --args "{\"payload\":{\"durationMs\":${DURATION}},\"action\":\"install\"}" \
    >/dev/null 2>&1 || true
fi

echo ""
echo "─────────────────────────────────────"
echo "🎉 设置完成！"
echo "   试试对 AI 说：「我的雨课堂ID是多少」"
echo "─────────────────────────────────────"
