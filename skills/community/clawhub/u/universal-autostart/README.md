# 🚀 Universal AutoStart - 通用自启动服务管理器

<div align="center">

![版本](https://img.shields.io/badge/version-1.1.0-blue)
![平台](https://img.shields.io/badge/platform-Windows%20|%20macOS-green)
![语言](https://img.shields.io/badge/language-Python-yellow)
![许可](https://img.shields.io/badge/license-MIT-orange)

**将任何程序（Python/BAT/EXE/C++/Shell）制作成 Windows/macOS 开机自启动服务的终极工具**

[📖 使用说明](SKILL.md) | [⚡ 快速开始](QUICKSTART.md) | [💬 问题反馈](https://gitee.com/steam2001/universal-autostart/issues)

</div>

---

## 📌 目录

- [核心功能](#-核心功能)
- [效果预览](#-效果预览)
- [快速开始](#-快速开始)
- [详细配置](#-详细配置)
- [使用场景](#-使用场景)
- [命令行参考](#-命令行参考)
- [常见问题](#-常见问题)
- [贡献与反馈](#-贡献与反馈)

---

## 🎯 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| **多程序支持** | Python / BAT / EXE / Shell / C++ 等任意程序 | ✅ |
| **Windows 开机自启** | Windows 任务计划程序，系统级稳定运行 | ✅ |
| **macOS 开机自启** | launchd plist 服务，系统级稳定运行 | ✅ |
| **自动重启** | 程序崩溃后自动恢复，可配置最大重启次数 | ✅ |
| **日志记录** | 完整的运行日志，支持多个级别 | ✅ |
| **灵活配置** | JSON 配置文件，简单易读 | ✅ |
| **一键操作** | 安装/卸载只需双击批处理脚本 | ✅ |

---

## 👀 效果预览

### 💻 使用流程示意

```
┌─────────────────────────────────────────────────────────┐
│                   你的程序 (.py/.bat/.exe)                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│            universal_service.py (核心服务)                │
│  ┌─────────────────────────────────────────────────────┐│
│  │  • 加载 JSON 配置                                     ││
│  │  • 启动目标程序                                       ││
│  │  • 监控运行状态                                       ││
│  │  • 崩溃时自动重启                                     ││
│  │  • 记录详细日志                                       ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│       Windows 任务计划程序 (开机自动触发)                    │
│           ★ 系统级服务 · 无需登录即可运行                  │
└─────────────────────────────────────────────────────────┘
```

### 📊 日志输出示例

```
2026-04-18 10:25:30 [INFO] ============================================================
2026-04-18 10:25:30 [INFO]   CoPaw App 服务启动
2026-04-18 10:25:30 [INFO] ============================================================
2026-04-18 10:25:30 [INFO] 启动命令：python copaw.exe app --host 127.0.0.1 --port 8088
2026-04-18 10:25:30 [INFO] 工作目录：C:\Users\Administrator\.copaw
2026-04-18 10:25:30 [INFO] 程序已启动 (PID: 12345)
```

### 🔧 一键安装界面

```batch
============================================================
  通用自启动服务 - 安装工具
============================================================

[OK] 管理员权限已获取

[步骤] 正在安装服务...
============================================================
  安装开机自启动任务
============================================================
[OK] 开机自启动任务已创建!
任务名称：CoPawAppAutoStart
下次开机将自动启动

============================================================
  安装完成！
============================================================
```

---

## 🚀 快速开始

### 方式一：新手向导 ⭐️ 推荐

#### Step 1: 复制配置模板

```bash
# Windows CMD
copy service_config.example.json my_config.json

# PowerShell
Copy-Item service_config.example.json my_config.json
```

#### Step 2: 编辑配置文件

用记事本或 VS Code 打开 `my_config.json`，修改关键部分：

```json
{
    "service_name": "我的服务",        // 👈 改为你想要的名字
    
    "program": {
        "type": "python",             // 👈 python/bat/exe
        "path": "C:\\完整\\路径\\程序", // 👈 你的程序路径
        "arguments": "--参数",         // 👈 启动参数（可选）
        "working_dir": "C:\\工作目录"  // 👈 程序所在目录
    }
}
```

#### Step 3: 一键安装

**右键点击 `install.bat` → 选择「以管理员身份运行」**

#### Step 4: 验证成功

打开「任务计划程序」→ 找到你设置的服务名 → 状态为「就绪」✅

---

### 方式二：命令行版

适合高级用户和自动化脚本：

```bash
# 查看帮助
python universal_service.py --help

# 安装服务（需管理员权限）
python universal_service.py install my_config.json

# 卸载服务（需管理员权限）
python universal_service.py uninstall my_config.json

# 手动启动（用于测试）
python universal_service.py start my_config.json

# 停止服务
python universal_service.py stop my_config.json

# 查看服务状态
python universal_service.py status my_config.json
```

---

## ⚙️ 详细配置

### 完整配置结构

```json
{
    "service_name": "String",      // 必填：Windows 任务名称
    "display_name": "String",      // 选填：显示名称
    "description": "String",       // 选填：服务描述
    
    "program": {
        "type": "String",          // 程序类型：python/bat/exe
        "path": "String",          // 必填：程序完整路径
        "arguments": "String",     // 选填：启动参数
        "working_dir": "String"    // 选填：工作目录
    },
    
    "log": {
        "enabled": Boolean,        // 是否启用日志
        "dir": "String",           // 日志目录路径
        "level": "String"          // 日志级别
    },
    
    "restart": {
        "auto_restart": Boolean,   // 崩溃自动重启
        "max_restarts": Number,    // 最大重启次数
        "restart_delay": Number    // 重启延迟（秒）
    }
}
```

### 配置详解

#### 1️⃣ 基本信息

```json
{
    "service_name": "MyPythonApp",      // Windows 任务计划程序中显示的名称
                                        // 建议用英文，避免特殊字符
                                        
    "display_name": "我的 Python 应用",   // 日志和界面中显示的友好名称
    
    "description": "这是应用的描述信息"   // 可选，用于备注
}
```

#### 2️⃣ 程序配置

```json
{
    "program": {
        "type": "python",              // 程序类型
                                       // 可选值：python / bat / exe
        
        "path": "C:\\Program Files\\Python311\\python.exe",  
                                       // 程序的绝对路径（必填！）
        
        "arguments": "app.py --host 0.0.0.0 --port 8088", 
                                       // 启动参数（可选）
        
        "working_dir": "C:\\Projects\\MyApp"
                                       // 工作目录（可选）
    }
}
```

#### 3️⃣ 日志配置

```json
{
    "log": {
        "enabled": true,               // 启用日志记录
        
        "dir": "C:\\Logs\\MyApp",      // 日志存放目录
                                       // 不存在会自动创建
        
        "level": "INFO"                // 日志级别
                                       // DEBUG(最详细)/INFO/WARNING/ERROR(最少)
    }
}
```

#### 4️⃣ 自动重启配置

```json
{
    "restart": {
        "auto_restart": true,          // 程序崩溃时自动重启
        
        "max_restarts": 5,             // 最大重启尝试次数
                                       // 防止无限重启循环
        
        "restart_delay": 30            // 重启等待时间（秒）
                                       // 给程序一些冷静的时间 😄
    }
}
```

---

## 📋 使用场景

### 场景 1: Python Web 应用自启动 🐍

```json
{
    "service_name": "FlaskWebApp",
    "display_name": "Flask Web 应用",
    
    "program": {
        "type": "python",
        "path": "C:\\Python\\Python311\\python.exe",
        "arguments": "app.py --prod",
        "working_dir": "C:\\Projects\\WebApp"
    },
    
    "log": {
        "enabled": true,
        "dir": "C:\\Logs\\WebApp",
        "level": "INFO"
    },
    
    "restart": {
        "auto_restart": true,
        "max_restarts": 3,
        "restart_delay": 60
    }
}
```

### 场景 2: 定时备份脚本自启动 🔄

```json
{
    "service_name": "DailyBackup",
    "display_name": "每日自动备份",
    
    "program": {
        "type": "bat",
        "path": "C:\\Scripts\\backup_daily.bat",
        "working_dir": "C:\\Scripts"
    },
    
    "log": {
        "enabled": true,
        "dir": "C:\\Logs",
        "level": "INFO"
    }
}
```

### 场景 3: C++ 桌面应用自启动 💻

```json
{
    "service_name": "MyDesktopTool",
    "display_name": "桌面小工具",
    
    "program": {
        "type": "exe",
        "path": "C:\\Program Files\\MyTools\\app.exe",
        "arguments": "--silent --no-window",
        "working_dir": "C:\\Program Files\\MyTools"
    }
}
```

### 场景 4: QwenPaw App 自启动 ⚡

本项目已预置配置，直接使用：

```bash
python universal_service.py install qwenpaw_service_config.json
```

或者编辑 `qwenpaw_service_config.json` 后：

```json
{
    "service_name": "QwenPawAppAutoStart",
    "display_name": "QwenPaw App",
    
    "program": {
        "type": "python",
        "path": "C:\\Python\\Python313\\Scripts\\qwenpaw.exe",
        "arguments": "app --host 127.0.0.1 --port 8088",
        "working_dir": "C:\\Users\\Administrator\\.qwenpaw"
    },
    
    "log": {
        "enabled": true,
        "dir": "C:\\Users\\Administrator\\.qwenpaw\\logs",
        "level": "INFO"
    },
    
    "restart": {
        "auto_restart": true,
        "max_restarts": 5,
        "restart_delay": 30
    }
}
```

### 场景 5: macOS 服务自启动 🍎

macOS 使用 launchd 管理开机启动，配置方式类似：

```json
{
    "service_name": "MyMacService",
    "display_name": "我的 Mac 服务",
    
    "program": {
        "type": "python",
        "path": "/usr/bin/python3",
        "arguments": "app.py --prod",
        "working_dir": "/Users/username/Projects/MyApp"
    },
    
    "log": {
        "enabled": true,
        "dir": "~/Library/Logs/MyApp",
        "level": "INFO"
    },
    
    "restart": {
        "auto_restart": true,
        "max_restarts": 3,
        "restart_delay": 60
    }
}
```

安装命令（需管理员权限）：

```bash
sudo python universal_service.py install my_config.json
```

### 场景 5: Node.js 应用自启动 🟨

```json
{
    "service_name": "NodeServer",
    "display_name": "Node.js 服务器",
    
    "program": {
        "type": "python",  // 使用 node.exe 同样适用
        "path": "C:\\Program Files\\nodejs\\node.exe",
        "arguments": "server.js",
        "working_dir": "C:\\Projects\\NodeApp"
    }
}
```

---

## 🛠️ 命令行参考

```
========================================
  通用自启动服务管理器
========================================

用法:
    python universal_service.py install     - 安装开机自启动
    python universal_service.py uninstall   - 卸载开机自启动
    python universal_service.py start       - 手动启动服务
    python universal_service.py stop        - 停止服务
    python universal_service.py status      - 查看服务状态
    python universal_service.py [config]    - 直接运行（不注册自启动）

选项:
    --help, -h                              - 显示帮助信息

示例:
    # 使用默认配置文件安装
    python universal_service.py install

    # 使用指定配置文件安装
    python universal_service.py install my_custom_config.json

    # 仅手动启动（不安装自启动）
    python universal_service.py start test_config.json

    # 检查服务状态
    python universal_service.py status MyService
```

---

## ❓ 常见问题

### Q1: 需要管理员权限吗？

**A:** 
- ✅ **安装/卸载** - 需要管理员权限
- ✅ **手动启动/停止** - 不需要
- ❌ **日常使用** - 不需要，服务会后台运行

---

### Q2: 如何查看运行日志？

**A:** 根据配置的日志目录查看：

```bash
# 默认在配置文件中指定的目录
C:\你的\日志\目录\service_20260418.log

# 或用 findstr 搜索
findstr "ERROR" *.log
```

---

### Q3: 开机没有自动启动怎么办？

**A:** 按以下顺序排查：

```
1. 打开「任务计划程序」
2. 找到对应的任务
3. 确认状态是否为「就绪」
4. 右键 → 「运行」测试是否正常
5. 检查「历史记录」查看错误信息
```

---

### Q4: 程序启动后立即退出？

**A:** 可能的原因：

```
• 程序本身有错误 → 查看日志文件定位问题
• 缺少依赖 → 确保所有依赖已安装
• 端口占用 → 更换端口号
• 工作目录错误 → 检查 working_dir 配置
• 环境变量缺失 → 任务计划程序不会加载全部环境变量
```

---

### Q5: 如何让多个程序同时自启动？

**A:** 每个程序单独创建一个配置和服务：

```bash
# 为每个程序创建独立的配置文件
python_app_config.json
web_server_config.json
backup_tool_config.json

# 分别安装
python universal_service.py install python_app_config.json
python universal_service.py install web_server_config.json
python universal_service.py install backup_tool_config.json
```

---

### Q6: 卸载后服务还在运行怎么办？

**A:** 

```bash
# 方法 1: 停止并卸载
python universal_service.py stop my_config.json
python universal_service.py uninstall my_config.json

# 方法 2: 手动清理
# 1. 打开任务计划程序
# 2. 找到并删除对应的任务
```

---

## 🔗 相关资源

- [📖 详细说明文档](SKILL.md)
- [⚡ 5 分钟快速开始](QUICKSTART.md)
- [📝 更新日志](CHANGELOG.md)
- [🐛 问题反馈](https://gitee.com/steam2001/universal-autostart/issues)

---

## 🤝 贡献与反馈

欢迎任何形式的贡献！

### 报告问题
如果遇到 bug 或有改进建议，请创建 Issue：
https://gitee.com/steam2001/universal-autostart/issues

### 提交代码
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源许可

本项目采用 **MIT License** - 自由使用、修改、分发。

详见 [LICENSE](LICENSE) 文件。

---

## ⭐️ Star 趋势

如果这个项目对你有帮助，请点个 ⭐️ Star 支持一下！

<div align="center">

[![Gitee Stars](https://img.shields.io/gitee/stars/steam2001/universal-autostart?style=social)](https://gitee.com/steam2001/universal-autostart)

**感谢每一位使用和支持的朋友！** ❤️

</div>

---

<div align="center">

 made with ❤ by steam2001（斯帝姆智能科技）| [Gitee](https://gitee.com/steam2001/universal-autostart) | v1.1.0

**支持 Windows 10/11 + macOS** 🚀

</div>