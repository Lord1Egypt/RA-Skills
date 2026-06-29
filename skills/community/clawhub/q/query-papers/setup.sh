#!/usr/bin/env bash
# setup.sh — query_papers Skill 安装脚本
set -e
cd "$(dirname "$0")"

echo "[1/3] 安装 Python 依赖..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo "[2/3] 检查 .env 配置..."
if [ ! -f .env ]; then
  cp env-example.txt .env
  echo "  已生成 .env，请编辑填入真实的 GITEA_ADMIN_TOKEN！"
else
  echo "  .env 已存在，跳过。"
fi

echo "[3/3] 自检..."
python3 scripts/kb_read.py --open_id setup_selftest --list all || true

echo ""
echo "安装完成。测试命令："
echo "  python3 scripts/kb_read.py --open_id <你的open_id> --list all"
