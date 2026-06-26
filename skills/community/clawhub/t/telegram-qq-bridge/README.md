# Telegram → QQ 自动转发技能

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.ai/skills/telegram-qq-bridge)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Node.js](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen)](https://nodejs.org/)

Telegram 群组消息自动转发到 QQ，事件驱动，Node.js 实现，随 OpenClaw 自动启动。

## 特性

- ✅ **自动监听** - 自动监听 Telegram 群组消息
- ✅ **自动转发** - 收到消息后自动转发到 QQ
- ✅ **事件驱动** - 无轮询，OpenClaw 原生集成
- ✅ **Node.js 实现** - 符合 OpenClaw 技术栈
- ✅ **插件化** - 作为 OpenClaw 插件，随系统自动启动
- ✅ **配置简单** - 支持配置文件和环境变量

## 快速开始

### 1. 安装
```bash
# 从 ClawHub 安装（推荐）
openclaw skill install telegram-qq-bridge

# 或手动安装
git clone https://github.com/your-repo/telegram-qq-bridge.git ~/.openclaw/skills/telegram-qq-bridge
```

### 2. 配置
```bash
cd ~/.openclaw/skills/telegram-qq-bridge/
cp config.example.json config.json
vim config.json
```

修改配置项：
```json
{
  "qqTarget": "qqbot:c2c:YOUR_OPENID",
  "qqAccount": "your_qq_account",
  "pollInterval": 2000
}
```

### 3. 启动
```bash
# 随 OpenClaw 自动启动
openclaw restart

# 或手动启动
cd ~/.openclaw/plugins/telegram-qq-bridge/
node index.js
```

### 4. 测试
```bash
# 在 Telegram 群组发送
@ollama_openclaw_at_dzt_bot 测试

# 检查 QQ 是否收到
# 应该收到：[Telegram] 测试
```

## 配置说明

### 配置文件
位置：`~/.openclaw/skills/telegram-qq-bridge/config.json`

```json
{
  "enabled": true,
  "qqTarget": "qqbot:c2c:YOUR_OPENID",
  "qqAccount": "your_qq_account",
  "pollInterval": 2000,
  "sessionFile": "~/.openclaw/agents/stockworker/sessions/SESSION.jsonl"
}
```

### 环境变量
```bash
export QQ_TARGET="qqbot:c2c:YOUR_OPENID"
export QQ_ACCOUNT="your_qq_account"
export POLL_INTERVAL="2000"
export TELEGRAM_QQ_SESSION_FILE="~/.openclaw/agents/stockworker/sessions/SESSION.jsonl"
```

### 配置项说明
| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `qqTarget` | QQ 目标地址 (格式：`qqbot:c2c:OPENID`) | - | ✅ |
| `qqAccount` | QQ 账号名 | `youyanli` | ✅ |
| `pollInterval` | 轮询间隔 (毫秒) | `2000` | ❌ |
| `sessionFile` | Telegram session 文件路径 | - | ❌ |

## 架构

```
Telegram (@ollama_openclaw_at_dzt_bot)
    ↓
OpenClaw Telegram Channel
    ↓
telegram-qq-bridge 插件
    ↓
QQ Bot
    ↓
用户 QQ
```

## 工作原理

1. 插件轮询监听 Telegram session 文件
2. 检测到包含 `@ollama_openclaw_at_dzt_bot` 的消息
3. 调用 `openclaw message send` 转发到 QQ
4. 用户 QQ 收到转发消息

## 故障排查

### 消息未转发
1. 检查消息是否包含 `@ollama_openclaw_at_dzt_bot`
2. 检查插件是否运行：`ps aux | grep telegram-qq-bridge`
3. 查看日志：`tail -f ~/.openclaw/plugins/telegram-qq-bridge/telegram-qq-bridge.log`

### QQ 未收到
1. 确认 `qqTarget` 格式正确：`qqbot:c2c:OPENID`
2. 确认 `qqAccount` 正确
3. 手动测试：
   ```bash
   openclaw message send \
     --channel qqbot \
     --account your_account \
     --target "qqbot:c2c:YOUR_OPENID" \
     --message "测试"
   ```

### 插件未启动
```bash
# 重启插件
cd ~/.openclaw/plugins/telegram-qq-bridge/
node index.js

# 或重启 OpenClaw
openclaw restart
```

## 开发

### 目录结构
```
telegram-qq-bridge/
├── index.js                 # 主程序
├── package.json            # 包配置
├── config.example.json     # 配置模板
├── .gitignore             # Git 忽略文件
├── README.md              # 本文件
├── SKILL.md               # 技能定义
└── QUICKSTART.md          # 快速参考
```

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/your-repo/telegram-qq-bridge.git
cd telegram-qq-bridge

# 安装依赖（如果有）
npm install

# 配置
cp config.example.json config.json
vim config.json

# 运行
node index.js
```

### 测试
```bash
# 单元测试（如果有）
npm test

# 集成测试
# 1. 在 Telegram 发送测试消息
# 2. 检查 QQ 是否收到
```

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 相关链接

- [ClawHub](https://clawhub.ai)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [项目仓库](https://github.com/your-repo/telegram-qq-bridge)
- [问题反馈](https://github.com/your-repo/telegram-qq-bridge/issues)

## 更新日志

### v1.0.0 (2026-05-17)
- ✨ 初始版本
- ✅ 实现 Telegram 到 QQ 的自动转发
- ✅ Node.js 实现，OpenClaw 插件集成
- ✅ 支持配置文件和环境变量
- ✅ 事件驱动，无轮询
