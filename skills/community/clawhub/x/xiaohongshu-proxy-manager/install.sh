#!/bin/bash

# 小红书代理管理器安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🌐 小红书代理管理器安装中..."
echo ""

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3"
    exit 1
fi

echo "✅ 找到 python3: $(python3 --version)"

# 创建必要目录
mkdir -p "$SCRIPT_DIR/source"
mkdir -p "$SCRIPT_DIR/config"



# 创建配置文件模板
if [ ! -f "$SCRIPT_DIR/config/proxies.json" ]; then
    cat > "$SCRIPT_DIR/config/proxies.json" << 'EOF'
{
  "proxies": [
    {
      "id": "proxy1",
      "name": "代理1",
      "protocol": "http",
      "host": "127.0.0.1",
      "port": 8080,
      "username": "",
      "password": "",
      "enabled": true
    }
  ],
  "account_mapping": {
    "account1": "proxy1",
    "account2": "proxy1"
  }
}
EOF
    echo "✅ 创建配置文件：config/proxies.json"
fi

# 检查主脚本
if [ ! -f "$SCRIPT_DIR/source/proxy_manager.py" ]; then
    echo "❌ 错误：缺少 source/proxy_manager.py"
    exit 1
fi

echo ""
echo "✅ 小红书代理管理器安装完成！"
echo ""
echo "📖 配置说明："
echo "  1. 编辑 config/proxies.json 添加代理列表"
echo "  2. 配置账号与代理的映射关系"
echo ""
echo "📖 使用方法："
echo "  # 列出所有代理"
echo "  xiaohongshu-proxy-manager --list"
echo ""
echo "  # 为指定账号获取代理"
echo "  xiaohongshu-proxy-manager --account account1"
echo ""
echo "  # 随机获取一个可用代理"
echo "  xiaohongshu-proxy-manager --random"
echo ""
echo "  # 测试代理延迟"
echo "  xiaohongshu-proxy-manager --test proxy1"
echo ""
echo "  # 测试所有代理"
echo "  xiaohongshu-proxy-manager --test-all"
