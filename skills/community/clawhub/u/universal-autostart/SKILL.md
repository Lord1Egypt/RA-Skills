---
name: universal-autostart
description: Cross-platform auto-start service manager for Windows and macOS. Supports installing, uninstalling, starting, stopping, and monitoring services with automatic restart. Use when you need to set up persistent background services that survive system reboots on Windows (sc/schtasks) or macOS (launchd).
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python", "python3"] },
        "platforms": ["windows", "macos"],
      },
  }
---

# Universal AutoStart Service Manager v1.1

跨平台的自启动服务管理器，支持 Windows 和 macOS。可以安装、卸载、启动、停止和监控服务，并支持自动重启。

## 🚀 快速开始

### Windows 安装

创建 `install_windows.bat` 文件（纯文本，保存为 UTF-8 编码）：

```batch
@echo off
chcp 65001 >nul
echo ============================================================
echo   通用自启动服务 - 安装工具 v1.1
echo ============================================================

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] 请以管理员身份运行此脚本！
    pause
    exit /b 1
)

echo [OK] 管理员权限已获取

:: 查找配置文件
set CONFIG_FILE=%~dp0service_config.json
if not exist "%CONFIG_FILE%" (
    set CONFIG_FILE=%~dp0qwenpaw_service_config.json
)

if not exist "%CONFIG_FILE%" (
    echo [ERROR] 未找到配置文件！
    pause
    exit /b 1
)

:: 安装服务
python "%~dp0universal_service.py" install "%CONFIG_FILE%" --no-check-admin

if %errorLevel% equ 0 (
    echo [OK] 安装完成！服务将在下次开机自动启动
) else (
    echo [ERROR] 安装失败！
)

pause
```

右键点击 `install_windows.bat` → **以管理员身份运行**

### macOS 安装

使用已提供的 `install_macos.sh`：

```bash
sudo ./install_macos.sh
```

## 📋 核心功能

| 功能 | 描述 |
|------|------|
| **跨平台支持** | Windows (sc + schtasks), macOS (launchd) |
| **自动重启** | 服务崩溃时自动重启（可配置最大重启次数） |
| **日志记录** | 实时日志输出，支持文件轮转 |
| **健康检查** | 端口/进程检测，确保服务正常运行 |
| **优雅退出** | 支持 SIGTERM/SIGINT 信号处理 |
| **环境变量** | 支持加载 .env 文件 |

## 🔧 使用方式

### 命令行操作

```bash
# 安装自启动（不立即运行）
python universal_service.py install [config.json] [--no-check-admin]

# 卸载自启动
python universal_service.py uninstall [config.json] [--no-check-admin]

# 手动启动服务
python universal_service.py start [config.json]

# 停止服务
python universal_service.py stop [config.json]

# 查看服务状态
python universal_service.py status [config.json]

# 直接运行（带自启动）
python universal_service.py [config.json]
```

### 双击脚本

- Windows: `install.bat` / `uninstall.bat`
- macOS: `install_macos.sh` / `uninstall_macos.sh`

## ⚙️ 配置文件

### QwenPaw 标准配置 (`qwenpaw_service_config.json`)

```json
{
  "service_name": "QwenPawService",
  "display_name": "QwenPaw 智能助手服务",
  "program": {
    "type": "python",
    "path": "python",
    "arguments": "-m qwenpaw.cli",
    "working_dir": "C:/Users/Administrator/.copaw/workspaces/default"
  },
  "environment": {
    "load_dotenv": true,
    "variables": {}
  },
  "log": {
    "enabled": true,
    "level": "INFO",
    "dir": ".logs",
    "max_size_mb": 10,
    "backup_count": 5,
    "console": true
  },
  "health_check": {
    "enabled": true,
    "type": "port",
    "port": 8765,
    "interval_seconds": 30,
    "timeout_seconds": 5,
    "max_failures": 3
  },
  "restart": {
    "auto_restart": true,
    "max_restarts": 5,
    "restart_delay": 30
  }
}
```

### 通用示例配置 (`service_config.example.json`)

```json
{
  "service_name": "MyCustomService",
  "display_name": "我的自定义服务",
  "program": {
    "type": "python",
    "path": "python3",
    "arguments": "app.py",
    "working_dir": "/path/to/app"
  },
  "environment": {
    "load_dotenv": false,
    "variables": {
      "NODE_ENV": "production"
    }
  },
  "log": {
    "enabled": true,
    "level": "DEBUG",
    "dir": "./logs"
  },
  "health_check": {
    "enabled": true,
    "type": "port",
    "port": 3000,
    "interval_seconds": 10
  },
  "restart": {
    "auto_restart": true,
    "max_restarts": 3,
    "restart_delay": 60
  }
}
```

