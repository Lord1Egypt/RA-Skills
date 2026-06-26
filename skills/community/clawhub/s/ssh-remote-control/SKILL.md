---
name: ssh-remote-control
description: SSH远程控制电脑 - 让AI Agent通过SSH连接和操作远程Mac/Linux电脑，无需在被控电脑上安装任何agent工具。一个服务器上的AI，触手伸向多台远程设备。
metadata: {"openclaw": {"homepage": "https://github.com/lixiang92229/skill-ssh-remote-control"}}
---

# SSH Remote Control - 远程控制技能

## 技能简介

让 AI Agent 从服务器通过 SSH 远程连接和控制 Mac/Linux 电脑，无需在被控电脑上安装任何 agent 工具。

**核心原理：**
- AI Agent 部署在服务器
- 通过 SSH 密钥认证连接远程设备
- 用 CLI 命令操作远程电脑（文件、软件、系统等）

**对比传统方案：**

| 方案 | Agent位置 | 被控电脑需要安装 | 架构 |
|------|----------|----------------|------|
| 传统方案 | 本地电脑 | 需要 | 本地控制本地 |
| **本技能** | 服务器 | 不需要 | 远程控制远程 |

## 工作原理

### 架构图

```
┌─────────────┐     SSH      ┌─────────────────┐
│   AI Agent │ ──────────> │  Remote Computer  │
│  (服务器)   │   加密隧道   │  (Mac/Linux)      │
│             │ <──────────  │                   │
│  执行命令    │   返回结果   │  无需安装agent   │
└─────────────┘             └─────────────────┘
```

### 连接流程

1. **远程电脑配置 SSH + 内网穿透**
2. **AI 服务器生成 SSH 密钥对**
3. **公钥添加到远程电脑**
4. **AI 通过 SSH 命令控制远程电脑**

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|-------|------|
| `SSH_TARGET_HOST` | 是 | 远程电脑的公网地址或域名 |
| `SSH_TARGET_PORT` | 是 | SSH 端口（默认22） |
| `SSH_TARGET_USER` | 是 | 远程电脑用户名 |
| `SSH_KEY_PATH` | 是 | 本地私钥路径 |
| `DEFAULT_SHELL` | 否 | 远程电脑默认shell（默认/bin/zsh） |

## 使用示例

### 基础连接测试

```bash
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'echo "SSH OK"'
```

### 文件操作

```bash
# 查看目录
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'ls -la ~/Desktop/'

# 查看文件内容
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'cat ~/Desktop/test.txt'

# 创建文件
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'cat > ~/Desktop/ai_created.txt << '"'"'EOF'"'"'
这是AI创建的文件
EOF'

# 上传文件到远程电脑
scp -i $SSH_KEY_PATH -P $SSH_TARGET_PORT localfile $SSH_TARGET_USER@$SSH_TARGET_HOST:/path/to/remote/

# 从远程电脑下载文件
scp -i $SSH_KEY_PATH -P $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST:/path/to/remote/file localpath/
```

### 软件控制（macOS）

```bash
# 打开应用
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'open -a "Safari"'

# 关闭应用
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'osascript -e '"'"'quit application "Safari"'"'"''

# 查看运行中的程序
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'osascript -e '"'"'tell application "System Events" to get name of every process'"'"''
```

### AppleScript 交互（macOS）

```bash
# 获取应用名称
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'osascript -e '"'"'tell application "NetEase Cloud Music" to name'"'"''

# 获取Chrome当前标签
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'osascript -e '"'"'tell application "Google Chrome" to get URL of every tab of every window'"'"''

# 截屏
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'screencapture ~/Desktop/screenshot.png'
```

### 系统监控

```bash
# 查看系统版本
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'sw_vers'

# 查看资源使用
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'top -l 1 | head -10'

# 查看磁盘空间
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'df -h'

# 查看运行进程
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'ps aux | head -20'
```

### 开发环境操作

```bash
# 查看Node.js版本
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'node --version'

# 查看Git状态
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'cd ~/project && git status'

# Docker操作
ssh -i $SSH_KEY_PATH -p $SSH_TARGET_PORT $SSH_TARGET_USER@$SSH_TARGET_HOST 'docker ps'
```

## 远程电脑配置要求

### macOS 配置步骤

1. **开启远程登录**
   - 系统偏好设置 → 共享 → 勾选"远程登录"
   - 设置允许访问的用户

2. **生成SSH密钥对**
   ```bash
   ssh-keygen -t ed25519 -C "ai@server"
   ```

