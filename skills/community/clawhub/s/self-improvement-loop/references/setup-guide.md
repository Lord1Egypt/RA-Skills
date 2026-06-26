# 安装后参考

## Per-Agent 架构

```
openclaw.json agents.list
    ↓
install.sh 为每个 agent 创建独立 cron + 独立 .learnings/
    ↓
Hook (handler.js) 根据 sessionKey 动态路由
    ↓
Cron job 使用 LEARNINGS_DIR 环境变量指向 agent 自己的 learnings 目录
```

## 验证 distill（单 agent / 全局）

```bash
bash ~/.openclaw/workspace/skills/self-improvement-loop/scripts/distill.sh --check-only
```

正常输出 JSON，包含 `patterns` / `category_fallback` / `meta`。

## 验证 distill（指定 agent）

```bash
# 指定 agent 工作区
LEARNINGS_DIR="$HOME/.openclaw/workspace/code-dev/.learnings" \
  bash ~/.openclaw/workspace/skills/self-improvement-loop/scripts/distill.sh --check-only

# 查看特定 agent 的 learnings
cat ~/.openclaw/workspace/code-dev/.learnings/LEARNINGS.md
```

## 查看 Cron 状态

```bash
openclaw cron list
```

多 agent 时应看到多个 cron（每 agent 一个）：

- `self-improvement-main`（每 1 小时）
- `self-improvement-code-dev`
- `self-improvement-墨灵`
- ...

每个 cron 的 `LEARNINGS_DIR` 已注入到消息中，指向对应 agent 的 workspace。

## 查看所有 agent 的 learnings 目录

```bash
# 从 openclaw.json 读取所有 agent workspaces
python3 -c "
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    d = json.load(f)
for a in d.get('agents', {}).get('list', []):
    print(a['id'], '→', a.get('workspace', 'N/A'))
"
```

## 测试 Hook（per-agent）

发送消息给不同 agent，观察各自 `.learnings/` 文件变化：

```bash
# 查看某个 agent 的 learnings 是否被更新
tail -f ~/.openclaw/workspace/code-dev/.learnings/LEARNINGS.md
```

Hook 根据 sessionKey 自动路由，无需手动指定。

## 调试

```bash
# 查看 distill JSON（pretty）
bash ~/.openclaw/workspace/skills/self-improvement-loop/scripts/distill.sh --check-only | python3 -m json.tool

# 查看某个 agent 的 distill
LEARNINGS_DIR="$HOME/.openclaw/workspace/code-dev/.learnings" \
  bash ~/.openclaw/workspace/skills/self-improvement-loop/scripts/distill.sh --check-only | python3 -m json.tool

# 手动触发 archive dry-run
bash ~/.openclaw/workspace/skills/self-improvement-loop/scripts/archive.sh --dry-run

# 查看某个 agent 的 learnings 文件
cat ~/.openclaw/workspace/main/.learnings/LEARNINGS.md

# 查看 pending notifications（per-agent）
ls ~/.openclaw/workspace/code-dev/.learnings/.pending_notifications/
```

## 添加新 agent

1. 在 `openclaw.json` 的 `agents.list` 中添加新 agent
2. 重新运行安装脚本：

```bash
cd ~/.openclaw/workspace/skills/self-improvement-loop
bash install.sh
```

会自动检测新增 agent，创建其 cron + learnings 目录。已有 agent 的 cron 不会被覆盖（幂等）。

## 删除 agent

1. 从 `openclaw.json` 中移除 agent
2. 手动删除其 cron：

```bash
openclaw cron remove self-improvement-<agent_id>
# 删除 learnings 目录（可选）
rm -rf ~/.openclaw/workspace/<agent_id>/.learnings
```

## 注意事项

- **无需修改 openclaw.json 后重新安装** — hook 和 cron 每次运行都动态读取 `openclaw.json`
- **LEARNINGS_DIR 硬编码在 cron 中** — 创建时注入，agent workspace 改变后需重新安装
- **所有 agent 共享同一份 scripts** — 逻辑在 `scripts/` 目录，通过环境变量隔离