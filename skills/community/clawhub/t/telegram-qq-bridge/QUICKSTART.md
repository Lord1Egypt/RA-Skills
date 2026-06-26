# Telegram → QQ 自动转发 快速参考

## 一句话说明
Telegram 群组消息自动转发到 QQ，事件驱动，Node.js 实现，随 OpenClaw 自动启动。

## 快速测试
```bash
# 1. 确保插件运行
ps aux | grep telegram-qq-bridge

# 2. Telegram 发送
@ollama_openclaw_at_dzt_bot 测试

# 3. 检查 QQ
# 应收到：[Telegram] 测试
```

## 配置信息
| 项目 | 值 |
|------|-----|
| Telegram Bot | @ollama_openclaw_at_dzt_bot |
| QQ 账号 | youyanli (有眼力劲儿) |
| QQ OPENID | `YOUR_OPENID_HERE` (你的 QQ OPENID) |
| 监听群组 | 股票智能体 125 |
| 轮询间隔 | 2 秒 |

## 文件位置
- 插件：`~/.openclaw/plugins/telegram-qq-bridge/`
- 技能：`~/.openclaw/skills/telegram-qq-bridge/`
- 日志：`~/.openclaw/plugins/telegram-qq-bridge/telegram-qq-bridge.log`

## 常用命令
```bash
# 启动插件
cd ~/.openclaw/plugins/telegram-qq-bridge/ && node index.js

# 查看日志
tail -f ~/.openclaw/plugins/telegram-qq-bridge/telegram-qq-bridge.log

# 重启插件
pkill -f telegram-qq-bridge && cd ~/.openclaw/plugins/telegram-qq-bridge/ && node index.js

# 手动发送测试
openclaw message send --channel qqbot --account youyanli --target "qqbot:c2c:YOUR_OPENID_HERE" --message "测试"
```

## 故障排查
- **未转发**: 检查消息是否 @bot
- **QQ 未收到**: 检查账号是否为 youyanli
- **插件未运行**: `ps aux | grep telegram-qq-bridge`

## 相关文档
- 完整文档：`README.md`
- 技能定义：`SKILL.md`
- 项目总结：`~/workspace-coding/telegramqq_bridge/项目完成总结.md`
