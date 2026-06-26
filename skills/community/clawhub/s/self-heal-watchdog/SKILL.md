---
name: self-heal-watchdog
description: >
  Automated self-healing system for OpenClaw gateway with model failover support.
  Three-layer protection: process watchdog (auto-restart on crash), config guard (backup + rollback),
  and model health check (auto-switch to fallback model on API failure).
  Use for: gateway monitoring, automatic recovery, model failover, crash recovery, uptime protection.
  Triggers: watchdog, self-heal, monitoring, recovery, failover, health check, gateway restart.
---

# Self-Heal Watchdog 🛡️

三层自愈保护系统，监控 OpenClaw Gateway 进程、配置完整性和模型响应。

## 安装

```bash
bash skills/self-heal-watchdog/scripts/setup.sh
```

使用 **launchd**（macOS 原生调度器），每 60 秒运行一次。

## 手动命令

| 命令 | 说明 |
|------|------|
| `bash scripts/status.sh` | 查看当前状态和最近日志 |
| `bash scripts/status.sh --full` | 查看完整日志 |
| `bash scripts/watchdog.sh` | 手动运行一次看门狗 |
| `bash scripts/watchdog.sh --dry-run` | 干运行（不执行任何操作） |
| `bash scripts/model-failover.sh` | 手动触发模型切换 |
| `bash scripts/setup.sh --uninstall` | 卸载看门狗 |

## 三层保护

### 1. Process Watchdog
每分钟检测 gateway 进程是否存活，崩溃自动 restart。

### 2. Config Guard
每次检查前备份 `~/.openclaw/openclaw.json`，配置损坏自动回滚。

### 3. Model Health Check
通过 `/health` 端点检测模型响应，连续 2 次失败自动切换 fallback 模型。

## 文件说明

| 文件 | 用途 |
|------|------|
| `scripts/watchdog.sh` | 主脚本（cron 每分钟调用） |
| `scripts/health-check.sh` | 健康检查逻辑 |
| `scripts/model-failover.sh` | 模型切换逻辑 |
| `scripts/setup.sh` | 安装/卸载 |
| `scripts/status.sh` | 状态查看 |

## 配置

- **状态文件:** `~/.openclaw/watchdog-state.json`
- **日志文件:** `~/.openclaw/watchdog/watchdog.log`
- **Gateway URL:** `http://localhost:18789`
- **检查间隔:** 1 分钟（cron）
- **失败阈值:** 连续 2 次触发 failover

## 安全

- 所有脚本仅监听 localhost
- 不记录 API key/token
- 日志自动轮转（保留 1000 行）
- 修改配置前先备份
