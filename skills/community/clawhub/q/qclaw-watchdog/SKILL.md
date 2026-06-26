---
name: qclaw-watchdog
description: |
  QClaw Watchdog - Monitors and auto-restarts QClaw when issues are detected.
  Works independently of QClaw, communicates via Feishu for alerts and commands.
  
  QClaw 看门狗 - 监控并自动重启 QClaw，独立于 QClaw 运行，通过飞书发送告警和接收指令。
metadata:
  {"openclaw": {"emoji": "🐕"}}
---

# QClaw Watchdog / QClaw 看门狗

## 功能 Features

- **自动监控** - 可配置间隔检查 QClaw 状态
- **自动修复** - 检测到异常时自动重启
- **飞书通知** - 通过飞书发送状态通知
- **远程控制** - 支持通过飞书发送指令
- **配置分离** - 配置文件与代码分离
- **自动更新** - 支持一键更新到最新版本

## 支持的指令 Commands

| 指令 Command | 说明 Description |
|--------------|-----------------|
| `状态` / `status` | 检查 QClaw 状态 |
| `重启` / `restart` | 重启 QClaw |
| `启动` / `start` | 启动 QClaw |
| `退出` / `quit` | 退出 QClaw |
| `配置` / `config` | 显示当前配置 |
| `帮助` / `help` | 显示帮助 |

## 配置 Configuration

### 配置文件 (config.json)

```json
{
  "feishu": {
    "app_id": "your-app-id",
    "app_secret": "your-secret",
    "user_id": "your-open-id"
  },
  "qclaw": {
    "health_url": "http://127.0.0.1:28789/health"
  },
  "watchdog": {
    "check_interval_ms": 180000,
    "restart_delay_ms": 10000,
    "max_retries": 3
  },
  "logs": {
    "main_log": "./watchdog.log",
    "command_log": "./commands.log"
  }
}
```

### 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `check_interval_ms` | 180000 | 巡检间隔（毫秒），默认3分钟 |
| `restart_delay_ms` | 10000 | 重启延迟（毫秒），默认10秒 |
| `max_retries` | 3 | 最大重试次数 |

### 环境变量

也可以通过环境变量覆盖配置：

```bash
export FEISHU_APP_ID="your-app-id"
export FEISHU_APP_SECRET="your-secret"
export FEISHU_USER_ID="your-open-id"
export CHECK_INTERVAL_MS=300000
```

## 安装 Installation

### 1. 创建配置文件

```bash
./init-config.sh
```

编辑 `config.json`，填入你的飞书应用配置。

### 2. 启动看门狗

```bash
# 前台运行
./start.sh

# 后台运行
nohup ./start.sh >> watchdog.log 2>&1 &
```

### 3. 开机自启 (macOS)

```bash
# 编辑 plist，修改路径
vim com.user.qclaw-watchdog.plist

# 复制到 LaunchAgents
cp com.user.qclaw-watchdog.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.qclaw-watchdog.plist
```

## 更新 Update

### 自动更新

```bash
# 检查更新
./update.sh --check

# 从 GitHub 更新
./update.sh --github username/qclaw-watchdog

# 一键更新
./update.sh

# 强制更新
./update.sh --force
```

### 手动更新

```bash
# 备份配置
cp config.json config.json.bak

# 拉取最新代码
git pull

# 恢复配置
cp config.json.bak config.json

# 重启服务
```

## 发布 Publish

### 发布到 GitHub

```bash
# 安装 GitHub CLI (如果未安装)
brew install gh

# 登录 GitHub
gh auth login

# 发布
./publish.sh --github yourname/qclaw-watchdog
```

发布后，其他用户可以通过以下方式安装：
```bash
# 克隆仓库
git clone https://github.com/yourname/qclaw-watchdog.git

# 配置
./init-config.sh

# 启动
./start.sh
```

## 文件结构

```
qclaw-watchdog/
├── SKILL.md           # 说明文档
├── watchdog.js        # 主程序
├── config.json        # 配置文件（可选）
├── start.sh          # 启动脚本
├── update.sh         # 更新脚本
└── init-config.sh    # 配置初始化脚本
```

## 工作原理

```
┌─────────────┐     WebSocket      ┌─────────────┐
│  飞书服务器  │ ←──────────────→  │   看门狗    │
└─────────────┘                   └──────┬───────┘
                                         │
                          HTTP           ↓
                          GET         ┌─────────────┐
                                  │  QClaw      │
                                  │  Gateway    │
                                  └─────────────┘
```

1. **WebSocket 连接** - 看门狗通过 WebSocket 接收飞书消息
2. **状态检查** - 定期检查 QClaw Gateway 健康状态
3. **自动修复** - 异常时自动重启 QClaw
4. **消息通知** - 通过飞书发送状态通知

## 飞书应用配置

### 1. 创建飞书企业自建应用

1. 打开 [飞书开发者后台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 添加权限：
   - `im:message:send_as_bot` - 发送消息
   - `im:message:receive` - 接收消息
4. 启用事件订阅（长连接模式）
5. 发布应用

### 2. 获取配置信息

| 配置项 | 获取方式 |
|--------|----------|
| App ID | 应用详情 → 凭证与基础信息 |
| App Secret | 应用详情 → 凭证与基础信息 |
| User Open ID | 见下文 |

### 3. 获取用户 Open ID

打开飞书 API 调试页面：

```
https://open.feishu.cn/api-explorer/cli_a9333bca0c78dceb?apiName=create&project=im&resource=message&version=v1
```

1. 在页面中找到「发送消息 API」
2. 查询参数 `receive_id_type` 选择 `open_id`
3. 在请求体中输入用户的 open_id（可以用用户的飞书 ID 或手机号查询）
4. 点击发送，即可看到返回的 open_id

## 注意事项

- 确保 Node.js >= 18 已安装
- 飞书应用需要已发布才能接收消息
- 看门狗独立运行，QClaw 挂了也能监控和告警
- 配置文件变更后需要重启生效