3. **添加公钥到远程电脑**
   ```bash
   echo "公钥内容" >> ~/.ssh/authorized_keys
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

4. **配置内网穿透**（如果电脑在内网）

   **为什么需要内网穿透？**
   大多数家庭/办公网络的电脑没有公网IP，无法直接从外网访问。内网穿透工具可以将内网端口映射到公网，让外部设备能够连接进来。

   **常用内网穿透工具：**

   | 工具 | 特点 | 官网 |
   |------|------|------|
   | 花生壳 | 国内老牌，稳定，支持SSH | oray.com |
   | ngrok | 国际流行，配置简单 | ngrok.com |
   | frp | 开源免费，可自建服务器 | github.com/fatedier/frp |
   | NATAPP | 国内服务，免费额度 | natapp.cn |

   **安全优势——本地完全控制：**

   与其他远程控制方案不同，本技能的安全性完全由你掌控：

   - **本地启动/停止**：穿透工具在你本地电脑运行，你可以随时关闭它
   - **按需连接**：需要时启动SSH穿透，不需要时关闭
   - **无需云端中转**：SSH加密隧道直连，数据不经过第三方服务器
   - **密钥认证**：即使穿透端口暴露，没有正确密钥也无法登录
   - **关闭即安全**：关闭穿透工具后，任何外部设备都无法访问你的电脑

   > 💡 **为什么"关闭穿透"是真正的安全？**
   >
   > 服务器的安全靠"规则"——端口持续开放，靠防火墙规则防护。
   > 个人电脑 + 穿透工具的安全靠"开关"——穿透工具不运行，外部根本找不到你。
   > 这不是"防护"，这是**物理隔离**。关闭穿透 = 攻击面归零。

   **使用建议：**
   - 仅在需要AI远程控制时才开启穿透
   - 使用完毕立即关闭穿透工具
   - 建议配合SSH密钥认证使用，禁用密码登录
   - 定期更换SSH密钥

### Linux 配置步骤

1. **安装openssh-server**
   ```bash
   sudo apt install openssh-server
   ```

2. **配置SSH**
   ```bash
   sudo nano /etc/ssh/sshd_config
   # 确保有：
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```

   > ⚠️ **安全建议**：禁用密码认证，只允许密钥认证

3. **重启SSH服务**
   ```bash
   sudo systemctl restart sshd
   ```

4. **配置内网穿透**（同上）

## 安全建议

### 1. 密钥安全
- 私钥文件权限必须是600
- 不要将私钥分享给他人
- 定期更换密钥
- ⚠️ **重要**：SSH私钥路径被AI获取后，AI理论上可访问任何使用该密钥的服务器。务必使用**专用密钥对**，不要使用日常登录密钥。

### 2. 防火墙
- SSH端口不要暴露给0.0.0.0
- 使用VPN或内网穿透
- 定期查看登录日志

### 3. 命令限制
- 可以在远程电脑的`~/.ssh/authorized_keys`中限制可执行的命令
- 示例：
  ```
  command="/usr/local/bin/limited.sh",no-pty,permitopen="*",ssh-ed25519 AAAA...
  ```

### 4. 最小权限原则

**使用专用受限账户**（而非 root/管理员）：
- 在远程电脑上创建专用账户，如 `aiagent`
- 只授权必要的操作权限
- 避免 AI 使用管理员权限

**密钥权限限制**：
- 使用 `from=` 限制连接来源 IP
- 使用 `command=` 限制可执行命令
- 使用 `no-pty` 禁止分配伪终端
- 使用 `permitopen=` 限制端口转发

示例（`~/.ssh/authorized_keys`）：
```
from="你的服务器IP",no-pty,command="/bin/false",ssh-ed25519 AAAA...
```

### 5. 密钥保护建议

- **passphrase 保护**：为私钥设置密码，防止密钥泄露被直接使用
- **专用密钥**：为本技能创建单独的 SSH 密钥对，可随时 revocation
- **定期轮换**：定期更换 SSH 密钥对

### 6. 监控与审计

- 定期查看 SSH 登录日志
- 监控异常的登录时间和来源
- 记录 AI 执行的关键命令（本地日志）

## 故障排除

### 连接被拒绝
1. 确认远程电脑SSH服务正在运行
2. 确认防火墙允许SSH端口
3. 确认花生壳等穿透服务正常运行

### 公钥认证失败
1. 确认公钥已添加到`~/.ssh/authorized_keys`
2. 确认文件权限正确：
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

### 超时或断开
1. 使用`ServerAliveInterval`保持连接
2. 检查网络稳定性
3. 确认内网穿透服务未过期

## 应用场景

1. **远程办公**: 在手机上通过AI操作办公室电脑
2. **智能家居**: 连接智能设备执行自动化任务
3. **跨设备协作**: 一个AI agent管理多台设备
4. **物联网控制**: 通过SSH控制树莓派等设备
5. **远程服务器管理**: 无需本地安装任何工具

## 技术优势

- **无需在被控电脑安装任何软件**: 只要有SSH即可
- **跨平台**: 支持macOS、Linux、Windows (WSL)
- **云端部署**: Agent在服务器，触手伸向各地
- **安全**: SSH加密隧道，无需暴露桌面
- **高效**: CLI对AI友好，Token消耗低

## 项目地址 | Project Links

- **ClawHub**: https://clawhub.com/skill/ssh-remote-control
- **GitHub**: https://github.com/lixiang92229/skill-ssh-remote-control

## 版本历史 | Changelog

- 1.0.9 (2026-03-31): 修复 homepage URL 与 GitHub 一致，强化私钥安全警告
- 1.0.6 (2026-03-31): 修复 Metadata 不匹配，修复 PasswordAuthentication yes 问题，强化安全建议
- 1.0.5 (2026-03-31): 重写 README 为整段中英双语格式
- 1.0.4 (2026-03-31): README 格式修正
- 1.0.3 (2026-03-31): 修复 GitHub 链接
- 1.0.2 (2026-03-31): 添加项目链接
- 1.0.1 (2026-03-31): 强调安全性，通用内网穿透工具，本地完全可控
- 1.0.0 (2026-03-30): 初始版本，支持macOS/Linux远程控制
