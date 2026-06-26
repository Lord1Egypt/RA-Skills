# SSH Remote Control Skill for OpenClaw

[中文](#中文) | [English](#english)

---

## 中文

### 概述

这是面向 **OpenClaw** 的 **SSH 远程控制 Skill** — 让 AI Agent 通过 SSH 远程连接和控制电脑，**无需在被控电脑上安装任何 agent 软件**。

传统 AI Agent 需要在本地安装软件才能控制电脑。本技能反其道而行——让 AI Agent 在服务器上运行，通过 SSH 远程控制任何有 SSH 接口的设备。

**能做的事**：
| 操作类型 | 示例 |
|---------|------|
| 文件操作 | 查看桌面、新建文件、上传下载 |
| 软件控制 | 打开/关闭应用、获取运行状态 |
| 系统监控 | 查看配置、磁盘空间、运行进程 |
| AppleScript | 截屏、获取浏览器标签、控制音乐播放 |
| 开发操作 | 查看Git状态、Docker操作、命令行操作 |

### 核心优势

- **远程控制**：AI Agent 在云端，触手伸向多台设备
- **零安装**：被控电脑只需开启 SSH，无需安装任何 agent
- **跨平台**：支持 macOS、Linux
- **CLI 优先**：对 AI 友好的操作方式，Token 消耗低
- **安全可控**：本地可随时关闭穿透工具

### 技术架构

```
┌─────────────┐     SSH      ┌─────────────────┐
│   AI Agent │ ──────────> │  远程电脑        │
│   (服务器)  │   加密隧道   │   (Mac/Linux)    │
│             │ <──────────  │                 │
│   执行命令   │   返回结果   │   无需安装agent │
└─────────────┘             └─────────────────┘
```

### 环境要求

- 远程设备开启 SSH 服务
- 内网穿透工具（如果设备在内网）
- SSH 密钥认证

### 快速开始

1. **被控电脑开启 SSH (macOS)**：
   - 系统偏好设置 → 共享 → 勾选"远程登录"

2. **生成 SSH 密钥对**：
```bash
ssh-keygen -t ed25519 -C "ai@server"
```

3. **添加公钥到被控电脑**：
```bash
echo "你的公钥内容" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

4. **配置内网穿透**（如果设备在内网）：

| 工具 | 特点 | 官网 |
|------|------|------|
| 花生壳 | 国内老牌，稳定 | oray.com |
| ngrok | 国际流行，配置简单 | ngrok.com |
| frp | 开源免费，可自建服务器 | github.com/fatedier/frp |

5. **配置环境变量**：
```bash
export SSH_TARGET_HOST="你的穿透地址"
export SSH_TARGET_PORT="穿透端口"
export SSH_TARGET_USER="用户名"
export SSH_KEY_PATH="/path/to/private/key"
```

6. **测试连接**：
```bash
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'echo "OK"'
```

### 功能示例

**文件操作**：
```bash
# 查看桌面文件
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'ls -la ~/Desktop/'

# 查看文件内容
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'cat ~/Desktop/notes.txt'

# 上传文件
scp -i $SSH_KEY_PATH -P $SSH_TARGET_PORT localfile $SSH_TARGET_USER@$SSH_TARGET_HOST:~/Desktop/
```

**软件控制 (macOS)**：
```bash
# 打开应用
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'open -a Safari'

# 截屏
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'screencapture ~/Desktop/screenshot.png'
```

**系统监控**：
```bash
# 系统版本
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'sw_vers'

# 磁盘空间
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'df -h'
```

### 安全说明

安全性完全由你掌控：

- **本地可控**：穿透工具在你本地运行，可随时关闭
- **按需连接**：需要时开启，不需要时关闭
- **密钥认证**：即使端口暴露，没有正确密钥无法登录
- **关闭即安全**：关闭穿透后，任何人无法访问

**核心建议**：
- 仅在需要 AI 远程控制时才开启穿透
- 使用完毕立即关闭
- 建议配合 SSH 密钥认证，禁用密码登录
- 定期更换 SSH 密钥

### 常见问题

**Q: 和向日葵/AnyDesk 等远程桌面有什么区别？**

| | 远程桌面 | 本 Skill |
|--|---------|---------|
| 控制方式 | 图形界面 | 命令行 |
| 占用带宽 | 高 | 极低 |
| AI 友好性 | 差 | 好 |
| 需要软件 | 是 | 否 |

**Q: 可以控制多台设备吗？**

A: 可以。每台设备配置独立的环境变量，AI 可以同时管理多台设备。

**Q: 设备关机了怎么办？**

A: 无法远程唤醒需要额外配置。保持电脑睡眠而非关机，或配置网络唤醒（WOL）。

### 版本历史

- v1.0.6 (2026-03-31)：强化安全建议，完善文档
- v1.0.4 (2026-03-31)：重写为整段中英双语格式
- v1.0.0 (2026-03-30)：初始版本

### 项目地址

- **ClawHub**：https://clawhub.com/skill/ssh-remote-control
- **GitHub**：https://github.com/lixiang92229/skill-ssh-remote-control

### 开源协议

MIT License

---

## English

### Overview

This is an **OpenClaw Skill** for enabling AI agents to remotely connect and control computers via SSH — **without installing any agent software on the controlled device**.

Traditional AI agents require installing software locally. This skill takes a different approach — running the AI agent on a server and controlling any device with SSH access remotely.

**What you can do**:
| Operation | Examples |
|-----------|----------|
| File Operations | Browse desktop, create files, upload/download |
| Software Control | Open/close apps, check running status |
| System Monitoring | View config, disk space, running processes |
| AppleScript | Screenshot, browser tabs, music control |
| Development | Git status, Docker, CLI commands |

### Core Advantages

- **Remote Control**: AI agent runs on server,触手伸向多台设备
- **Zero Install**: Controlled device only needs SSH enabled, no agent software needed
- **Cross-Platform**: Supports macOS, Linux
- **CLI First**: AI-friendly commands, low Token consumption
- **Secure & Controllable**: Local tunnel can be disabled anytime

### Architecture

```
┌─────────────┐     SSH      ┌─────────────────┐
│   AI Agent │ ──────────> │  Remote Computer  │
│  (Server) │   Encrypted  │  (Mac/Linux)      │
│             │ <──────────  │                   │
│  Execute    │   Return    │  No agent needed │
└─────────────┘             └─────────────────┘
```

### Requirements

- SSH server enabled on remote device
- Tunnel tool (花生壳/ngrok/frp/etc.) if device is behind NAT
- SSH key-based authentication

### Quick Start

1. **Enable SSH on remote device (macOS)**:
   - System Preferences → Sharing → Enable "Remote Login"

2. **Generate SSH key pair**:
```bash
ssh-keygen -t ed25519 -C "ai@server"
```

3. **Add public key to remote device**:
```bash
echo "your-public-key" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

4. **Configure tunnel** (if behind NAT):

| Tool | Features | Website |
|------|----------|---------|
| 花生壳 | Stable, SSH support | oray.com |
| ngrok | Popular, easy setup | ngrok.com |
| frp | Open source, self-hosted | github.com/fatedier/frp |

5. **Configure environment variables**:
```bash
export SSH_TARGET_HOST="your-tunnel-address.example.com"
export SSH_TARGET_PORT="12345"
export SSH_TARGET_USER="your-username"
export SSH_KEY_PATH="/path/to/private/key"
```

6. **Test connection**:
```bash
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'echo "OK"'
```

### Feature Examples

**File Operations**:
```bash
# List directory
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'ls -la ~/Desktop/'

# View file content
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'cat ~/Desktop/notes.txt'

# Upload file
scp -i $SSH_KEY_PATH -P $SSH_TARGET_PORT localfile $SSH_TARGET_USER@$SSH_TARGET_HOST:~/Desktop/
```

**Software Control (macOS)**:
```bash
# Open application
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'open -a Safari'

# Screenshot
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'screencapture ~/Desktop/screenshot.png'
```

**System Monitoring**:
```bash
# System version
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'sw_vers'

# Disk space
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'df -h'
```

### Security Notes

Security is fully under your control:

- **Local Control**: Tunnel runs locally, can be turned off anytime
- **On-demand**: Enable when needed, disable when not
- **Key Auth**: Without correct key, cannot login even if port is exposed
- **Disabled = Secure**: After disabling tunnel, no one can access

**Key recommendations**:
- Enable tunnel only when AI remote control is needed
- Disable immediately after use
- Use SSH key auth, disable password login
- Regularly rotate SSH keys

### FAQ

**Q: How is this different from remote desktop apps like AnyDesk?**

| | Remote Desktop | This Skill |
|--|---------|---------|
| Control | GUI | CLI |
| Bandwidth | High | Minimal |
| AI-Friendly | Poor | Excellent |
| Install Software | Yes | No |

**Q: Can I control multiple devices?**

A: Yes. Each device has its own environment variables. AI can manage multiple devices.

**Q: Does it work when the device is powered off?**

A: No. Keep the device in sleep mode, or configure Wake-on-LAN (WOL).

### Version History

- v1.0.6 (2026-03-31): Strengthen security recommendations
- v1.0.4 (2026-03-31): Rewrite README in bilingual format
- v1.0.0 (2026-03-30): Initial release

### Project Links

- **ClawHub**: https://clawhub.com/skill/ssh-remote-control
- **GitHub**: https://github.com/lixiang92229/skill-ssh-remote-control

### License

MIT License

---

[中文](#中文) | [English](#english)
