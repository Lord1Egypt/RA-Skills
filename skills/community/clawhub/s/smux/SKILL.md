---
name: smux
description: Cross-pane messaging for tmux. Use `tmux-bridge` command to send messages between panes labeled p1, p2, p3...
version: 1.0.0
metadata:
  { "openclaw": { "emoji": "🖥️", "os": ["darwin", "linux"], "requires": { "bins": ["tmux"] } } }
---

# smux

多 pane 协作技能。通过 `p1`, `p2`, `p3` 标签与其他 pane 通信，无需记忆 pane ID。

## 快速开始

```bash
# 从普通 shell 启动三 pane 工作台
tmux-bridge -l mysession

# 查看当前 session 的 panes
tmux-bridge list

# 收到任务后，先判断当前消息是不是来自其他 agent
tmux-bridge pending

# 需要对方回传结果时显式声明
tmux-bridge send --expect-reply p1 '请分析 src/auth.ts'

# 仅通知，不要求回复
tmux-bridge send --no-reply p1 '我先去跑测试'

# 收到待回复任务后回传最终结论
tmux-bridge reply '分析完成：...'
```

## 命令

| 命令 | 用途 |
|---|---|
| `launch` / `-l <session_name> [delay_secs]` | 从外层 shell 创建新的三 pane session，并自动 attach |
| `kill-session` / `-k <session_name>` | 按 session 名快速关闭整个 tmux session |
| `list` | 列出当前 session 的所有 pane 和标签 |
| `send --expect-reply <target> <msg>` | 发送需要回传结果的消息 |
| `send --no-reply <target> <msg>` | 发送不需要回传的消息 |
| `pending` | 查看当前 pane 未处理的待回复消息，状态为 `waiting` 或 `overdue` |
| `reply <msg>` | 回复当前 pane 最近一条待回复消息 |
| `rename` | 将当前 session 所有 pane 重命名为 p1, p2, p3... |
| `auto-label` | 输出自动命名配置脚本 |

## Agent 协作准则

1. 在生成最终回复前，先执行 `tmux-bridge pending` 判断当前 pane 是否有待回复消息。
2. 如果 `pending` 显示 `waiting` 或 `overdue`，说明当前任务来自其他 agent，最终结论必须用 `tmux-bridge reply '<结论>'` 回传。
3. 如果 `pending` 没有待回复项，视为普通用户输入，不需要调用 `reply`。
4. 给其他 agent 发任务时，默认使用显式模式：
   - 需要结果时用 `--expect-reply`
   - 只是通知时用 `--no-reply`
5. 禁止回传“收到”“正在处理”“谢谢”这类无效内容；即使没有发现，也要明确回复“无发现”。
6. 如果 `tmux-bridge reply` 报错 `no pending reply target for this pane`，说明当前没有可自动回复的对象，此时再手动使用 `tmux-bridge send --no-reply <target> '<结论>'`。

## 自动命名（推荐）

开启后，新创建的 pane 自动获得 `p1`, `p2` 标签：

```bash
# 添加配置到 tmux.conf
tmux-bridge auto-label >> ~/.tmux.conf
tmux source-file ~/.tmux.conf
```

## 使用原则

- 外层创建/关闭 session 优先使用 `tmux-bridge -l` 和 `tmux-bridge -k`
- `pending` 是判断消息来源的唯一依据，不要靠目测 pane 输出猜测
- 发 agent 消息时不要手搓 `send-keys`
- 标签优先：用 `p1` 代替 `%42`
- `reply` 只用于处理 `--expect-reply` 建立的待回复消息
