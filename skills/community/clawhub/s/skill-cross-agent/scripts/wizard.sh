#!/bin/bash
# cross-agent-wizard - 交互式向导

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║   🔌 Cross-Agent 跨机器协作向导        ║"
echo "║   引导你完成跨机器Agent协作配置        ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# 步骤1: 检查依赖
echo "📋 步骤 1/5: 检查依赖..."
if ! command -v sshpass > /dev/null 2>&1; then
    echo "  ⚠️ 未安装 sshpass，正在安装..."
    sudo apt update && sudo apt install -y sshpass
else
    echo "  ✅ sshpass 已安装"
fi

# 步骤2: 扫描网络
echo ""
echo "📋 步骤 2/5: 扫描局域网设备..."
echo "  请输入网段 (默认: 192.168.3):"
read -r NETWORK
NETWORK="${NETWORK:-192.168.3}"

# 快速扫描
echo "  🔍 扫描 ${NETWORK}.0/24..."
FOUND_IPS=()
for i in $(seq 1 20); do
    IP="${NETWORK}.${i}"
    if ping -c 1 -W 0.3 "$IP" > /dev/null 2>&1; then
        echo "    ✓ 发现: $IP"
        FOUND_IPS+=("$IP")
    fi
done

if [ ${#FOUND_IPS[@]} -eq 0 ]; then
    echo "  ❌ 未发现在线设备"
    exit 1
fi

# 步骤3: 选择目标
echo ""
echo "📋 步骤 3/5: 选择目标机器..."
echo "  请输入目标IP (从上方的列表中选择):"
read -r TARGET_IP

# 步骤4: 输入认证信息
echo ""
echo "📋 步骤 4/5: 输入认证信息..."
echo "  请输入用户名 (默认: admin):"
read -r TARGET_USER
TARGET_USER="${TARGET_USER:-admin}"

echo "  请输入密码:"
read -rs TARGET_PASS
echo ""

# 步骤5: 测试连接
echo ""
echo "📋 步骤 5/5: 测试连接..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if "${SCRIPT_DIR}/test.sh" "$TARGET_IP" "$TARGET_USER" "$TARGET_PASS"; then
    echo ""
    echo -e "${GREEN}✅ 连接成功!${NC}"
    echo ""
    echo "是否保存为默认配置? (y/n)"
    read -r SAVE
    if [ "$SAVE" = "y" ]; then
        "${SCRIPT_DIR}/config.sh" --default-user "$TARGET_USER"
        "${SCRIPT_DIR}/config.sh" --default-pass "$TARGET_PASS"
        "${SCRIPT_DIR}/config.sh" --default-ip "$TARGET_IP"
        echo "✅ 配置已保存"
    fi
    echo ""
    echo "🎉 向导完成! 现在你可以使用:"
    echo "   openclaw cross-agent send '你的任务'"
else
    echo ""
    echo "❌ 连接失败，请检查:"
    echo "   - IP地址是否正确"
    echo "   - 用户名/密码是否正确"
    echo "   - 目标机器SSH是否开启"
fi