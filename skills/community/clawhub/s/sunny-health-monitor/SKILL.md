---
name: sunny-health-monitor
version: 1.0.0
description: Lightweight system health monitoring for macOS - monitor CPU, memory, disk usage, cron job status, and generate health reports with Discord notifications.
author: sunnyhot
license: MIT
keywords:
  - system-health
  - monitoring
  - cron-jobs
  - discord
  - macos
---

# Sunny Health Monitor - 系统健康监控

**轻量级 macOS 系统健康监控工具**

---

## ✨ 核心功能

### 🖥️ **系统资源监控**
- ✅ CPU 使用率
- ✅ 内存使用率
- ✅ 磁盘使用率
- ✅ 网络状态
- ✅ 进程监控

### ⏰ **定时任务监控**
- ✅ 检查所有 cron jobs 状态
- ✅ 识别失败任务
- ✅ 统计成功率
- ✅ 生成任务报告

### 📊 **健康报告**
- ✅ 系统资源摘要
- ✅ 定时任务状态
- ✅ 性能指标
- ✅ 优化建议
- ✅ 推送到 Discord

---

## 📊 **监控指标**

### **系统资源**

| 指标 | 正常范围 | 警告 | 严重 |
|------|---------|------|------|
| **CPU** | < 50% | 50-80% | > 80% |
| **内存** | < 70% | 70-90% | > 90% |
| **磁盘** | < 70% | 70-90% | > 90% |

### **定时任务**

| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| **成功率** | > 95% | 80-95% | < 80% |
| **失败任务** | 0 | 1-2 | > 2 |
| **超时任务** | 0 | 1-2 | > 2 |

---

## 🚀 **使用方法**

### **1. 自动监控模式**（推荐）

创建定时任务，每 30 分钟检查一次：

```bash
openclaw cron add \
  --name "system-health-monitor" \
  --cron "*/30 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --message "运行 system-health-monitor: 检查系统健康，生成报告。报告格式用中文。"
```

---

### **2. 手动触发分析**

```bash
node /Users/xufan65/.openclaw/workspace/skills/system-health-monitor/scripts/monitor.cjs
```

**功能**:
- 检查系统资源
- 分析定时任务
- 生成健康报告
- 推送到 Discord

---

### **3. 查看当前状态**

```bash
cat /Users/xufan65/.openclaw/workspace/memory/system-health-status.json
```

**包含内容**:
- 最后检查时间
- 系统资源状态
- 定时任务状态
- 健康评分

---

## 📋 **工作流程**

```
定时扫描 (每30分钟)
   ↓
检查系统资源
   ├─ CPU 使用率
   ├─ 内存使用率
   ├─ 磁盘使用率
   └─ 网络状态
   ↓
检查定时任务
   ├─ 成功任务
   ├─ 失败任务
   ├─ 超时任务
   └─ 成功率
   ↓
计算健康评分
   ↓
生成报告
   ↓
推送到 Discord
```

---

## 📊 **健康评分系统**

### **评分维度** (总分 100 分)

#### **系统资源** (40 分)
- CPU (15 分)
- 内存 (15 分)
- 磁盘 (10 分)

#### **定时任务** (40 分)
- 成功率 (20 分)
- 失败任务数 (10 分)
- 超时任务数 (10 分)

#### **系统稳定性** (20 分)
- 运行时间 (10 分)
- 错误日志 (10 分)

---

### **评分等级**

| 等级 | 分数范围 | 状态 | 说明 |
|------|---------|------|------|
| ⭐⭐⭐⭐⭐ | 90-100 | 优秀 | 系统运行完美 |
| ⭐⭐⭐⭐ | 80-89 | 良好 | 系统运行良好 |
| ⭐⭐⭐ | 70-79 | 一般 | 需要关注 |
| ⭐⭐ | 60-69 | 较差 | 需要优化 |
| ⭐ | < 60 | 危险 | 需要立即处理 |

---

## 📝 **报告格式**

### **系统健康报告**

```
📊 系统健康报告

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖥️ 系统资源
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CPU: 35% (4核 / 8核)
✅ 内存: 65% (10.4GB / 16GB)
✅ 磁盘: 45% (234GB / 512GB)
✅ 网络: 正常

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 定时任务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

总任务: 15 个
✅ 成功: 13 个
❌ 失败: 2 个
⏱️ 超时: 0 个

成功率: 86.7%

失败任务:
  • Daily Auto-Update
  • deals-noon

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 健康评分: 85/100 ⭐⭐⭐⭐

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 优化建议

1. 修复 2 个失败任务
2. 检查 deals-noon 超时问题
3. 考虑增加超时时间

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 **配置文件**

### `config/monitor.json`

```json
{
  "system": {
    "cpu": {
      "warning": 50,
      "critical": 80
    },
    "memory": {
      "warning": 70,
      "critical": 90
    },
    "disk": {
      "warning": 70,
      "critical": 90
    }
  },
  "cronJobs": {
    "warningThreshold": 2,
    "criticalThreshold": 5,
    "successRateWarning": 80,
    "successRateCritical": 60
  },
  "notifications": {
    "channel": "discord",
    "to": "channel:1478698808631361647",
    "onWarning": true,
    "onCritical": true
  }
}
```

---

## 📊 **状态文件**

### `memory/system-health-status.json`

```json
{
  "lastCheck": "2026-03-12T20:30:00+08:00",
  "healthScore": 85,
  "system": {
    "cpu": 35,
    "memory": 65,
    "disk": 45
  },
  "cronJobs": {
    "total": 15,
    "success": 13,
    "failed": 2,
    "timeout": 0,
    "successRate": 86.7
  },
  "status": "good",
  "recommendations": [
    "修复 2 个失败任务",
    "检查 deals-noon 超时问题"
  ]
}
```

---

## 🎯 **监控的系统**

### **OpenClaw 系统**
- ✅ OpenClaw 运行状态
- ✅ 定时任务执行状态
- ✅ 技能同步状态
- ✅ 日志分析状态

### **系统资源**
- ✅ CPU 使用率
- ✅ 内存使用率
- ✅ 磁盘使用率
- ✅ 网络连接状态

---

## 💡 **智能建议**

### **自动建议**（基于分析）

1. **资源优化**
   ```
   检测到: CPU 使用率过高 (>80%)
   建议: 关闭不必要的进程或升级硬件
   ```

2. **任务优化**
   ```
   检测到: deals-noon 多次超时
   建议: 增加超时时间或优化任务
   ```

3. **安全建议**
   ```
   检测到: 磁盘使用率接近 90%
   建议: 清理不必要的文件或扩展存储
   ```

---

## 📝 **更新日志**

### v1.0.0 (2026-03-12)
- ✅ 初始版本
- ✅ 系统资源监控
- ✅ 定时任务监控
- ✅ 健康评分系统
- ✅ 报告生成
- ✅ Discord 推送

---

**🚀 让你的系统健康监控更加智能和高效！**
