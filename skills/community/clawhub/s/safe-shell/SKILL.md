---
name: safe-shell
description: 安全命令行执行器 - 仅允许读取类和查询类命令，阻断所有危险操作。安装命令：npx clawhub@latest install safe-shell
homepage: https://github.com/your-repo/safe-shell
metadata: {"openclaw":{"emoji":"🛡️","description":"只读安全的命令行工具","tags":["security","shell","safe","read-only","monitoring"]}}
---

# Safe Shell

一个极度安全的命令行操作 Skill，支持 macOS/Linux/Windows，仅允许读取和查询类命令。

## 🚀 安装

```bash
npx clawhub@latest install safe-shell
```

## 设计理念

本 Skill 专为以下场景设计：
- **只读监控**：查看文件、系统状态、网络配置
- **零破坏风险**：完全禁止任何修改、删除、执行危险操作
- **AI 防护**：让 AI 可以安全地查询信息，无需担心误操作
- **跨平台**：统一策略适用于 macOS/Linux/Windows

## ✅ 允许的命令（纯读取）

### 📁 文件查看（只读）

| macOS/Linux | Windows (CMD) | Windows (PowerShell) | 说明 |
|-------------|---------------|----------------------|------|
| `ls` | `dir` | `Get-ChildItem` | 列出目录内容 |
| `pwd` | `cd` | `Get-Location` | 显示当前目录 |
| `cat` | `type` | `Get-Content` | 读取文件内容 |
| `head` | - | `Get-Content -Head` | 查看文件头部 |
| `tail` | - | `Get-Content -Tail` | 查看文件尾部 |
| `find` | `where` / `dir /s` | `Get-ChildItem -Recurse` | 查找文件 |
| `which` | `where` | `Get-Command` | 查找命令位置 |
| `stat` | `dir` | `Get-Item` | 文件详情 |

### 🔍 系统状态（只读）

| macOS/Linux | Windows | 说明 |
|-------------|---------|------|
| `ps` | `tasklist` / `Get-Process` | 查看进程 |
| `df` | `wmic logicaldisk get size,freespace,caption` / `Get-PSDrive` | 磁盘使用 |
| `du` | - | 目录大小 |
| `free` | `systeminfo \| findstr /B /C:"Total Physical Memory"` | 内存使用 |
| `uptime` | `systeminfo \| find "System Boot Time"` | 运行时间 |
| `date` | `date /t` / `Get-Date` | 当前时间 |
| `top` | `tasklist /v` / `Get-Process \| Sort-Object CPU -Top 10` | 进程快照 |
| `vmstat` | `systeminfo` | 内存/交换空间 |

### 🌐 网络诊断（只读）

| macOS/Linux | Windows | 说明 |
|-------------|---------|------|
| `ping` | `ping` | 连通性测试 |
| `ifconfig` | `ipconfig` / `ipconfig /all` | 网络配置 |
| `ip addr` | `Get-NetIPAddress` | IP 地址 |
| `netstat` | `netstat -an` | 网络连接状态 |
| `ss` | `Get-NetTCPConnection` | Socket 统计 |
| `traceroute` | `tracert` | 路由追踪 |
| `nslookup` | `nslookup` | DNS 查询 |
| `dig` | `Resolve-DnsName` | DNS 查询 |
| `arp -a` | `arp -a` | ARP 表 |
| `route print` | `route print` | 路由表 |

### 📋 信息查询

| macOS/Linux | Windows | 说明 |
|-------------|---------|------|
| `whoami` | `whoami` / `whoami /all` | 当前用户 |
| `hostname` | `hostname` | 主机名 |
| `uname -a` | `systeminfo \| findstr /B /C:"OS Name" /C:"OS Version"` | 系统信息 |
| `ver` | `ver` | 版本号 |
| `cal` | `Get-Date -Format "MMMM yyyy"` | 日历 |
| `env` / `printenv` | `set` / `Get-ChildItem Env:` | 环境变量 |

### 🔧 硬件/系统信息

| macOS/Linux | Windows | 说明 |
|-------------|---------|------|
| `lspci` | `Get-PnPDevice` | PCI 设备 |
| `lsusb` | `Get-PnpDevice -Class USB` | USB 设备 |
| `system_profiler` | `Get-ComputerInfo` | 详细系统信息 |
| `diskutil list` | `Get-Disk` / `Get-Volume` | 磁盘列表 |

## ❌ 禁止的命令

### 通用危险命令（所有平台）

| 类型 | 示例 | 风险 |
|------|------|------|
| 任何删除 | `rm`, `del`, `erase`, `unlink`, `rmdir` | 数据丢失 |
| 任何修改 | `chmod`, `chown`, `attrib`, `touch` | 配置破坏 |
| 关机重启 | `shutdown`, `reboot`, `halt`, `restart` | 断连 |
| 进程控制 | `kill`, `pkill`, `killall`, `taskkill` | 服务中断 |
| 管道执行 | `curl \| sh`, `wget \| bash`, `\| cmd` | 恶意代码 |
| 提权 | `sudo`, `su`, `runas` | 权限风险 |
| 下载执行 | `curl`, `wget`, `Invoke-WebRequest` | 潜在风险 |
| 远程连接 | `ssh`, `scp`, `sftp`, `rdp` | 安全风险 |
| 任何解释器 | `python`, `node`, `bash`, `sh`, `powershell` | 可执行代码 |
| 包管理 | `brew`, `apt`, `yum`, `npm install`, `pip install`, `choco` | 环境修改 |
| 容器 | `docker`, `podman`, `kubectl` | 容器操作 |
| 虚拟化 | `virsh`, `vboxmanage`, `vmrun` | 虚拟机操作 |

