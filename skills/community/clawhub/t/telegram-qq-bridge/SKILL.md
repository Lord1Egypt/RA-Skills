# telegram-qq-bridge Skill

## 描述
Telegram → QQ 自动转发技能。监听 Telegram 群组消息，自动转发到 QQ 私聊。

## 触发词
- telegram 转发
- qq 转发
- telegram qq 桥接
- 自动转发 telegram
- telegram to qq

## 位置
`~/.openclaw/skills/telegram-qq-bridge/`

## 功能
1. **自动监听** Telegram 群组消息（需要 @ollama_openclaw_at_dzt_bot）
2. **自动转发** 到 QQ（有眼力劲儿账号）
3. **事件驱动** 无轮询，OpenClaw 原生集成
4. **Node.js 实现** 符合 OpenClaw 技术栈

## 架构
```
Telegram (@ollama_openclaw_at_dzt_bot)
    ↓
OpenClaw Telegram Channel (stockworker agent)
    ↓
telegram-qq-bridge 插件 (自动监听)
    ↓
QQ Bot (有眼力劲儿 youyanli)
    ↓
用户 QQ 收到消息
```

## 配置
- **Telegram Bot**: @ollama_openclaw_at_dzt_bot
- **QQ 账号**: youyanli (有眼力劲儿)
- **QQ Target**: `qqbot:c2c:YOUR_OPENID_HERE` (替换为你的 QQ OPENID)
- **监听群组**: 股票智能体 125 (-1003838124188)

## 使用方法

### 启动转发
```bash
# 插件随 OpenClaw 自动启动
# 或手动启动
cd ~/.openclaw/plugins/telegram-qq-bridge/
node index.js
```

### 测试转发
1. 在 Telegram 群组发送：`@ollama_openclaw_at_dzt_bot 测试`
2. 检查 QQ 是否收到：`[Telegram] 测试`

### 查看状态
```bash
ps aux | grep telegram-qq-bridge
tail -f ~/.openclaw/plugins/telegram-qq-bridge/telegram-qq-bridge.log
```

## 文件清单
| 文件 | 说明 |
|------|------|
| `~/.openclaw/plugins/telegram-qq-bridge/index.js` | 主程序（Node.js） |
| `~/.openclaw/plugins/telegram-qq-bridge/package.json` | 包配置 |
| `~/.openclaw/plugins/telegram-qq-bridge/openclaw.plugin.json` | 插件配置 |
| `~/.openclaw/skills/telegram-qq-bridge/SKILL.md` | 本文件 |
| `~/.openclaw/workspace-coding/telegramqq_bridge/` | 项目文档和测试脚本 |

## 依赖
- Node.js >= 14.0.0
- OpenClaw >= 2026.5.2
- QQ Bot 账号（youyanli）
- Telegram Bot (@ollama_openclaw_at_dzt_bot)

## 注意事项
1. **必须 @bot**: Telegram 消息需要包含 `@ollama_openclaw_at_dzt_bot` 才会被处理
2. **账号正确**: 确保使用 `youyanli` 账号发送，不是默认账号
3. **target 格式**: 必须使用 `qqbot:c2c:OPENID` 格式
4. **自动启动**: 插件随 OpenClaw 自动启动，无需手动干预

## 故障排查

### 消息未转发
1. 检查 Telegram 消息是否包含 `@ollama_openclaw_at_dzt_bot`
2. 检查插件是否运行：`ps aux | grep telegram-qq-bridge`
3. 查看日志：`tail -f ~/.openclaw/plugins/telegram-qq-bridge/telegram-qq-bridge.log`

### QQ 未收到
1. 确认 OPENID 正确：`YOUR_OPENID_HERE`（从 QQ Bot 配置中获取）
2. 确认账号正确：`youyanli`（有眼力劲儿）
3. 手动测试：`openclaw message send --channel qqbot --account youyanli --target "qqbot:c2c:YOUR_OPENID_HERE" --message "测试"`

### 插件未启动
```bash
# 重启插件
cd ~/.openclaw/plugins/telegram-qq-bridge/
node index.js
```

## 版本历史
- **v1.0.0** (2026-05-17): 初始版本
  - Node.js 实现
  - OpenClaw 插件集成
  - 自动监听 Telegram 消息
  - 自动转发到 QQ

## 相关项目
- 项目目录：`~/.openclaw/workspace-coding/telegramqq_bridge/`
- 文档：`~/.openclaw/workspace-coding/telegramqq_bridge/README_最终版.md`
