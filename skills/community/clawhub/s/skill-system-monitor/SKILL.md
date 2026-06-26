---
name: skill-system-monitor
description: 跨平台系统监控工具，支持 Linux 和 Windows，监控硬盘、内存、CPU 使用情况，记录历史数据，支持变化对比和预警。**适合定时任务**。触发场景：(1) 定时系统健康检查（推荐每6小时），(2) 用户询问系统状态、资源使用情况，(3) 资源异常预警，(4) 查看历史监控数据对比。
---

# System Monitor - 系统监控技能

跨平台系统监控工具，**自动检测操作系统类型**，支持 Linux 和 Windows，用于监控服务器硬盘、内存、CPU 使用情况，记录历史快照，支持变化趋势对比和异常预警。

**🎯 本技能特别适合定时任务使用**，推荐频率：
- 生产服务器：1-2 小时
- 个人服务器：2-4 小时  
- 开发环境：6-12 小时

## 功能特点

- 💾 **硬盘监控** - 检查硬盘使用率，支持预警阈值
- 🧠 **内存监控** - 检查内存和 Swap/页面文件使用情况
- ⚙️ **CPU 负载** - 监控 CPU 负载/使用率
- 📊 **进程监控** - 显示资源占用 TOP 进程
- ⏱️ **运行时间** - 显示系统运行时长
- 🌐 **网络流量** - 监控网络接收/发送流量
- 💿 **磁盘 I/O** - 磁盘读写速率和利用率（Linux）
- 🐳 **Docker 状态** - 容器运行/停止数量（Linux）
- 🔧 **服务状态** - 关键服务运行状态（MongoDB/MySQL/PostgreSQL/Docker/Nginx/OpenClaw）
- 📜 **历史记录** - 自动保存监控快照
- 📈 **趋势对比** - 对比历史数据，分析变化趋势
- ⚠️ **异常预警** - 自动判断状态并预警
- 🖥️ **跨平台支持** - 自动检测 Linux/Windows/macOS，调用对应脚本

## 配置说明

### 配置文件位置

配置文件按优先级查找：
1. **环境变量指定**: `$SYSTEM_MONITOR_CONFIG`
2. **技能配置目录**: `~/.openclaw/skills/config/skill-system-monitor/config.json` ⭐ **推荐**
3. **技能安装目录**: `~/.openclaw/skills/skill-system-monitor/config.json`

> **推荐**：使用技能配置目录（#2），独立于技能安装目录，卸载重装不会丢失配置。

### 快速配置

**1. 复制示例配置：**
```bash
mkdir -p ~/.openclaw/skills/config/skill-system-monitor
cp ~/.openclaw/skills/skill-system-monitor/config.example.json ~/.openclaw/skills/config/skill-system-monitor/config.json
```

**2. 编辑配置：**
```bash
nano ~/.openclaw/skills/config/skill-system-monitor/config.json
```

### 配置项说明

```json
{
  "alerts": {
    "disk": {
      "warning": 70,      // 硬盘警告阈值 (%)
      "critical": 85      // 硬盘危险阈值 (%)
    },
    "memory": {
      "warning": 70,      // 内存警告阈值 (%)
      "critical": 85      // 内存危险阈值 (%)
    },
    "cpu": {
      "warning": 1,       // CPU 负载警告 (倍核心数)
      "critical": 2       // CPU 负载危险 (倍核心数)
    }
  },
  "monitor": {
    "disk": true,         // 是否监控硬盘
    "memory": true,       // 是否监控内存
    "swap": true,         // 是否监控 Swap
    "cpu": true,          // 是否监控 CPU
    "uptime": true,       // 是否显示运行时间
    "network": true,      // 是否监控网络流量
    "disk_io": true,      // 是否监控磁盘 I/O
    "docker": true,       // 是否监控 Docker
    "services": true,     // 是否监控关键服务
    "top_processes": 5    // TOP 进程数量
  }
}
```

### 禁用某些监控

如果不需要某些监控项，可以设置为 `false`：

```json
{
  "monitor": {
    "disk_io": false,     // 不监控磁盘 I/O
    "docker": false,      // 不监控 Docker
    "services": false     // 不监控服务状态
  }
}
```

### 自定义服务监控（Linux）

服务监控使用 systemd，如需自定义，可在脚本中修改 `check_service` 函数。

### 自定义预警阈值

根据服务器配置调整阈值：

```json
{
  "alerts": {
    "disk": {
      "warning": 80,      // 硬盘 80% 才警告
      "critical": 90      // 硬盘 90% 才危险
    },
    "memory": {
      "warning": 80,
      "critical": 90
    }
  }
}
```

## 使用方法

### 方式一：随时调用（手动触发）

直接运行监控脚本，获取当前系统状态：

```bash
# Linux / macOS（自动检测）
bash /path/to/skill-system-monitor/scripts/monitor.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File scripts\monitor-windows.ps1
```

**适用场景**：
- 用户询问"系统状态"、"服务器监控"、"资源使用情况"
- 排查性能问题
- 临时检查系统健康

### 方式二：定时任务（推荐）

通过 OpenClaw cron 配置定时监控，自动检测并报告：

```json
{
  "name": "系统监控（每6小时）",
  "schedule": { "kind": "every", "everyMs": 21600000 },
  "payload": {
    "kind": "systemEvent",
    "text": "系统监控检查：运行监控脚本，报告系统状态，如有异常立即预警。"
  },
  "sessionTarget": "main"
}
```

