# Trojan Setup

🌐 一键搭建 Linux 系统 Trojan 代理环境

## 功能特性

- ⚡ 自动下载安装 Trojan v1.16.0
- 🔧 自动配置 Trojan client 模式
- 🌐 安装 proxychains4 实现全局代理
- 🖥️ 修复 Chrome 官方安装源
- 📖 提供详细使用文档

## 系统要求

- Linux 系统（Ubuntu/Debian 等）
- sudo 权限
- Trojan 服务器订阅（IP、端口、密码、SNI）

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/trojan-setup.git
cd trojan-setup

# 运行安装脚本
chmod +x install.sh
sudo ./install.sh
```

### 2. 配置 Trojan

编辑配置文件，填入你的服务器信息：

```bash
sudo nano /usr/src/trojan/config.json
```

配置示例：
```json
{
    "run_type": "client",
    "local_addr": "0.0.0.0",
    "local_port": 1080,
    "remote_addr": "YOUR_SERVER_IP",
    "remote_port": YOUR_PORT,
    "password": ["YOUR_PASSWORD"],
    "ssl": {
        "sni": "YOUR_SNI",
        "verify": false,
        "verify_hostname": false,
        "cert": ""
    }
}
```

### 3. 启动服务

```bash
sudo systemctl start trojan
sudo systemctl enable trojan  # 开机自启
```

### 4. 验证代理

```bash
# 测试本地 IP
curl -4 ip.sb

# 测试代理 IP
proxychains4 curl -4 ip.sb
```

## 使用方法

### 命令行代理

```bash
# 单次命令走代理
proxychains4 curl https://www.google.com
proxychains4 wget https://example.com/file.zip
proxychains4 git clone https://github.com/user/repo.git

# 设置环境变量（当前终端会话）
export http_proxy=socks5://127.0.0.1:1080
export https_proxy=socks5://127.0.0.1:1080
```

### 浏览器代理

1. 安装 SwitchyOmega 插件
2. 配置 SOCKS5 代理：127.0.0.1:1080
3. 选择 proxy 模式即可翻墙

## 管理命令

```bash
# 查看状态
sudo systemctl status trojan

# 启动/停止/重启
sudo systemctl start trojan
sudo systemctl stop trojan
sudo systemctl restart trojan

# 查看日志
sudo cat /usr/src/trojan/trojan.log
```

## 安装到 OpenClaw

```bash
clawhub install trojan-setup
```

## 文件结构

```
trojan-setup/
├── SKILL.md              # OpenClaw Skill 文档
├── install.sh            # 安装脚本
└── config.json.example   # 配置模板
```

## 安全提示

⚠️ 本工具仅用于合法用途，请遵守当地法律法规。

## 卸载

```bash
sudo systemctl stop trojan
sudo systemctl disable trojan
sudo rm -rf /usr/src/trojan
sudo rm -f /etc/systemd/system/trojan.service
sudo apt remove proxychains4
sudo systemctl daemon-reload
```

## 相关链接

- [Trojan GitHub](https://github.com/trojan-gfw/trojan)
- [Proxychains-ng](https://github.com/rofl0r/proxychains-ng)
- [OpenClaw](https://openclaw.ai)

## 许可证

MIT License

## 作者

- 咕咚 (Gudong) - OpenClaw Assistant

## 致谢

感谢西部世界 VPN 提供的配置教程参考