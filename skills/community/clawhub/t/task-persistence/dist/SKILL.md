---
name: task-persistence
description: 自动监控和恢复会话状态、任务持久化和网关重启反馈。支持任务延续、状态快照和主动通知。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄"
      }
  }
---

# Task Persistence - 会话与任务持久化

## 功能概述

Task Persistence 技能提供完整的会话状态管理和任务恢复能力：

### 🔄 任务持久化 (Task Persistence)
- **自动保存**：长时间运行的任务自动保存状态到磁盘
- **智能恢复**：网关重启后自动检测并恢复未完成任务
- **任务队列**：支持多任务排队、暂停、恢复和取消
- **进度跟踪**：实时显示任务进度和预计完成时间

### 💾 会话快照 (Session Snapshot)
- **定期快照**：自动保存会话上下文和对话历史
- **状态恢复**：重启后从最近快照恢复对话状态
- **上下文压缩**：智能压缩历史记录，保持关键信息
- **记忆集成**：与 memory-core 插件协同工作

### 🔔 网关监控 (Gateway Monitor)
- **状态检测**：实时监控网关运行状态
- **主动通知**：重启完成后自动发送状态报告
- **健康检查**：定期执行系统健康检查
- **异常告警**：检测到问题时及时通知用户

## 使用场景

- **长时间任务**：文件处理、数据导入、批量操作等
- **系统维护**：网关更新、配置更改后的状态恢复
- **意外中断**：系统崩溃、网络断开后的任务恢复
- **日常监控**：持续监控系统状态和性能

## 命令和工具

### 任务管理
```bash
uv run {baseDir}/scripts/task_manager.py --action list
uv run {baseDir}/scripts/task_manager.py --action resume --task-id <id>
uv run {baseDir}/scripts/task_manager.py --action pause --task-id <id>
uv run {baseDir}/scripts/task_manager.py --action cancel --task-id <id>
```

### 会话快照
```bash
uv run {baseDir}/scripts/session_snapshot.py --action save --label "before-update"
uv run {baseDir}/scripts/session_snapshot.py --action restore --label "latest"
uv run {baseDir}/scripts/session_snapshot.py --action list
```

### 网关监控
```bash
uv run {baseDir}/scripts/gateway_monitor.py --action status
uv run {baseDir}/scripts/gateway_monitor.py --action health-check
uv run {baseDir}/scripts/gateway_monitor.py --action notify-restart
```

### 综合操作
```bash
# 启动完整监控
uv run {baseDir}/scripts/main.py --mode full

# 仅启用任务持久化
uv run {baseDir}/scripts/main.py --mode tasks-only

# 仅启用会话快照
uv run {baseDir}/scripts/main.py --mode snapshot-only
```

## 配置

配置文件位置：`{workspace}/config/task-persistence.json`

默认配置：
```json
{
  "task_persistence": {
    "enabled": true,
    "auto_save_interval": 30,
    "max_concurrent_tasks": 5,
    "task_dir": "{workspace}/tasks"
  },
  "session_snapshot": {
    "enabled": true,
    "snapshot_interval": 60,
    "max_snapshots": 10,
    "snapshot_dir": "{workspace}/snapshots"
  },
  "gateway_monitor": {
    "enabled": true,
    "check_interval": 10,
    "notify_on_restart": true,
    "health_check_enabled": true
  }
}
```

## 依赖

- Python 3.8+
- uv (推荐) 或 pip
- psutil (系统监控)
- OpenClaw memory-core 插件

## 最佳实践

1. **定期清理**：自动清理过期的任务和快照文件
2. **资源监控**：监控系统资源使用，避免过度消耗
3. **错误处理**：完善的错误处理和重试机制
4. **用户控制**：提供简单的命令来控制各项功能的开关

## 集成

此技能与以下技能协同工作：
- **session-monitor**：提供详细的 token 和状态信息
- **memory-core**：利用向量搜索进行智能状态恢复
- **healthcheck**：执行系统安全和性能检查
- **cron**：支持定时任务和定期快照