**适用场景**：
- 定期健康检查（建议每 6 小时）
- 7x24 小时无人值守监控
- 异常自动告警通知

### 方式三：对比历史数据

查看资源使用趋势变化：

```bash
bash scripts/compare.sh
```

输出示例：
```
📊 系统监控报告
==================
主机: wezn
时间: 2026-03-14 20:57:50
运行时间: up 1 day, 9 hours, 55 minutes

💾 硬盘状态
总容量: 69G | 已用: 45G (68%) | 可用: 22G
状态: ✅正常

🧠 内存状态
总内存: 4G | 已用: 2G (50%) | 可用: 2G
Swap: 1G/2G
状态: ✅正常

⚙️ CPU 负载 (4核)
1分钟: 0.01 | 5分钟: 0.03 | 15分钟: 0.00
状态: ✅正常

🌐 网络流量
接收: 360.2 MB | 发送: 385.9 MB

💿 磁盘 I/O
读: 0/s, 写: 0/s, 利用率: 0.0%

🐳 Docker 容器
运行: 0, 停止: 3

🔧 关键服务
MongoDB: ✅ | MySQL: ✅ | PostgreSQL: ✅
Docker: ✅ | Nginx: ✅ | OpenClaw: ✅

🔴 资源占用 TOP 5 (内存)
1. clawdbot-gateway - 1122M (30.1%)
2. node (fund) - 129M (3.4%)
3. mongod - 103M (2.7%)
...
```

### 对比历史数据

```bash
bash scripts/compare.sh
```

输出示例：
```
📈 变化趋势对比
==================
对比时间: 2026-03-14 14:00 → 2026-03-14 20:48

💾 硬盘: 71% → 68% (-3%)
🧠 内存: 55% → 49% (-6%)
```

### 查看历史记录

```bash
# 列出所有历史记录
ls history/

# 查看特定记录
cat history/2026-03-14_20-48.log
```

## 目录结构

```
skill-system-monitor/
├── SKILL.md              # 技能说明文档
├── scripts/
│   ├── monitor.sh        # 主监控脚本（自动检测 OS）
│   ├── monitor-linux.sh  # Linux 监控脚本
│   ├── monitor-windows.ps1 # Windows 监控脚本 (PowerShell)
│   └── compare.sh        # 对比脚本（分析变化趋势）
└── history/              # 历史记录目录
    ├── YYYY-MM-DD_HH-MM.json  # JSON 格式（用于对比）
    └── YYYY-MM-DD_HH-MM.log   # 文本格式（人类可读）
```

## 定时监控配置

### 推荐：通过 OpenClaw Cron 配置

使用 `cron` 工具配置定时监控任务：

```json
{
  "name": "系统监控（每6小时）",
  "schedule": { "kind": "every", "everyMs": 21600000 },
  "payload": {
    "kind": "systemEvent",
    "text": "系统监控检查：请运行监控脚本，检查系统健康状态，如有异常立即报告。"
  },
  "sessionTarget": "main"
}
```

### 定时任务配置示例

**每 6 小时监控（推荐）：**
```json
{
  "name": "系统健康检查",
  "schedule": { "kind": "every", "everyMs": 21600000 },
  "payload": {
    "kind": "systemEvent",
    "text": "执行系统监控：运行 bash /home/app/.openclaw/skills/skill-system-monitor/scripts/monitor.sh，检查硬盘、内存、CPU、服务状态，如有异常立即预警。"
  },
  "sessionTarget": "main"
}
```

**每天早上 9 点监控：**
```json
{
  "name": "每日系统报告",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "systemEvent",
    "text": "每日系统报告：运行监控脚本，生成系统状态报告。"
  },
  "sessionTarget": "main"
}
```

### 预警行为

当监控发现异常时，会在报告中显示 ⚠️ 预警信息：
- 硬盘使用率 ≥ 警告阈值（默认 70%）
- 内存使用率 ≥ 警告阈值（默认 70%）
- CPU 负载过高（> 2倍核心数）
- 关键服务停止运行

**预警级别：**
- ✅ **正常**：资源使用在合理范围内
- ⚠️ **警告**：资源使用偏高，建议关注
- 🔴 **危险**：资源使用过高，需要立即处理

## 注意事项

1. **跨平台支持**：脚本会自动检测操作系统，调用对应平台的监控命令
2. **权限要求**：
   - Linux: 需要读取 `/proc` 文件系统和执行 `df`, `free` 等命令
   - Windows: 需要运行 PowerShell 脚本的权限
3. **历史记录**：会持续累积，建议定期清理旧记录
4. **预警阈值**：可在脚本中根据实际情况调整
5. **依赖工具**：
   - Linux: `bc`（**必需**，用于 CPU 状态计算）、`iostat`（可选，磁盘 I/O）
   - 安装命令：`apt install bc sysstat -y`（Debian/Ubuntu）
   - Windows: 无额外依赖

## 适用系统

| 平台 | 支持状态 | 脚本文件 |
|------|----------|----------|
| Linux (Ubuntu/Debian) | ✅ 完全支持 | `monitor-linux.sh` |
| Linux (CentOS/RHEL) | ✅ 完全支持 | `monitor-linux.sh` |
| Linux (Alpine) | ✅ 完全支持 | `monitor-linux.sh` |
| macOS | ⚠️ 部分支持 | `monitor-linux.sh` |
| Windows 10/11 | ✅ 完全支持 | `monitor-windows.ps1` |
| Windows Server | ✅ 完全支持 | `monitor-windows.ps1` |
| WSL | ✅ 完全支持 | `monitor-linux.sh` |
