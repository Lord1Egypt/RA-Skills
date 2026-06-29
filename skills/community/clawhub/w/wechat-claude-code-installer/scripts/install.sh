#!/usr/bin/env bash
# install.sh —— 一键装 wechat-claude-code（包含 clone + npm install + setup 灌答案）
set -euo pipefail

WORK_DIR="${1:-$HOME/Claude Code}"

echo "============================================================"
echo "  wechat-claude-code-installer :: 一键安装"
echo "============================================================"
echo "  Claude Code 工作目录: $WORK_DIR"
echo ""

# 1. 体检（必须先过）
"$(dirname "$0")/doctor.sh"
echo ""
read -p "继续吗？(y/N) " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
  echo "已取消。"
  exit 0
fi

# 2. clone
TARGET=~/.claude/skills/wechat-claude-code
if [ -d "$TARGET" ]; then
  echo "⚠️  $TARGET 已存在，跳过 clone"
else
  echo ""
  echo "📦 Clone 上游项目..."
  GH_HOST=github.com git clone https://github.com/Wechat-ggGitHub/wechat-claude-code.git "$TARGET"
fi

# 3. npm install
echo ""
echo "📦 npm install..."
cd "$TARGET"
npm install --silent

# 4. 准备工作目录
mkdir -p "$WORK_DIR"

# 5. 跑 setup 灌答案
echo ""
echo "🔍 启动 setup（会弹出二维码图片）..."
echo "   请用微信扫码并确认绑定。"
echo ""
echo "$WORK_DIR" | npm run setup
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "❌ setup 失败（exit $EXIT_CODE）。"
  exit $EXIT_CODE
fi

echo ""
echo "✅ 安装完成。"

# v0.3 新增：自动 pin 当前上游 commit（基线，方便后续检测漂移）
CHECK="$(dirname "$0")/check-upstream.sh"
if [ -x "$CHECK" ]; then
  "$CHECK" --pin || true
fi

echo ""
echo "下一步："
echo "  1. 跑 fix-cwd.sh \"$WORK_DIR\"          修复 cwd 僵尸字段"
echo "  2. 跑 fix-meta-talk.sh                关闭 hook 元话术泄露"
echo "  3. 跑 fix-caffeinate.sh               加防闲置睡眠"
echo "  4. cd $TARGET && npm run daemon -- start  起 daemon"
echo ""
echo "或者直接跑 fix-all.sh \"$WORK_DIR\" 一次完成 1+2+3。"
echo ""
echo "💡 上游有快速迭代，建议每周跑一次："
echo "   check-upstream.sh        看本地 vs 远程是否漂移"
echo "   check-upstream.sh --since 看 pin 以来上游加了哪些 commit"
