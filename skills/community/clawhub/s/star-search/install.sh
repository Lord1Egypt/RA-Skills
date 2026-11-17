#!/bin/bash
# star-search 一键安装脚本
# 用法: bash install.sh

set -e

echo "=========================================="
echo "  star-search 一键安装"
echo "=========================================="
echo ""

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3.10+: https://www.python.org/downloads/"
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")")
echo "✓ 检测到 Python $PY_VERSION"

# 2. 安装依赖
echo ""
echo "[1/4] 安装 Python 依赖..."
pip3 install --user --quiet     fastapi uvicorn pydantic httpx aiohttp lxml     python-multipart aiosqlite 2>&1 | tail -3 || {
    echo "❌ 依赖安装失败"
    exit 1
}
echo "✓ 依赖安装完成"

# 3. 配置 .env
echo ""
echo "[2/4] 配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ 已创建 .env 文件 (请编辑填入你的 LLM API key)"
    echo ""
    echo "必须修改的配置:"
    echo "  LLM_API_KEY=你的key"
    echo "  LLM_BASE_URL=https://api.openai.com/v1  (或你的 OpenAI 兼容端点)"
else
    echo "✓ .env 已存在, 跳过"
fi

# 4. 安装 Playwright (可选, fetch_content 用)
echo ""
echo "[3/4] 安装 Playwright 浏览器 (约 200MB)..."
read -p "是否安装? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip3 install --user --quiet playwright 2>&1 | tail -3
    python3 -m playwright install chromium 2>&1 | tail -5
    echo "✓ Playwright 安装完成"
else
    echo "⊘ 跳过 Playwright (fetch_content 高级功能不可用, 但核心搜索仍可工作)"
fi

# 5. 启动服务
echo ""
echo "[4/4] 启动服务..."
echo ""
echo "选择启动方式:"
echo "  1. 直接启动 (前台)"
echo "  2. 后台 systemd 服务"
read -p "请选择 [1/2]: " choice

case "$choice" in
    2)
        if [ -f deploy/star-search.service ]; then
            sudo cp deploy/star-search.service /etc/systemd/system/
            sudo systemctl daemon-reload
            sudo systemctl enable star-search
            sudo systemctl start star-search
            echo "✓ systemd 服务已启动"
            echo "  查看状态: sudo systemctl status star-search"
            echo "  查看日志: sudo journalctl -u star-search -f"
        else
            echo "❌ deploy/star-search.service 不存在"
            exit 1
        fi
        ;;
    *)
        echo "启动服务在 http://127.0.0.1:5000 ..."
        python3 scripts/api_server.py --host 127.0.0.1 --port 5000
        ;;
esac

echo ""
echo "=========================================="
echo "  ✓ 安装完成!"
echo "=========================================="
echo ""
echo "测试:"
echo "  curl http://127.0.0.1:5000/v1/health"
echo ""
echo "使用:"
echo "  from star_search_langchain import StarSearchTool"
echo "  tool = StarSearchTool()"
echo "  tool.run('你的查询')"
