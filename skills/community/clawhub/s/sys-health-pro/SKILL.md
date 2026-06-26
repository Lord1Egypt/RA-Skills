---
name: system-health-monitor
version: 1.0.0
description: 系统健康监控工具。监控 CPU、内存、磁盘、网络连接等，发现异常时告警。适合服务器/工作室/个人电脑。
author: 你的名字
triggers:
  - "系统监控"
  - "服务器状态"
  - "健康检查"
  - "资源监控"
---

# System Health Monitor 💻

监控系统资源状态，发现异常及时告警。

## 功能

- 🖥️ CPU 使用率监控
- 💾 内存使用监控
- 💿 磁盘空间监控
- 🌐 网络连接监控
- 🔔 异常告警
- 📊 定时报告

## 使用方法

### 查看当前状态

```bash
python3 scripts/health.py status
```

### 详细报告

```bash
python3 scripts/health.py report
```

### 持续监控（每 60 秒）

```bash
python3 scripts/health.py watch
```

### 设置告警阈值

```bash
python3 scripts/health.py alert --cpu 90 --memory 85
```

## 示例

```bash
# 查看系统状态
python3 scripts/health.py status

# 生成完整报告
python3 scripts/health.py report
```
