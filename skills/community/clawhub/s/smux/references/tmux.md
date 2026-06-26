***

name: tmux
description: Raw tmux commands for session, pane, and window control.
metadata:
{ "openclaw": { "emoji": "🧵", "os": \["darwin", "linux"], "requires": { "bins": \["tmux"] } } }
------------------------------------------------------------------------------------------------

# tmux

跨 pane 通信优先使用已安装的 `tmux-bridge` 命令。如果命令不存在，使用绝对路径调用 bridge 脚本，严禁使用相对路径。原生 `tmux` 只保留 3 类 fallback：目标确认、布局管理、排障。

## 目标确认

```bash
tmux list-panes -F '#S:#I.#P #{pane_id} #{pane_current_command} #{pane_title}'
tmux display-message -p '#S:#I.#P #{pane_id}'
```

## 布局管理

```bash
tmux split-window -h -t SESSION
tmux split-window -v -t SESSION
tmux select-layout -t SESSION tiled
```

## 排障

```bash
tmux capture-pane -t SESSION:WINDOW.PANE -p
```

## 使用原则

- 发 agent 消息时不要手搓 `send-keys`
- 确认目标时先看当前 session，再发消息
- 创建新 pane 时优先 `split-window`，然后 `select-layout tiled`