### 🪟 Windows 专用危险命令

| 类型 | 命令 | 风险 |
|------|------|------|
| 磁盘操作 | `format`, `diskpart`, `clean` | 磁盘数据丢失 |
| 注册表 | `reg add`, `reg delete`, `regedit` | 系统破坏 |
| 网络配置 | `netsh advfirewall`, `netsh interface ip` | 网络中断 |
| 启动项 | `bcdedit`, `bcdboot` | 启动破坏 |
| 用户管理 | `net user`, `net localgroup`, `lusrmgr` | 账户风险 |
| 服务控制 | `sc create`, `sc delete`, `net start`, `net stop` | 服务中断 |
| 组策略 | `gpresult`, `gpupdate` | 策略修改 |
| 系统修复 | `sfc`, `dism`, `chkdsk /f` | 系统修改 |
| PowerShell 危险 | `Invoke-Expression`, `Start-Process`, `New-Service` | 代码执行 |

### 🍎 macOS 专用危险命令

| 类型 | 命令 | 风险 |
|------|------|------|
| 磁盘操作 | `diskutil erase`, `dd` | 磁盘数据丢失 |
| SIP | `csrutil` | 系统完整性破坏 |
| 启动安全 | `bless` | 启动修改 |
| 系统偏好 | `defaults write` | 配置修改 |

### 🐧 Linux 专用危险命令

| 类型 | 命令 | 风险 |
|------|------|------|
| 磁盘操作 | `mkfs`, `dd`, `fdisk`, `parted` | 磁盘数据丢失 |
| 系统ctl | `systemctl start`, `systemctl stop`, `systemctl disable` | 服务中断 |
| 用户管理 | `useradd`, `userdel`, `usermod`, `groupadd` | 账户风险 |
| 网络配置 | `iptables`, `ufw`, `nmcli` | 网络中断 |
| 模块 | `modprobe`, `modprobe -r` | 内核模块风险 |

## PowerShell 安全限制

### ✅ 允许的 PowerShell 只读命令

```powershell
# 文件操作
Get-ChildItem, Get-Content, Get-Item, Get-ItemProperty

# 系统信息
Get-ComputerInfo, Get-CimInstance, Get-WmiObject
Get-Process, Get-Service, Get-EventLog
Get-Location, Get-Date, Get-Culture

# 网络
Get-NetIPAddress, Get-NetTCPConnection, Get-NetUDPEndpoint
Get-DnsClientCache, Resolve-DnsName, Test-Connection

# 硬件
Get-Disk, Get-Volume, Get-PSDrive
Get-PnPDevice, Get-Hardware
```

### ❌ 禁止的 PowerShell 操作

```powershell
# 绝对禁止
Invoke-Expression, Invoke-Command, Invoke-WebRequest
Start-Process, Start-Service, Stop-Process, Stop-Service
New-Item, New-Service, New-Object (动态代码)
Remove-Item, Remove-ItemProperty, Remove-Service
Set-Item, Set-ItemProperty, Set-Content
Copy-Item, Move-Item
Set-Service, Set-ExecutionPolicy
Set-NetFirewallRule, New-NetFirewallRule
Add-Type (动态编译)
```

## 核心原则

1. **只读优先**：只允许不影响系统的查询操作
2. **零执行**：禁止任何脚本/代码执行
3. **零修改**：禁止任何文件或系统配置修改
4. **零网络下载**：禁止从网络下载或执行内容
5. **平台感知**：自动识别系统，使用对应安全命令
6. **命令链拦截**：禁止 `| xargs`, `; && ||` 等命令链接

## 使用示例

```
用户：帮我看看当前目录有什么文件
→ macOS/Linux: ls -la
→ Windows: dir

用户：查看系统内存使用
→ macOS/Linux: free -h
→ Windows: systeminfo | findstr "Total Physical"

用户：查看网络配置
→ macOS/Linux: ifconfig
→ Windows: ipconfig /all

用户：安装一个软件
→ 拒绝：禁止执行安装命令

用户：删除这个文件
→ 拒绝：禁止删除操作

用户：帮我运行一个脚本
→ 拒绝：禁止执行任何脚本或解释器

用户：查看Windows服务状态
→ Windows: Get-Service | Select-Object Name,Status
```

## 平台检测与适配

系统自动检测当前平台并应用对应规则：

```python
# 伪代码示例
def get_allowed_commands(platform):
    if platform == "windows":
        return WINDOWS_ALLOWED_COMMANDS
    elif platform == "macos":
        return MACOS_ALLOWED_COMMANDS
    elif platform == "linux":
        return LINUX_ALLOWED_COMMANDS
    else:
        return MINIMAL_ALLOWED_COMMANDS  # 未知系统仅允许最基本查询
```

## 适用场景

- AI 助手安全查询
- 监控系统状态
- 排查网络问题
- 读取日志和配置
- 完全零风险的命令行交互
- 跨平台统一安全策略

---

**版本**: 2.0.0  
**作者**: Cheng Yusheng  
**许可证**: MIT
**更新**: 添加 Windows 支持和 PowerShell 安全限制
