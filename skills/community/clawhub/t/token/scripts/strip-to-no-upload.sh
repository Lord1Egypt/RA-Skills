#!/usr/bin/env bash
# =============================================================================
# strip-to-no-upload.sh — 从「有上报版」生成「无上报版」发布包
#
# 用法：
#   bash scripts/strip-to-no-upload.sh [output_zip_path]
#
# 示例：
#   bash scripts/strip-to-no-upload.sh
#   bash scripts/strip-to-no-upload.sh /tmp/llm-token-compressor-no-upload-v1.8.0.zip
#
# 输出：
#   {skill_dir}/llm-token-compressor-no-upload-v{X.Y.Z}.zip
#
# 不消耗积分：本脚本只做本地文件操作，不调用任何 API
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 读取版本号
VERSION=$(grep -E '^version:' "$SKILL_DIR/SKILL.md" | head -1 | sed 's/.*"\(.*\)".*/\1/')
NO_UPLOAD_VERSION="${VERSION}"
OUTPUT_NAME="llm-token-compressor-no-upload-v${NO_UPLOAD_VERSION}.zip"
OUTPUT_PATH="${1:-$SKILL_DIR/$OUTPUT_NAME}"

echo "🔧 开始生成无上报版发布包"
echo "   源目录：$SKILL_DIR"
echo "   版本：v${NO_UPLOAD_VERSION}"
echo ""

# ── Step 1：创建临时工作目录 ───────────────────────────────────────────────
TMP_DIR=$(mktemp -d)
WORK_DIR="$TMP_DIR/llm-token-compressor-no-upload"
mkdir -p "$WORK_DIR"

echo "📁 临时工作目录：$WORK_DIR"

# ── Step 2：用 rsync 复制（排除 .git、旧 ZIP、上报脚本）──────────────────
rsync -av \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='llm-token-compressor-no-upload-*.zip' \
  --exclude='llm-token-compressor-v*.zip' \
  "$SKILL_DIR/" "$WORK_DIR/"

echo "   ✅ 文件复制完成"

# 删除工作目录里可能存在的旧版 ZIP（rsync exclude 可能没生效）
rm -f "$WORK_DIR"/*.zip

# ── Step 3：删除上报相关脚本 ─────────────────────────────────────────────
rm -f "$WORK_DIR/scripts/headroom_upload.py"
rm -f "$WORK_DIR/scripts/opc_headroom_reporter.py"
rm -f "$WORK_DIR/scripts/install_and_verify.sh"
rm -f "$WORK_DIR/scripts/strip-skill-md.py"  # 构建时用，不打包进发布包
echo "   ✅ 已删除上报相关脚本"

# ── Step 4：裁剪 SKILL.md（去掉所有上报相关内容）────────────────────────
python3 "$SCRIPT_DIR/strip-skill-md.py" "$WORK_DIR/SKILL.md" "$WORK_DIR/SKILL.md.tmp"
mv "$WORK_DIR/SKILL.md.tmp" "$WORK_DIR/SKILL.md"

# 验证：检查是否还有上报关键词
REMAINING=$(grep -c "上报\|mrkjai\|MRKJAI" "$WORK_DIR/SKILL.md" 2>/dev/null || true)
if [ "$REMAINING" -gt 0 ]; then
    echo "   ⚠️  警告：SKILL.md 仍含 ${REMAINING} 处「上报」关键词，请手动检查"
    grep -n "上报\|mrkjai\|MRKJAI" "$WORK_DIR/SKILL.md"
else
    echo "   ✅ SKILL.md 已完全去除上报内容（0 处残留）"
fi

# ── Step 5：修改 SKILL.md 头部（version + description）──────────────────
python3 << PYEOF
import re

with open("$WORK_DIR/SKILL.md", "r", encoding="utf-8") as f:
    content = f.read()

# 修改 description：去掉上报相关描述，加「完全本地运行」
old = '内置一键安装脚本、企业内网适配方案、压缩效果对比报告、场景专项配置（法律/医疗/金融/代码）、模型更新指南，以及可选的数据上报功能（可随时关闭，首次使用引导用户选择）。基于开源项目'
new = '内置一键安装脚本、企业内网适配方案、压缩效果对比报告、场景专项配置（法律/医疗/金融/代码）、模型更新指南。完全本地运行，不向任何外部服务器发送数据。基于开源项目'
content = content.replace(old, new)

with open("$WORK_DIR/SKILL.md", "w", encoding="utf-8") as f:
    f.write(content)

print("   ✅ SKILL.md description 已更新（无上报版）")
PYEOF

# ── Step 6：打包 ZIP ─────────────────────────────────────────────────────
cd "$TMP_DIR"
zip -r "$OUTPUT_PATH" "llm-token-compressor-no-upload/" \
    -x "*.DS_Store" \
    -x "__pycache__/*" \
    -x "scripts/strip-skill-md.py"

echo ""
echo "✅ 无上报版发布包已生成："
echo "   $OUTPUT_PATH"
echo ""
echo "📦 包内容："
unzip -l "$OUTPUT_PATH"

echo ""
echo "🚀 下一步："
echo "   1. 登录虾评：https://xiaping.coze.com"
echo "   2. 找到「大模型token成本节约」→ 点击「更新版本」"
echo "   3. 上传 $OUTPUT_PATH"
echo "   4. 版本号：v${NO_UPLOAD_VERSION}"
echo "   5. 更新说明："
echo "      - 内置定价表（自动识别模型，无需手动传 --pricing）"
echo "      - 新增场景专项配置（法律/医疗/金融/代码，含推荐 target_ratio）"
echo "      - 新增模型与定价表更新章节"
echo "      - 完全本地运行，不上报任何数据"

# 清理临时目录
rm -rf "$TMP_DIR"
