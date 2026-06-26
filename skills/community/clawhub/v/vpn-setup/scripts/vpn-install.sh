#!/usr/bin/env bash
#
# VPN Setup Script - WireGuard & OpenVPN Installer
# Author: 小虾 (Xiao Xia)
# License: MIT
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VPN_TYPE="${VPN_TYPE:-wireguard}"
SERVER_IP="${SERVER_IP:-}"
SERVER_PORT_WG="${SERVER_PORT_WG:-51820}"
SERVER_PORT_OV="${SERVER_PORT_OV:-1194}"
DNS_SERVER="${DNS_SERVER:-1.1.1.1}"
CLIENT_NAME="${CLIENT_NAME:-client}"

# Detect OS
get_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/centos-release ]; then
        echo "centos"
    else
        echo "unknown"
    fi
}

# Detect public IP
detect_ip() {
    if [ -n "$SERVER_IP" ]; then
        echo "$SERVER_IP"
        return
    fi
    # Try multiple methods
    IP=$(curl -s -4 ifconfig.me 2>/dev/null || \
         curl -s -4 icanhazip.com 2>/dev/null || \
         curl -s -4 api.ip.sb/ip 2>/dev/null || \
         echo "")
    
    if [ -z "$IP" ]; then
        echo -e "${RED}无法自动检测公网 IP，请手动设置 SERVER_IP 环境变量${NC}"
        exit 1
    fi
    echo "$IP"
}

# Check root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}请使用 sudo 运行此脚本${NC}"
        exit 1
    fi
}

# Install WireGuard
install_wireguard() {
    local OS=$(get_os)
    local SERVER_IP=$(detect_ip)
    
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}   WireGuard VPN 安装${NC}"
    echo -e "${BLUE}   服务器 IP: ${SERVER_IP}${NC}"
    echo -e "${BLUE}   端口：${SERVER_PORT_WG}${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    
    # Install packages
    case $OS in
        ubuntu|debian)
            apt-get update
            apt-get install -y wireguard qrencode
            ;;
        centos|rocky|almalinux)
            yum install -y epel-release
            yum install -y wireguard-tools qrencode
            ;;
        *)
            echo -e "${RED}不支持的系统：$OS${NC}"
            exit 1
            ;;
    esac
    
    # Generate keys
    cd /etc/wireguard
    wg genkey | tee wg0.key | wg pubkey > wg0.pub
    
    # Create server config
    cat > wg0.conf <<EOF
[Interface]
Address = 10.8.0.1/24
ListenPort = ${SERVER_PORT_WG}
PrivateKey = $(cat wg0.key)
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
SaveConfig = true

[Peer]
# 客户端配置将单独生成
EOF
    
    # Enable IP forwarding
    echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/99-wireguard.conf
    sysctl -p /etc/sysctl.d/99-wireguard.conf
    
    # Enable service
    systemctl enable wg-quick@wg0
    systemctl start wg-quick@wg0
    
    # Generate client config
    mkdir -p ~/vpn-client-config
    cd ~/vpn-client-config
    wg genkey | tee ${CLIENT_NAME}.key | wg pubkey > ${CLIENT_NAME}.pub
    
    cat > ${CLIENT_NAME}.conf <<EOF
[Interface]
PrivateKey = $(cat ${CLIENT_NAME}.key)
Address = 10.8.0.2/24
DNS = ${DNS_SERVER}

[Peer]
PublicKey = $(cat /etc/wireguard/wg0.pub)
Endpoint = ${SERVER_IP}:${SERVER_PORT_WG}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF
    
    # Add client to server
    echo "" >> /etc/wireguard/wg0.conf
    echo "[Peer]" >> /etc/wireguard/wg0.conf
    echo "PublicKey = $(cat ${CLIENT_NAME}.pub)" >> /etc/wireguard/wg0.conf
    echo "AllowedIPs = 10.8.0.2/32" >> /etc/wireguard/wg0.conf
    
    systemctl restart wg-quick@wg0
    
    # Generate QR code
    qrencode -t ANSIUTF8 < ${CLIENT_NAME}.conf
    
    echo -e "\n${GREEN}✓ WireGuard 安装完成！${NC}"
    echo -e "${YELLOW}客户端配置文件：~/vpn-client-config/${CLIENT_NAME}.conf${NC}"
    echo -e "${YELLOW}扫描二维码或复制配置到客户端${NC}"
}

# Install OpenVPN
install_openvpn() {
    local OS=$(get_os)
    local SERVER_IP=$(detect_ip)
    
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}   OpenVPN 安装${NC}"
    echo -e "${BLUE}   服务器 IP: ${SERVER_IP}${NC}"
    echo -e "${BLUE}   端口：${SERVER_PORT_OV}${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    
    # Install using official script
    curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
    chmod +x openvpn-install.sh
    
    # Set environment variables for automated install
    export APPROVE_INSTALL=y
    export APPROVE_IP=y
    export IP=${SERVER_IP}
    export ENDPOINT=${SERVER_IP}
    export PORT=${SERVER_PORT_OV}
    export PROTOCOL=udp
    export DNS=${DNS_SERVER}
    export COMPRESSION_ENABLED=n
    export CLIENT=${CLIENT_NAME}
    export PASS=1
    
    # Run installer
    ./openvpn-install.sh
    
    # Move client config
    mkdir -p ~/vpn-client-config
    mv ~/${CLIENT_NAME}.ovpn ~/vpn-client-config/ 2>/dev/null || true
    
    echo -e "\n${GREEN}✓ OpenVPN 安装完成！${NC}"
    echo -e "${YELLOW}客户端配置文件：~/vpn-client-config/${CLIENT_NAME}.ovpn${NC}"
}

# Main
main() {
    check_root
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════╗"
    echo "║        VPN Setup - 小虾 🦞          ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Interactive selection if no argument
    if [ -z "$1" ]; then
        echo "选择 VPN 类型:"
        echo "1) WireGuard (推荐 - 更快更简单)"
        echo "2) OpenVPN (兼容性更好)"
        read -p "请选择 [1-2]: " choice
        case $choice in
            1) VPN_TYPE="wireguard" ;;
            2) VPN_TYPE="openvpn" ;;
            *) echo "无效选择"; exit 1 ;;
        esac
    else
        VPN_TYPE="$1"
    fi
    
    case $VPN_TYPE in
        wireguard|wg|1)
            install_wireguard
            ;;
        openvpn|ov|2)
            install_openvpn
            ;;
        *)
            echo -e "${RED}未知类型：$VPN_TYPE${NC}"
            echo "使用：wireguard 或 openvpn"
            exit 1
            ;;
    esac
}

main "$@"
