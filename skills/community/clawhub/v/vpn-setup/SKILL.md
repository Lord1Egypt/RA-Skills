---
name: vpn-setup
description: 一键搭建 VPN 服务器（WireGuard/OpenVPN），支持多种 Linux 发行版。
author: 小虾 (Xiao Xia)
version: 1.0.1
homepage: https://github.com/openclaw/openclaw
triggers:
  - "搭建 VPN"
  - "安装 VPN"
  - "VPN setup"
  - "wireguard"
  - "openvpn"
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["curl","bash"]},"config":{"env":{"VPN_TYPE":{"description":"VPN 类型","default":"wireguard","options":["wireguard","openvpn"],"required":false},"SERVER_IP":{"description":"服务器公网 IP","required":false}}}}}
---

# VPN Setup 技能

一键搭建 VPN 服务器，支持 WireGuard 和 OpenVPN。

## 快速开始

```bash
# WireGuard（推荐 - 更快更简单）
uv run {baseDir}/scripts/vpn-install.sh wireguard

# OpenVPN（兼容性更好）
uv run {baseDir}/scripts/vpn-install.sh openvpn
```

## 交互式安装

```bash
uv run {baseDir}/scripts/vpn-install.sh
```

## 配置选项

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `VPN_TYPE` | VPN 类型：wireguard 或 openvpn | wireguard |
| `SERVER_IP` | 服务器公网 IP（自动检测） | 自动 |
| `SERVER_PORT` | VPN 监听端口 | 51820 (WG) / 1194 (OV) |
| `DNS_SERVER` | 客户端 DNS 服务器 | 1.1.1.1 |

## 输出文件

安装完成后会生成：

- **WireGuard**: `/etc/wireguard/wg0.conf`
- **OpenVPN**: `/root/client.ovpn`
- **客户端配置**: `~/vpn-client-config/` 目录

## 管理命令

### WireGuard

```bash
# 查看状态
sudo systemctl status wg-quick@wg0

# 添加客户端
wg genkey | tee /etc/wireguard/client.key | wg pubkey > /etc/wireguard/client.pub

# 重启服务
sudo systemctl restart wg-quick@wg0
```

### OpenVPN

```bash
# 查看状态
sudo systemctl status openvpn

# 生成新客户端
cd /etc/openvpn/easy-rsa/
./easyrsa build-client-full newclient nopass
```

## 支持的系统

- Ubuntu 20.04+
- Debian 10+
- CentOS 7+
- Rocky Linux 8+
- AlmaLinux 8+

## 安全提示

- 安装后请修改默认端口
- 定期更新系统和 VPN 软件
- 使用强密码/密钥
- 配置防火墙限制访问

## 故障排查

```bash
# 查看日志
sudo journalctl -u wg-quick@wg0 -f
sudo journalctl -u openvpn -f

# 测试连接
ping 10.8.0.1  # WireGuard 默认网关
ping 10.8.0.1  # OpenVPN 默认网关
```
