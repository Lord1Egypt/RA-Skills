---
name: solvea-chat
version: 0.5.3
description: Call Solvea Web App chat API to get AI customer service replies. Use for real customer-service questions. On session boot message ("new session was started"), call with --mark-reset (no peer-id needed). For normal messages, call with --peer-id and --message. Never call for other slash-prefixed commands.
---

# Solvea AI 客服对话

将 OpenClaw 渠道消息（飞书、钉钉等）接入 [Solvea](https://solvea.cx) Web App，一键部署 AI 客服 agent。

## 安装

```bash
cd ~/.openclaw
clawhub install solvea-chat
```

复制上一步输出中 `Installed solvea-chat ->` 后面的路径，执行其中的 `setup.sh`：

```bash
bash <上面输出的路径>/setup.sh
```

按提示完成配置后，重启 OpenClaw。

## 前置条件

- [OpenClaw](https://openclaw.ai) 已安装并配置至少一个渠道（飞书 / 钉钉等）
- 拥有 Solvea Web App 的 X-Token 和 Agent ID
- 本地已安装 `python3`

### 手动修改配置

如需事后修改：

- API 配置：编辑 `<skill目录>/.env`
- 渠道绑定：编辑 `~/.openclaw/openclaw.json`，在 `bindings` 中添加：

```json
{
  "agentId": "solvea",
  "match": { "channel": "<渠道名>" }
}
```

---

## 调用方式（供 agent 参考）

**发送客服消息：**
```bash
skills/solvea-chat/.venv/bin/python skills/solvea-chat/scripts/chat.py \
  --peer-id "feishu:<open_id>" \
  --message "<用户消息内容>"
```

**session 启动时记录 reset 标记（boot 消息时调用，无需 peer-id）：**
```bash
skills/solvea-chat/.venv/bin/python skills/solvea-chat/scripts/chat.py --mark-reset
```

**重置指定用户 session：**
```bash
skills/solvea-chat/.venv/bin/python skills/solvea-chat/scripts/chat.py \
  --peer-id "feishu:<open_id>" \
  --reset
```

**参数说明：**
- `--mark-reset`：记录 reset 标记，下次 chat 时自动先清除 session
- `--peer-id`：用户唯一标识，飞书用户使用 `feishu:<open_id>` 格式
- `--message`：本轮用户消息（与 `--reset` 二选一）
- `--reset`：立即清除该用户的 Solvea session

---

## Session 管理

脚本自动管理 `memory/solvea-sessions.json`：

| 场景 | 行为 |
|------|------|
| 新用户首次消息 | 服务端分配新 chat_id，自动保存 |
| 老用户继续对话 | 读取已有 chat_id，保持上下文 |
| session 失效 | 自动清除旧 chat_id，重建新 session 后重试 |
| `/reset` 命令 | 清除 chat_id，下次对话从头开始 |

## 错误处理

| 情况 | 输出 |
|------|------|
| AI 正常回复 | stdout: AI 回复内容 |
| 需要转人工 | stdout: 转人工提示语 |
| AI 无法回答 | stdout: 无法回答提示语 |
| 网络/认证/配置错误 | stderr: 错误详情，exit code=1 |

## 参考

- API 详细说明：`references/api-spec.md`
