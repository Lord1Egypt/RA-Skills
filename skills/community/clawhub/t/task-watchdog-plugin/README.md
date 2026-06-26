# openclaw-task-watchdog

**OpenClaw Task Watchdog Plugin** — Auto-notify on subagent failures, exec errors, and stale tasks.

[OpenClaw 任务看门狗插件](#中文说明) — 子 agent 失败、exec 异常退出、任务停滞时自动通知。

---

## The Problem

When OpenClaw runs long tasks via subagents or `exec`, failures can go unnoticed. Users end up repeatedly checking "is it done yet?" or tasks silently stall without anyone knowing.

**Task Watchdog solves this** by monitoring task lifecycle events and injecting timely notifications into the parent session — so you always know when something needs attention.

## Features

| Hook | What it does |
|------|-------------|
| **`subagent_ended`** | Detects abnormal subagent outcomes (error, timeout, killed, reset, deleted) and notifies the parent session. Also sends continuation reminders on normal completions. |
| **`after_tool_call` (exec)** | Watches for abnormal `exec` exits — non-zero exit codes, OOM kills, signals, permission denied, command not found. |
| **`heartbeat_prompt_contribution`** | When timer patrol is off, injects patrol instructions into heartbeat cycles to check for stale running tasks. |
| **`gateway_start`** | Starts a timer-based patrol that periodically requests heartbeats to trigger stale-task checks. |

### Key Design Decisions

- **Deadlock-safe**: Uses in-process API calls instead of spawning CLI commands.
- **Idempotent**: Each notification uses an `idempotencyKey` to prevent duplicates.
- **Zero-config**: Works out of the box with sensible defaults.

## Installation

```bash
# Via OpenClaw plugin install
openclaw plugin install openclaw-task-watchdog

# Via npm
npm install openclaw-task-watchdog
```

## Configuration

All settings are optional. Configure via `openclaw.plugin.json` → `config`:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `subagentNotifyOn` | `string[]` | `["error", "timeout", "killed"]` | Subagent outcomes that trigger notifications. Options: `error`, `timeout`, `killed`, `reset`, `deleted` |
| `execNotifyOnAbnormal` | `boolean` | `true` | Enable notifications on abnormal exec exits |
| `injectionTtlMs` | `integer` | `300000` (5 min) | TTL for next-turn injection messages (5000–600000 ms) |
| `timerPatrol` | `boolean` | `true` | Enable timer-based patrol on gateway start. When enabled, heartbeat patrol is skipped. |
| `heartbeatPatrol` | `boolean` | `false` | Enable heartbeat-based patrol. Only effective when timerPatrol is disabled. |
| `timerPatrolIntervalMs` | `integer` | `120000` (2 min) | Timer patrol interval (30000–600000 ms) |
| `staleThresholdMs` | `integer` | `1800000` (30 min) | How long before a running task is considered stale (60000–7200000 ms) |

Example configuration:

```json
{
  "task-watchdog": {
    "subagentNotifyOn": ["error", "timeout", "killed", "reset"],
    "timerPatrolIntervalMs": 180000,
    "staleThresholdMs": 900000
  }
}
```

## Development

```bash
# Install dependencies
npm install

# Build
npx tsc

# Build and watch
npx tsc --watch
```

## Changelog

### v1.1.0 (2026-05-12)

**Bug Fixes:**
- 🔴 Fixed interval leak: idempotency map cleanup `setInterval` now properly cleared on `gateway_stop`
- 🔴 Fixed `heartbeatPatrol` logic: clear mutual exclusion with `timerPatrol`, now works correctly when timer patrol is disabled
- Added `heartbeatPatrol` to `configSchema` for discoverability

**Improvements:**
- 🟡 `injectionTtlMs` config now respected instead of hardcoded 60s TTL
- 🟡 Added optional chaining on `api.runtime.system.*` calls for API version safety
- 🟡 `reason` and `error` fields truncated to 200 chars to prevent oversized notifications
- 🟡 `notifiedKeys` Map capped at 10,000 entries with oldest-half eviction
- 🟡 `JSON.stringify` wrapped in try-catch for circular reference safety
- All timer cleanup unified under single `gateway_stop` handler

## License

MIT

---

## 中文说明

### 解决什么问题？

OpenClaw 通过子 agent 或 `exec` 执行长任务时，失败可能被忽略。用户不得不反复检查进度，或者任务默默停滞无人知晓。

**Task Watchdog** 监控任务生命周期事件，在需要关注时自动向父 session 注入通知。

### 四个 Hook

1. **子 agent 结束监控** — 检测异常退出（错误、超时、被杀、重置、删除）并通知父 session。正常完成也会发送延续提醒。
2. **exec 异常检测** — 监控非零退出码、OOM kill、信号终止、权限拒绝等异常。
3. **心跳巡检注入** — 在关闭定时巡检时，通过心跳周期注入巡检指令检查停滞任务。
4. **定时巡检** — gateway 启动时开启定时器，定期触发心跳检查停滞任务。

### 安装

```bash
openclaw plugin install openclaw-task-watchdog
```

### 开发构建

```bash
npm install && npx tsc
```
