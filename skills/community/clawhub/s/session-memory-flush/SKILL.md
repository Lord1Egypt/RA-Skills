---
name: session-memory-flush
description: 在 OpenClaw session 即将因 idle/reset 释放前，扫描 `openclaw sessions --json` 可见会话，读取 transcript，提炼高价值上下文并写入 workspace memory 文件，降低新 session 的失忆感。用于 main、native subagent、cron、dreaming 等会话的 idle 前摘要回收；当需要安装、验证、调试、交付这个 skill，或需要解释它与 builtin memory / per-agent SQLite index / workspace 共享范围的关系时使用。
---

# session-memory-flush

## 目标

在 OpenClaw session 因 idle 自动释放前，读取当前 session transcript，优先调用 `openclaw.json` 中 `agents.defaults.model.primary` 对应提供者做 LLM 摘要，并把值得后续继续工作的上下文写入短期记忆文件。

默认写入 `~/.openclaw/workspace/memory/YYYY-MM-DD.md`；也可用 `SESSION_MEMORY_OUTPUT_DIR` 或 `openclaw.json > sessionMemoryFlush.outputDir` 覆盖输出目录。

## 能保证什么，不能保证什么

### 这个 skill 能保证的

- 扫描 `openclaw sessions --json` 当前可见的 session
- 在 transcript 可定位时，回收 main / native subagent / cron / dreaming 等 session 的摘要
- 当前版本会按 `session.agentId` 感知 transcript 与模型配置，不再把所有 session 偷偷当成 `main`
- 摘要写入 memory markdown，供**共享同一 workspace / 同一记忆文件加载链路**的新 session 继续读取

### 这个 skill 不能单独保证的

- **不能保证不同 agentId 天然共享 builtin memory**
- OpenClaw builtin memory index 是 **per-agent SQLite database**，路径类似 `~/.openclaw/memory/<agentId>.sqlite`
- 所以“其他 agent 也一样”是否成立，取决于它们是否共享：
  - 同一 workspace
  - 同一 `memory/*.md` 读取链路
  - 同一 memory search / index 配置范围
- 如果是完全独立的 agentId / workspace，这个 skill 只能保证“成功 flush 到某个 memory 文件”，不能替 OpenClaw 保证“所有 agent 后续都会天然读到同一份记忆”

## 当前环境如何判断

如果 `openclaw sessions --json` 里看到的 session 都是同一个 `agentId`（比如全是 `main`），那你的实际运行效果通常可以近似理解为：

- main session：可以受益
- native subagent：通常也可以受益
- dreaming / cron：只要 transcript 可见，也可以被回收

但这依然是因为它们**实际落在同一个 agent scope**，不是因为这个 skill 神奇地跨 agent 统一了 builtin memory。

## 不处理的场景

- `/new`
- `/reset`
- 用户明确要求清空上下文

这些场景视为用户主动重置，不做旧会话回收。

## 处理的场景

- 私聊超过 idle 阈值前
- 群聊超过 idle 阈值前
- 运维手动指定 sessionId 强制 flush

## 摘要输出格式

```markdown
## YYYY-MM-DD HH:mm 会话摘要

来源：agent=<agentId> / channel / type / sessionId=xxx

- 本轮目标：
- 已完成事项：
- 重要决策：
- 用户偏好：
- 待办事项：
- 风险和未完成上下文：
```

## 摘要规则

- 不保留完整聊天原文
- 不写临时寒暄
- 只保留后续任务真正需要的信息
- 单个 session 摘要控制在 300-800 字
- 敏感信息按公司安全规则脱敏
- 去重键按 `agentId:sessionId` 记录，避免不同 agent 误判为同一条 session
- LLM 调用失败时，允许降级为本地规则摘要，保证任务不中断

## 运行方式

定时运行：

```bash
bash install.sh
```

默认行为不再写死在 skill 里，而是按下面顺序取值：

1. 环境变量（最高优先级）
2. `openclaw.json > sessionMemoryFlush`
3. OpenClaw 自身的 `openclaw.json > session.reset/session.resetByType`
4. 最后才回退到保底值

其中：

- 私聊 idle 优先复用 `session.resetByType.direct.idleMinutes`
- 群聊 idle 优先复用 `session.resetByType.group.idleMinutes`
- 轮询频率优先读 `sessionMemoryFlush.timerMinutes`
- scan window 优先读 `sessionMemoryFlush.scanWindowMinutes`

推荐在 `openclaw.json` 里显式加一段：

```json
{
  "sessionMemoryFlush": {
    "timerMinutes": 1,
    "idleMinutes": {
      "direct": 5,
      "group": 30
    },
    "scanWindowMinutes": {
      "direct": 1,
      "group": 5
    },
    "outputDir": "$HOME/.openclaw/workspace/memory"
  }
}
```

仍可通过环境变量覆盖：

```bash
SESSION_MEMORY_TIMER_MINUTES=1 \
SESSION_MEMORY_DM_IDLE_MINUTES=5 \
SESSION_MEMORY_GROUP_IDLE_MINUTES=30 \
SESSION_MEMORY_SCAN_WINDOW_DM=1 \
SESSION_MEMORY_SCAN_WINDOW_GROUP=5 \
SESSION_MEMORY_OUTPUT_DIR="$HOME/.openclaw/workspace/memory" \
bash install.sh
```

如果什么都不传，`install.sh` 会直接读 `~/.openclaw/openclaw.json` 生成 timer/service。

手动试跑：

```bash
python3 watcher.py --once --dry-run
```

强制处理指定 session：

```bash
python3 watcher.py --once --force-session <sessionId>
```

## 交付建议

## 安全与隐私边界

- 发布前应保持 `state/flushed_sessions.json` 为空状态：`{"flushed_sessions": {}}`。
- 不要随 skill 一起发布真实的 `openclaw.json`、session `jsonl`、memory markdown、SQLite 数据库、日志、缓存目录或任何本地运行产物。
- 该 skill 会读取本机 OpenClaw session transcript，并优先使用当前用户 `openclaw.json` 中配置的模型提供商生成摘要；这意味着 transcript 可能会发送给用户自己配置的 LLM provider。
- `watcher.py` 只在运行时读取本机 `openclaw.json` 或环境变量中的 API key 用于请求模型，不会把 API key 写入 `state`、memory markdown 或日志。
- 如果部署环境不允许 transcript 出网，应通过内网模型、专用 `SESSION_MEMORY_LLM_*` 配置，或依赖本地规则摘要兜底。

如果要做成更稳的标准交付，建议把外部描述统一写成下面这句：

> 该 skill 会在 session 即将 idle/reset 释放前，把 transcript 摘要写入 memory 文件，降低后续新 session 的失忆感；它对当前 `openclaw sessions --json` 可见的 session 普遍适用，但不同 `agentId` 是否能共享后续记忆效果，仍取决于 workspace、memory 文件加载链路以及 builtin memory 的 per-agent 索引边界。
