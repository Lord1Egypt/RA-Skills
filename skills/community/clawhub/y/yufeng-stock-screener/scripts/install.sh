#!/bin/bash
# =====================================================
# 禹锋量化 A股选股 Skill 一键安装脚本
# =====================================================

echo "========================================"
echo "  禹锋量化 Skill 安装"
echo "========================================"

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi
echo "[✓] Python 已安装: $(python3 --version)"

# 2. 安装依赖
echo "[*] 安装依赖..."
pip3 install requests --quiet 2>/dev/null || python3 -m pip install requests --quiet
echo "[✓] 依赖安装完成"

# 3. 创建 Skill 目录
SKILL_DIR="$HOME/.workbuddy/skills/a-stock-quant-screener"
mkdir -p "$SKILL_DIR/scripts"

# 4. 复制文件
echo "[*] 复制 Skill 文件..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp -r "$SCRIPT_DIR/../skill/"* "$SKILL_DIR/"
echo "[✓] Skill 安装完成"

# 5. 配置 Token
echo ""
echo "========================================"
echo "  配置 Token"
echo "========================================"
read -p "请输入你的 API Token（直接回车跳过）: " USER_TOKEN
if [ -n "$USER_TOKEN" ]; then
    echo "export YUFENG_QUANT_TOKEN=\"$USER_TOKEN\"" >> ~/.bashrc
    export YUFENG_QUANT_TOKEN="$USER_TOKEN"
    echo "[✓] Token 已配置到 ~/.bashrc"
else
    echo "[*] 未配置 Token，使用时需通过 --token 参数传递"
fi

echo ""
echo "========================================"
echo "  安装完成！"
echo "========================================"
echo ""
echo "使用方式："
echo "  python3 ~/.workbuddy/skills/a-stock-quant-screener/scripts/query_stocks.py \\"
echo "    --action screen --token YOUR_TOKEN"
echo ""
echo "支持的 action："
echo "  screen   - 今日选股"
echo "  analyze  - 个股分析（需 --code）"
echo "  sector   - 热门板块"
echo "  timing   - 择时评分（需 --code）"
echo "  status   - 查询 Token 状态"
echo ""