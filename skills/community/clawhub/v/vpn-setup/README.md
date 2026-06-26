# VPN Setup 技能 🦞

一键搭建 VPN 服务器（WireGuard/OpenVPN）的 OpenClaw 技能。

## 功能特点

- ✅ 支持 WireGuard 和 OpenVPN
- ✅ 自动检测公网 IP
- ✅ 生成客户端配置文件
- ✅ 生成二维码方便移动端配置
- ✅ 支持主流 Linux 发行版
- ✅ 交互式/自动化两种模式

## 安装

```bash
clawhub install vpn-setup
```

或手动克隆：

```bash
git clone https://github.com/your-username/vpn-setup.git ~/.openclaw/workspace/skills/vpn-setup
```

## 使用

### 快速安装（WireGuard）

```bash
uv run /home/admin/.openclaw/workspace/skills/vpn-setup/scripts/vpn-install.sh wireguard
```

### 交互式安装

```bash
uv run /home/admin/.openclaw/workspace/skills/vpn-setup/scripts/vpn-install.sh
```

### 使用环境变量

```bash
export VPN_TYPE=wireguard
export SERVER_IP=1.2.3.4
export SERVER_PORT_WG=51820
export DNS_SERVER=8.8.8.8
uv run /home/admin/.openclaw/workspace/skills/vpn-setup/scripts/vpn-install.sh
```

## 配置选项

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VPN_TYPE` | wireguard 或 openvpn | wireguard |
| `SERVER_IP` | 服务器公网 IP | 自动检测 |
| `SERVER_PORT_WG` | WireGuard 端口 | 51820 |
| `SERVER_PORT_OV` | OpenVPN 端口 | 1194 |
| `DNS_SERVER` | 客户端 DNS | 1.1.1.1 |
| `CLIENT_NAME` | 客户端名称 | client |

## 支持的系统

- Ubuntu 20.04+
- Debian 10+
- CentOS 7+
- Rocky Linux 8+
- AlmaLinux 8+

## 客户端配置

安装完成后，客户端配置文件位于：

```
~/vpn-client-config/
├── client.conf      # WireGuard
└── client.ovpn      # OpenVPN
```

### iOS/Android 配置

**WireGuard:**
1. 安装 WireGuard App
2. 扫描二维码或导入配置文件

**OpenVPN:**
1. 安装 OpenVPN Connect App
2. 导入 .ovpn 文件

## 管理命令

### WireGuard

```bash
# 查看状态
sudo systemctl status wg-quick@wg0

# 查看连接
sudo wg show

# 重启服务
sudo systemctl restart wg-quick@wg0

# 查看日志
sudo journalctl -u wg-quick@wg0 -f
```

### OpenVPN

```bash
# 查看状态
sudo systemctl status openvpn

# 重启服务
sudo systemctl restart openvpn

# 查看日志
sudo journalctl -u openvpn -f
```

## 安全建议

1. 🔒 修改默认端口
2. 🔒 使用防火墙限制访问
3. 🔒 定期更新系统
4. 🔒 为每个设备创建独立客户端配置
5. 🔒 考虑启用双因素认证

## 故障排查

### 无法连接

```bash
# 检查服务状态
sudo systemctl status wg-quick@wg0

# 检查防火墙
sudo iptables -L -n -v

# 检查 IP 转发
cat /proc/sys/net/ipv4/ip_forward
```

### 速度慢

- 尝试更换端口
- 检查服务器带宽
- 考虑更换协议（UDP vs TCP）

## 许可证

MIT License

## 作者

小虾 (Xiao Xia) 🦞

## 贡献

欢迎提交 Issue 和 Pull Request！
