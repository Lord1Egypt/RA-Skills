#!/data/data/com.termux/files/usr/bin/env bash
# TDX Formula Master — 安装依赖
set -e

echo "📈 TDX Formula Master — 安装依赖"
echo "══════════════════════════════════"

echo ""
echo "📦 Node 运行时..."
if command -v node &>/dev/null; then
  echo "  ✅ Node.js $(node -v)"
else
  echo "  ⚠️ 需要 Node.js: https://nodejs.org"
fi

echo ""
echo "✅ 无需额外依赖，脚本开箱即用"
echo ""
echo "使用:"
echo "  node scripts/formula-validator.js check \"CROSS(MA(C,5),MA(C,10)) AND VOL>REF(VOL,1);\""
echo "  node scripts/formula-validator.js gen \"均线金叉放量\""
echo "  node scripts/formula-validator.js list"