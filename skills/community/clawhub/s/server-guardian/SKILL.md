---
name: server-guardian
description: 服务器健康监控与自动恢复技能。当服务器出现卡顿、崩溃、Bot 连接异常或网关中断时使用此技能。支持：执行健康检查、自动诊断故障、一键恢复 Gateway、清理内存/磁盘、整理日志、检查 OOM Killer 等操作。触发场景包括：服务器变慢、Bot 无响应、日志报 ERROR、内存/磁盘告警、进程消失等任何异常情况。注意：API 访问限流为 60 秒内最多 40 次。
---

# Server Guardian

## Overview

OpenClaw 服务器的"守护神"，负责检测、诊断和自动修复服务器异常。

**核心能力：**
1. **健康检查** — 5 维度全面诊断（CPU / 内存 / 磁盘 / 进程 / 日志）
2. **自动恢复** — 根据诊断结果执行对应修复，无需人工干预
3. **预防性维护** — 日志整理、OOM 检查、配置优化

## Quick Start

遇到服务器异常时，直接说：
- "执行健康检查"
- "检查服务器状态"
- "Gateway 挂了，帮我看看"
- "服务器好卡，诊断一下"

## Workflow

```
发现异常
  ↓
执行 health_check.sh（健康检查）
  ↓
┌─ OK     → 正常，无需操作
├─ WARN   → 关注，可选执行 auto_recover.sh
└─ CRITICAL → 立即执行 auto_recover.sh full
```

## Health Check

运行诊断脚本（无需参数）：

```bash
bash /root/.openclaw/workspace/skills/server-guardian/scripts/health_check.sh
```

**检查 5 大维度：**

| 维度 | 检查内容 | 告警阈值 |
|------|----------|----------|
| 系统 | CPU 负载 | > 2×核心数 |
| 系统 | 内存使用率 | > 90% |
| 系统 | 磁盘使用率 | > 90% |
| 进程 | Gateway 存活 | 进程消失 |
| 进程 | OpenClaw 进程数 | 进程消失 |
| 网络 | Gateway API 端口 | 端口不通 |
| 日志 | ERROR/FATAL 关键词 | 任意 1 个 |
| 系统 | 崩溃日志（journalctl） | 最近 1h 有记录 |

**退出码：**
- `0` = 正常
- `1` = 警告（建议关注）
- `2` = 严重（立即处理）

## Auto Recovery

自动恢复脚本，支持多种操作：

```bash
bash /root/.openclaw/workspace/skills/server-guardian/scripts/auto_recover.sh <action>
```

| action | 说明 |
|--------|------|
| `check` | 执行健康检查（同上） |
| `restart` | 仅重启 Gateway |
| `full` | **推荐** 完整恢复流程（整理日志→检查OOM→清理内存→重启Gateway→验证） |
| `mem` | 清理内存缓存 |
| `procs` | 查找并处理高内存进程 |
| `logs` | 压缩大日志 + 清理 30 天+旧日志 |
| `disk` | 清理磁盘空间（npm/pnpm 缓存） |
| `oom` | 检查 OOM Killer 记录 |
| `optimize` | 输出 Gateway 配置优化建议 |
| `menu` | 交互式菜单 |

**推荐使用 `full`**，一次性完成完整恢复。

## OOM Killer 检测

内存耗尽时系统会触发 OOM Killer 自动杀掉进程。若检测到 OOM：

**表现：**
- Bot 进程突然消失
- `dmesg | grep killed` 有输出
- Gateway 日志无错误但进程没了

**处理建议：**
- 增加 SWAP 空间
- 在 `gateway.yml` 中添加内存限制
- 使用 `auto_recover.sh full` 重启恢复

## Gateway 重启

```bash
# 标准重启（推荐）
openclaw gateway restart

# 强制启动
openclaw gateway start

# 查看状态
openclaw gateway status
```

重启后等待 5-8 秒再验证是否成功。

## 告警阈值参考

详见 [references/thresholds.md](references/thresholds.md)

## 故障排查指南

详见 [references/troubleshooting.md](references/troubleshooting.md)
