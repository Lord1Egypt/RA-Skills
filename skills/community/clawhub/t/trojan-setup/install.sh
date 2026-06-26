#!/bin/bash
# Trojan Setup Script
# 自动安装 Trojan 代理客户端和 proxychains4

set -e

echo "========================================"
echo "Trojan Setup Script"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 安装目录
TROJAN_DIR="/usr/src/trojan"
TROJAN_VERSION="1.16.0"

echo "[1/6] 更新系统包列表..."
apt-get update > /dev/null 2>&1
echo -e "${GREEN}✓ 系统更新完成${NC}"

echo ""
echo "[2/6] 安装必要工具..."
apt-get install -y wget tar proxychains4 > /dev/null 2>&1
echo -e "${GREEN}✓ 工具安装完成${NC}"

echo ""
echo "[3/6] 下载 Trojan v${TROJAN_VERSION}..."
if [ -f "/usr/src/trojan-${TROJAN_VERSION}-linux-amd64.tar.xz" ]; then
    echo "Trojan 已下载，跳过下载步骤"
else
    cd /usr/src
    wget -q "https://github.com/trojan-gfw/trojan/releases/download/v${TROJAN_VERSION}/trojan-${TROJAN_VERSION}-linux-amd64.tar.xz"
    echo -e "${GREEN}✓ Trojan 下载完成${NC}"
fi

echo ""
echo "[4/6] 解压并安装 Trojan..."
cd /usr/src
if [ -d "$TROJAN_DIR" ]; then
    echo "备份现有配置..."
    cp "$TROJAN_DIR/config.json" "$TROJAN_DIR/config.json.backup.$(date +%Y%m%d)" 2>/dev/null || true
fi

tar xvf "trojan-${TROJAN_VERSION}-linux-amd64.tar.xz" > /dev/null 2>&1
mv trojan "$TROJAN_DIR"
chmod +x "$TROJAN_DIR/trojan"
echo -e "${GREEN}✓ Trojan 安装完成${NC}"

echo ""
echo "[5/6] 配置 proxychains4..."
# 配置 proxychains4
if ! grep -q "socks5  127.0.0.1 1080" /etc/proxychains4.conf 2>/dev/null; then
    echo "socks5  127.0.0.1 1080" >> /etc/proxychains4.conf
    echo -e "${GREEN}✓ proxychains4 配置完成${NC}"
else
    echo "proxychains4 已配置"
fi

echo ""
echo "[6/6] 修复 Chrome 官方源..."
# 删除旧源
rm -f /etc/apt/sources.list.d/google-chrome.list

# 添加官方 GPG 密钥
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg

# 添加官方源
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# 更新 apt
apt-get update > /dev/null 2>&1
echo -e "${GREEN}✓ Chrome 源修复完成${NC}"

echo ""
echo "========================================"
echo -e "${GREEN}安装完成！${NC}"
echo "========================================"
echo ""
echo -e "${YELLOW}下一步操作：${NC}"
echo ""
echo "1. 编辑 Trojan 配置文件："
echo "   sudo nano /usr/src/trojan/config.json"
echo ""
echo "2. 填写你的服务器信息："
echo "   - remote_addr: 服务器 IP"
echo "   - remote_port: 服务器端口"
echo "   - password: 连接密码"
echo "   - ssl.sni: 服务器域名"
echo ""
echo "3. 启动 Trojan："
echo "   sudo systemctl start trojan"
echo "   sudo systemctl enable trojan"
echo ""
echo "4. 测试代理："
echo "   proxychains4 curl -4 ip.sb"
echo ""
echo -e "${YELLOW}配置文件模板位于：${NC}"
echo "   ~/.openclaw/workspace/skills/trojan-setup/config.json.example"
echo ""
echo -e "${YELLOW}查看日志：${NC}"
echo "   sudo cat /usr/src/trojan/trojan.log"
echo ""
echo "========================================"