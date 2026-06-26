#!/bin/bash
# Mini TimeBot 一键运行（环境配置 + API Key + 注册用户 + 启动服务）

# 锁定绝对路径：确保无论在哪启动，都能找到项目根目录
export PROJECT_ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
export MINI_TIMEBOT_HEADLESS=0
cd "$PROJECT_ROOT"
echo "========== 1/4 环境检查与配置 =========="
bash scripts/setup_env.sh
if [ $? -ne 0 ]; then
    echo "❌ 环境配置失败，请检查错误信息"
    exit 1
fi

# 激活虚拟环境（如果存在），后续所有 python 调用均使用虚拟环境
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

echo ""
echo "========== 2/4 API Key 配置 =========="
# 建议加上判断，防止配置失败后继续运行
bash scripts/setup_apikey.sh
if [ $? -ne 0 ]; then
    echo "⚠️  API Key 配置未完成（可能已跳过或出错）"
fi

echo ""
echo "========== 3/4 用户管理 =========="
read -p "是否需要添加新用户？(y/N): " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    bash scripts/adduser.sh
fi

echo ""
echo "========== 4/4 启动服务 =========="

# 询问是否部署公网
read -p "是否部署到公网？(y/N): " tunnel_answer
if [[ "$tunnel_answer" =~ ^[Yy]$ ]]; then
    echo "🌐 正在后台启动 Cloudflare Tunnel..."
    python scripts/tunnel.py &
    TUNNEL_PID=$!
    # 确保主进程退出时也关闭隧道
    trap "kill $TUNNEL_PID 2>/dev/null" EXIT
    sleep 2
fi

# exec 替换当前进程，确保信号（Ctrl+C、kill、终端关闭）直达 launcher.py
exec python scripts/launcher.py
