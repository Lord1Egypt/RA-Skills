---
name: 金刚罩
version: 1.1.0
description: "金刚罩 — OpenClaw 系统守护：配置安全（pre-validate + 自动备份 + 失败回滚）、健康巡检、资源优化、故障自愈。刀枪不入，百毒不侵。"
author: 主谋
emoji: 🔱
tags:
  - system
  - guardian
  - resilience
  - rollback
  - health
  - optimization
metadata:
  openclaw:
    requires:
      bins: [openclaw, python3]
---

# 🔱 金刚罩 — 刀枪不入，百毒不侵

让 OpenClaw 更强壮、更高效、不容易崩溃。

## 核心能力

### 1. 安全重启（Safe Restart）

**永远不要直接跑 `openclaw gateway restart`**，使用：

```bash
bash ~/.openclaw/skills/system-guardian/scripts/safe-restart.sh
```

流程：
```
校验配置 → 自动备份(3件套) → 重启 Gateway → 健康检查 → 失败则自动回滚
```

详细步骤：
1. `openclaw config validate` — 配置语法和字段校验
2. 备份三个关键文件到 `~/.openclaw/backups/`：
   - `openclaw.json.<timestamp>.bak` — 主配置
   - `env.<timestamp>.bak` — 环境变量
   - `ai.openclaw.gateway.plist.<timestamp>.bak` — macOS 开机自启配置
3. `openclaw gateway restart`
4. 等待 15 秒，检查 `openclaw gateway status`
5. 如果 Gateway 不在线：自动恢复全部备份 → 再次重启 → 再次检查
6. 如果仍然失败：报警并保留现场

### 2. 配置变更防护（Config Guard）

修改 `openclaw.json` 前调用：

```bash
bash ~/.openclaw/skills/system-guardian/scripts/config-guard.sh check
```

检查项目：
- JSON 语法是否合法
- 必需字段是否存在（gateway, channels, agents）
- 自动检测配置模式：**env-based**（使用 `${VAR}` 引用 .env）或 **inline**（密钥直接写在 openclaw.json 中），两种都支持
- 端口冲突检查
- 磁盘空间检查

### 3. 健康巡检（Health Patrol）

```bash
bash ~/.openclaw/skills/system-guardian/scripts/health-patrol.sh
```

检查项目（13 项）：
1. Gateway 进程状态 + 内存占用（>1GB 警告，>1.5GB 严重）
2. 磁盘空间（总量、可用）
3. OpenClaw 目录空间细分
4. Session 文件累积
5. 记忆数据库大小
6. 备份文件管理
7. **Cron 任务健康**：检测连续失败的任务并告警
8. **插件健康检查**：检查所有已安装插件的状态和加载情况
9. **配置变更审计**：检测 openclaw.json 变更，记录 diff 到审计日志
10. 临时文件清理
11. **自动清理**：Session >14天自动删、备份保留最近10份、日志保留7天
12. **性能基线记录**：每次巡检记录指标到 CSV，可看趋势和泄漏检测
13. 审计日志管理（超过 1MB 自动轮转）

### 4. 资源优化建议（Resource Advisor）

根据当前系统状态给出优化建议：
- Session transcript 过大时建议清理
- 备份文件过多时建议归档
- 磁盘空间低于 10GB 时预警
- 内存占用异常时分析原因
- 模型使用效率分析（哪些 cron 可以用更轻的模型）

## Agent 使用指南

当需要修改配置或重启 Gateway 时，按以下流程操作：

```
1. 修改 openclaw.json
2. 运行 config-guard.sh check 验证
3. 如果验证通过 → 运行 safe-restart.sh
4. 如果验证失败 → 修复问题后重试
```

**铁律：任何配置变更必须经过 safe-restart.sh，禁止直接 `openclaw gateway restart`**

## 推荐 Cron 配置

```json5
{
  "name": "system-health-patrol",
  "description": "每日凌晨 4:00 系统健康巡检 + 资源清理",
  "schedule": { "kind": "cron", "expr": "0 4 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" },
  "payload": {
    "kind": "agentTurn",
    "model": "anthropic/claude-sonnet-4-6",
    "timeoutSeconds": 120,
    "message": "运行系统健康巡检：bash ~/.openclaw/skills/system-guardian/scripts/health-patrol.sh\n读取输出并总结巡检结果。如果发现 CRITICAL 或 WARNING，输出问题说明和建议处理方式。如果全部 OK，输出：系统健康 ✅ 无异常。"
  }
}
```

## 数据文件

巡检产生的数据存储在 `~/.openclaw/data/system-guardian/`：
- `baseline.csv` — 性能基线时序数据（Gateway 内存、磁盘、Session 数等）
- `config-audit.log` — 配置变更审计日志（时间 + hash + diff）
- `.config-hash` / `.config-snapshot.json` — 用于变更检测

## 版本历史

- v1.0: 安全重启 + 配置防护 + 健康巡检（8项）
- v1.1: Cron 健康监控 + 插件检查 + 配置审计 + 自动清理 + 性能基线（13项）
- v2.0: 多节点健康管理（计划中）
