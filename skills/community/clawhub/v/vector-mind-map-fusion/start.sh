#!/bin/bash
# Vector-Mind Map-Fusion 一键启动脚本

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "Vector-Mind Map-Fusion 启动脚本"
echo "=========================================="

# 加载环境变量
if [ -f .env ]; then
    echo "[启动] 加载 .env 配置"
    export $(cat .env | grep -v '^#' | xargs)
fi

# 检查依赖
if [ ! -f requirements.txt ]; then
    echo "[错误] requirements.txt 不存在"
    exit 1
fi

# 安装依赖（如果需要）
if ! python3 -c "import httpx" 2>/dev/null; then
    echo "[启动] 安装 Python 依赖..."
    pip install -r requirements.txt -q
fi

# 创建必要的目录
mkdir -p memory/layers/l2a memory/layers/l2 memory/layers/hnsw memory/layers/infinitydb logs

# 显示菜单
echo ""
echo "请选择操作:"
echo "  1. 运行全部 (L1 + L2 + L3)"
echo "  2. 运行 L1 提取层"
echo "  3. 运行 L2 整理层"
echo "  4. 运行 L3 检索层"
echo "  5. 搜索记忆"
echo "  6. 查看系统状态"
echo "  0. 退出"
echo ""

read -p "请输入选项 [1-6, 0退出]: " choice

case "$choice" in
    1)
        echo "[启动] 运行全部层..."
        python3 main.py run --all
        ;;
    2)
        echo "[启动] 运行 L1..."
        python3 main.py run --layer l1
        ;;
    3)
        echo "[启动] 运行 L2..."
        python3 main.py run --layer l2
        ;;
    4)
        echo "[启动] 运行 L3..."
        python3 main.py run --layer l3
        ;;
    5)
        read -p "请输入搜索内容: " query
        python3 main.py search "$query"
        ;;
    6)
        python3 main.py stats
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo "[错误] 无效选项"
        exit 1
        ;;
esac

echo "[完成] 操作完成"