### 配置选项说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `service_name` | string | 服务内部名称（唯一标识） |
| `display_name` | string | 服务显示名称 |
| `program.type` | string | 程序类型：`python` / `node` / `binary` / `shell` |
| `program.path` | string | 可执行程序路径 |
| `program.arguments` | string | 启动参数 |
| `program.working_dir` | string | 工作目录 |
| `environment.load_dotenv` | bool | 是否加载 .env 文件 |
| `environment.variables` | object | 额外环境变量 |
| `log.enabled` | bool | 是否启用日志 |
| `log.level` | string | 日志级别：DEBUG/INFO/WARNING/ERROR |
| `log.dir` | string | 日志目录 |
| `log.max_size_mb` | int | 单文件最大大小 (MB) |
| `log.backup_count` | int | 保留的备份文件数量 |
| `log.console` | bool | 是否输出到控制台 |
| `health_check.enabled` | bool | 是否启用健康检查 |
| `health_check.type` | string | 检查类型：`port` / `process` |
| `health_check.port` | int | 端口号 |
| `health_check.interval_seconds` | int | 检查间隔 |
| `health_check.timeout_seconds` | int | 超时时间 |
| `health_check.max_failures` | int | 最大失败次数 |
| `restart.auto_restart` | bool | 是否自动重启 |
| `restart.max_restarts` | int | 最大重启次数 |
| `restart.restart_delay` | int | 重启延迟 (秒) |

## 🔍 健康检查

支持两种检查方式：

### 端口检查 (推荐 Web 服务)

```json
{
  "health_check": {
    "enabled": true,
    "type": "port",
    "port": 8765,
    "interval_seconds": 30,
    "timeout_seconds": 5,
    "max_failures": 3
  }
}
```

当连续 3 次无法连接到 8765 端口时，触发自动重启。

### 进程检查

```json
{
  "health_check": {
    "enabled": true,
    "type": "process",
    "interval_seconds": 10
  }
}
```

定期检查子进程是否存活。

## 📝 日志管理

### 默认行为

- 日志文件：`.logs/UniversalService_YYYY-MM-DD.log`
- 日志级别：`INFO`
- 文件轮转：单文件 10MB，保留 5 个备份
- 控制台输出：是

### 禁用日志

```json
{
  "log": {
    "enabled": false
  }
}
```

## 🔄 自动重启机制

### 防死循环设计

```
第 1 次崩溃: 立即重启
第 2 次崩溃: 立即重启
第 3 次崩溃: 等待 5 秒后重启
...
累计 5 次崩溃: 停止重启，记录严重错误
```

可通过配置调整：

```json
{
  "restart": {
    "max_restarts": 5,
    "restart_delay": 30
  }
}
```

## 🛠️ 高级功能

### 环境变量加载

```json
{
  "environment": {
    "load_dotenv": true,
    "variables": {
      "APP_MODE": "production",
      "LOG_LEVEL": "DEBUG"
    }
  }
}
```

会优先使用 `variables` 中的值，覆盖 .env 文件的设置。

### 多程序类型支持

```json
// Python 程序
{
  "program": {
    "type": "python",
    "path": "python3",
    "arguments": "app.py"
  }
}

// Node.js 程序
{
  "program": {
    "type": "node",
    "path": "node",
    "arguments": "server.js"
  }
}

// 可执行文件
{
  "program": {
    "type": "binary",
    "path": "/usr/local/bin/myapp",
    "arguments": "--config config.yaml"
  }
}

// Shell 脚本
{
  "program": {
    "type": "shell",
    "path": "bash",
    "arguments": "scripts/start.sh"
  }
}
```

## 🐛 故障排查

### 问题 1: 权限不足

**Windows:**
```
右键 → 以管理员身份运行
```

**macOS:**
```bash
sudo ./install_macos.sh
```

### 问题 2: 服务未启动

检查日志：
```bash
type .logs\UniversalService_*.log    # Windows
tail -f .logs/UniversalService_*.log  # macOS
```

### 问题 3: 健康检查频繁重启

降低检查频率或增加失败阈值：
```json
{
  "health_check": {
    "interval_seconds": 60,
    "max_failures": 5
  }
}
```

### 问题 4: Python 找不到

指定完整路径：
```json
{
  "program": {
    "path": "C:\\Python39\\python.exe"
  }
}
```

## 📦 文件结构

```
universal-autostart/
├── universal_service.py       # 核心服务管理器
├── install.bat                # Windows 安装脚本
├── uninstall.bat              # Windows 卸载脚本
├── install_macos.sh           # macOS 安装脚本
├── uninstall_macos.sh         # macOS 卸载脚本
├── qwenpaw_service_config.json # QwenPaw 标准配置
├── service_config.example.json # 通用配置示例
└── README.md                  # 用户文档
```

## 🔄 版本历史

### v1.1 (当前版本)
- ✅ 新增 macOS launchd 支持
- ✅ 改进权限检测方法
- ✅ 优化日志轮转机制
- ✅ 增加健康检查功能
- ✅ 修复 admin_check() 子进程问题

### v1.0
- ✅ Windows sc/schtasks 支持
- ✅ 基础自动重启功能
- ✅ 日志记录
- ✅ 环境变量支持

## 📄 许可证

MIT License

---

**项目地址:** https://gitee.com/steam2001/universal-autostart  
**技能商店:** skillhub.club
