---
name: trojan-setup
description: 自动安装和配置 Trojan 代理客户端，支持 proxychains4 全局代理，修复 Chrome 官方源。适用于 Linux 系统的翻墙环境搭建。
metadata:
  openclaw:
    emoji: 🌐
---

# Trojan Setup Skill

自动安装和配置 Trojan 代理客户端，实现 Linux 系统翻墙访问外网。

## 功能

- ⚡ 自动下载安装 Trojan v1.16.0
- 🔧 配置 Trojan client 模式
- 🌐 安装 proxychains4 全局代理
- 🖥️ 修复 Chrome 官方安装源
- 📖 提供详细使用说明

## 前置条件

- Linux 系统（Ubuntu/Debian 等）
- sudo 权限
- Trojan 服务器信息（IP、端口、密码、SNI）

## 安装步骤

### 1. 运行安装脚本

```bash
cd ~/.openclaw/workspace/skills/trojan-setup
chmod +x install.sh
sudo ./install.sh
```

### 2. 配置 Trojan

编辑配置文件：

```bash
sudo nano /usr/src/trojan/config.json
```

填写你的 Trojan 服务器信息：

```json
{
    "run_type": "client",
    "local_addr": "0.0.0.0",
    "local_port": 1080,
    "remote_addr": "YOUR_SERVER_IP",
    "remote_port": YOUR_SERVER_PORT,
    "password": ["YOUR_PASSWORD"],
    "ssl": {
        "sni": "YOUR_SNI",
        "verify": false,
        "verify_hostname": false,
        "cert": ""
    }
}
```

**参数说明：**
- `remote_addr`: Trojan 服务器 IP 地址
- `remote_port`: Trojan 服务器端口
- `password`: Trojan 连接密码
- `sni`: 服务器域名（SNI）

### 3. 启动 Trojan

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
proxychains4 npm install

# 设置环境变量（当前终端）
export http_proxy=socks5://127.0.0.1:1080
export https_proxy=socks5://127.0.0.1:1080

# 取消代理
unset http_proxy
unset https_proxy
```

### 浏览器代理

1. 安装 SwitchyOmega 插件
2. 配置 SOCKS5 代理：127.0.0.1:1080
3. 选择 proxy 模式即可翻墙

### Chrome 浏览器安装

```bash
# 更新源并安装
sudo apt update
sudo apt install google-chrome-stable

# 启动 Chrome
google-chrome
```

## 管理命令

```bash
# 查看 Trojan 状态
sudo systemctl status trojan

# 启动 Trojan
sudo systemctl start trojan

# 停止 Trojan
sudo systemctl stop trojan

# 重启 Trojan
sudo systemctl restart trojan

# 查看日志
sudo cat /usr/src/trojan/trojan.log
```

## 配置文件示例

查看 `config.json.example` 获取完整配置模板：

```bash
cat ~/.openclaw/workspace/skills/trojan-setup/config.json.example
```

## 常见问题

### Q: Trojan 启动失败？

A: 检查日志：
```bash
sudo cat /usr/src/trojan/trojan.log
```

常见原因：
- 配置文件格式错误
- 服务器信息填写错误
- 端口被占用

### Q: 代理不生效？

A: 检查 Trojan 是否运行：
```bash
sudo systemctl is-active trojan
```

### Q: Chrome 无法安装？

A: 确保已添加官方源和 GPG 密钥，然后：
```bash
sudo apt update
sudo apt install google-chrome-stable
```

## 安全提示

⚠️ 本工具仅用于合法用途，请遵守当地法律法规。

## 卸载

```bash
# 停止服务
sudo systemctl stop trojan
sudo systemctl disable trojan

# 删除文件
sudo rm -rf /usr/src/trojan
sudo rm -f /etc/systemd/system/trojan.service

# 删除 proxychains4
sudo apt remove proxychains4

# 刷新 systemd
sudo systemctl daemon-reload
```

## 相关链接

- [Trojan GitHub](https://github.com/trojan-gfw/trojan)
- [Proxychains-ng](https://github.com/rofl0r/proxychains-ng)
- [Chrome 官方](https://www.google.com/chrome/)