---
name: OpenClaw Install Guide (WSL2 Windows)
slug: openclaw-install-wsl-windows
version: 1.1.0
homepage:
description: "Complete step-by-step installation guide for OpenClaw on Windows 10/11 with WSL2, includes common pitfalls and solutions from real installation experience."
metadata: {"workbuddy":{"emoji":"🚀","os":["windows"]}}
---

<!--
# OpenClaw Windows (WSL2) 安装指南
# OpenClaw Installation Guide for Windows 10/11 (WSL2)

This installation guide is designed to be used by OpenClaw-like software tools to assist users in installing OpenClaw on Windows WSL2 environment.
本安装指南是供类 OpenClaw 的第三方软件工具调用，辅助用户在 Windows WSL2 环境下安装 OpenClaw。

This guide shares pitfalls and solutions collected from actual installation experience by the author and community contributors.
本指南分享了作者和社区在实际安装过程中遇到的各种坑和解决方法。

**Author** / **作者**: Deepwhite 深白色
**Contributor** / **贡献者**: workfisher
**License**: MIT
-->

## When to Use

Use this guide when you need to install OpenClaw on a Windows 10/11 machine via WSL2.
当你需要在 Windows 10/11 的 WSL2 环境中安装 OpenClaw 时，请使用本指南。

This guide includes: / 本指南包含：
- One-click installation to system C: drive / 一键安装到系统盘 C 盘
- Custom installation to non-system drives (D/E/F) / 自定义安装到非系统盘
- Comprehensive troubleshooting from real-world experience / 来自实际安装经验的完整排错指南
- Optimizations for Chinese network environment / 针对国内网络环境的优化

## Prerequisites / 前置要求

### Hardware / Software Requirements / 硬件/软件要求
- **OS**: Windows 10 version 2004+ (build 19041+) / Windows 11 all versions
  - 系统要求：Windows 10 需要 2004 版本以上，内部版本号≥19041；Windows 11 任意版本都符合
- **Hardware**: CPU supports virtualization (VT-x/AMD-V), RAM ≥ 8GB, ≥ 20GB free disk space
  - 硬件要求：CPU 需要支持虚拟化技术，内存至少 8GB，磁盘剩余空间至少 20GB
- **Network**: Access to GitHub or Chinese mirror sources available
  - 网络要求：能够访问 GitHub 或配置了国内镜像源

### Mandatory Pre-flight Check / 安装前必做环境检查（能规避 90% 的安装失败）

**1.1 Check Windows System Version / 检查 Windows 系统版本**
1. Press `Win + R`, type `winver`, press Enter
   - 按下 `Win + R`，输入 `winver`，回车
2. Verify version: / 核对版本：
   - Windows 10: version 2004+, build number ≥ 19041
   - Windows 11: any version is OK
3. If version is too old: Go to **Settings → Windows Update → Check for updates**, upgrade to latest stable version before continuing
   - 如果版本不达标：打开「设置 → Windows 更新 → 检查更新」，升级到最新稳定版再继续

> ⚠️ **Important Lesson from Pitfalls / 重要踩坑经验**:
> If Windows 10 version is too old, it will lack `lxcore.sys` and `lxss.sys` kernel drivers, WSL will never start properly. **You must upgrade system to latest version**.
> 如果 Windows 10 版本太老，会缺少 `lxcore.sys` 和 `lxss.sys` 内核驱动，WSL 始终无法启动，必须升级系统到最新版本。

**1.2 Verify CPU Virtualization is Enabled / 确认 CPU 虚拟化已开启**
1. Press `Ctrl + Shift + Esc` to open Task Manager
   - 按 `Ctrl + Shift + Esc` 打开任务管理器
2. Go to **Performance** tab → click **CPU**
   - 切换到「性能」选项卡，点击「CPU」
3. Check "Virtualization: Enabled" in bottom-right corner
   - 在右下角查看「虚拟化：已启用」
4. If not enabled: Reboot → enter BIOS → enable CPU virtualization. Google "your computer model enable virtualization" for tutorial.
   - 如果未启用：重启电脑进 BIOS 开启 CPU 虚拟化，搜索「你的电脑型号 开启虚拟化」获取教程

**1.3 Prepare Terminal with Admin Privileges / 准备管理员权限终端**
All following operations **must** be run as administrator: / 后续所有操作必须以管理员身份运行终端：
1. Press `Win + X`
   - 按 `Win + X`
2. Select **Windows Terminal (Admin)** (on Windows 10, select **Windows PowerShell (Admin)**)
   - 选择「Windows 终端（管理员）」（Windows 10 选择「Windows PowerShell（管理员）」）
3. Accept UAC prompt, you are now in admin terminal
   - 同意 UAC 提示，进入管理员终端

---

## Chapter 2: Beginner Friendly - One-click Install WSL2 to System C: Drive / 第二章：新手零门槛 - 一键安装 WSL2 到系统盘 C 盘

**Use Case / 适用场景**: C: drive has ≥ 20GB free space, want fastest installation. 4 steps total, 5 minutes to complete.
C 盘剩余空间 ≥ 20GB，想最快速度完成安装，选择这个方案。全程仅需 4 步，5 分钟完成。

**2.1 Run One-click Install Command / 执行一键安装命令**
```powershell
wsl --install
```

This is official Microsoft one-click install, it automatically does: / 这是微软官方一键安装，会自动完成：
- ✅ Enables Windows Subsystem for Linux core feature / 启用「适用于 Linux 的 Windows 子系统」核心组件
- ✅ Enables Virtual Machine Platform feature / 启用「虚拟机平台」虚拟化组件
- ✅ Downloads and installs latest WSL2 Linux kernel / 下载并安装 WSL2 最新 Linux 内核
- ✅ Downloads and installs default Ubuntu Linux distribution / 下载并安装默认的 Ubuntu Linux 发行版
- ✅ Automatically sets WSL2 as default version / 自动设置 WSL2 为默认版本

Wait for initialization to complete, follow prompt to create UNIX user account: / 等待初始化完成后，按提示创建 UNIX 用户账户：
```bash
# 1. Enter custom username (lowercase ASCII only, no spaces/Chinese, recommend "openclaw")
# 输入自定义用户名（纯英文小写，无空格/中文，推荐 openclaw）
Enter new UNIX username: openclaw

# 2. Enter custom password (no echo on screen, this is normal, remember it!)
# 输入自定义密码（输入时无字符回显，正常输入，务必牢记！）
New password:

# 3. Confirm password by entering again
# 再次输入密码确认
Retype new password:
```

**2.2 Reboot to Activate Components / 重启电脑使组件生效**

After command completes, **you must reboot** or system components won't take effect.
命令执行完成后，**必须重启电脑**，否则系统组件不会生效。

**2.3 Verify Installation Success / 验证安装是否成功**
```powershell
wsl --list --verbose
```

**Success Criteria (all must be true) / 成功标准（必须同时满足）**:
- STATE shows Running / STATE 列显示 Running
- VERSION column shows **2** (must be 2, can't be 1) / VERSION 列显示 2（必须为 2，不可为 1）
- Distribution name shows Ubuntu / 发行版名称显示 Ubuntu

**2.4 System Update & Mirror Configuration / 系统更新与软件源配置**

Run inside WSL: / 进入 WSL 后执行：
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y curl wget git
```

**For users in China: Recommended to replace with Aliyun mirror for faster speed / 国内用户推荐替换阿里云镜像源加速**:
```bash
sudo sed -i 's|http://archive.ubuntu.com/ubuntu|https://mirrors.aliyun.com/ubuntu|g' /etc/apt/sources.list
sudo sed -i 's|http://security.ubuntu.com/ubuntu|https://mirrors.aliyun.com/ubuntu|g' /etc/apt/sources.list
sudo apt update && sudo apt upgrade -y
```

After completing, skip to Chapter 4. / 完成后跳转到第四章继续。

---

## Chapter 3: Custom Install WSL2 to Non-System Drive (D/E/F) / 第三章：自定义盘符安装 WSL2（非系统盘 D/E/F 盘）

**Use Case / 适用场景**: C: drive doesn't have enough space, want to install WSL on another drive. 10 steps, ~15 minutes.
C 盘空间不足，想把 WSL 安装到其他盘。全程 10 步，15 分钟完成。

**Key Note / 核心说明**: Official Microsoft `wsl --install` doesn't support custom install path directly. We use official standard method: "install core → export distro → import to target drive", which is safe.
微软官方 `wsl --install` 没有直接指定安装路径的参数，因此采用「装核心组件 → 导出发行版 → 导入到目标盘」的官方标准方案，安全无风险。

**3.1 Install WSL Core Components (mandatory) / 安装 WSL 核心组件（必须先做）**

Run these commands one-by-one in admin terminal: / 在管理员终端中依次执行：
```powershell
# Enable WSL core feature / 启用 WSL 核心组件
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform feature / 启用虚拟机平台组件
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# !! PITFALL WARNING !! System built-in wsl.exe is too old, need manual install latest version
# 这里有坑：系统自带 wsl.exe 版本太旧，需要手动安装最新版
# Download from: https://github.com/microsoft/WSL/releases/latest
# After install, add new WSL to PATH with higher priority:
# $oldPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
# [System.Environment]::SetEnvironmentVariable("Path", "C:\Program Files\WSL;" + $oldPath, "Machine")

# Enable all Hyper-V core components (mandatory, otherwise WSL won't start)
# 启用所有 Hyper-V 核心组件（必须，否则 WSL 无法启动）
Enable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform -All -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Hypervisor -All -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Services -All -NoRestart
bcdedit /set hypervisorlaunchtype auto

# Set WSL2 as default version / 设置 WSL2 为默认版本
wsl --set-default-version 2
```

After execution, **you must reboot** for components to activate. / 执行完成后，**必须重启电脑**，使组件生效。

> ⚠️ **Common Pitfall / 常见坑**: If `wsl --set-default-version 2` only prints help text and doesn't execute, that means built-in wsl.exe is too old. **You must manually download and install latest WSL MSI package**.
> 如果 `wsl --set-default-version 2` 只打印帮助文档不执行，说明系统自带的 wsl.exe 太旧，必须手动下载安装最新版 WSL MSI 包。

**3.2 Install Ubuntu Distro to Temporary Location / 安装 Ubuntu 发行版到临时目录**

After reboot, open admin terminal again, install Ubuntu 22.04 LTS (stable): / 重启后再次打开管理员终端，安装 Ubuntu 22.04 LTS 稳定版：
```powershell
wsl --install -d Ubuntu-22.04
```

**3.3 Terminate Distro to Prevent Auto-Initialization / 终止发行版，避免自动初始化**

After installation, **DO NOT open Ubuntu app** (it will auto-initialize on C: drive), just run: / 安装完成后，**绝对不要打开 Ubuntu 应用**（否则会自动初始化占用 C 盘），直接执行：
```powershell
wsl --terminate Ubuntu-22.04
```

**3.4 Create Install Directory on Target Drive / 在目标盘创建安装目录**

Open File Explorer, on target drive (e.g. D:), create: / 打开文件资源管理器，在目标盘（如 D 盘）创建：
- Temp export dir: `D:\WSL\backup` / 导出文件临时目录：`D:\WSL\backup`
- Final install dir: `D:\WSL\Ubuntu2204` / 最终安装目录：`D:\WSL\Ubuntu2204`

> ❗ **Critical Pitfall Avoidance / 关键避坑**:
> Directory path **MUST NOT contain Chinese characters, spaces, or special characters**, otherwise import will fail.
> 目录路径**绝对不要有中文、空格、特殊字符**，否则会导致导入失败。

**3.5 Export Distro to Temp File / 导出发行版到临时文件**
```powershell
# Format: wsl --export <distro-name> <full-export-path>
# 命令格式：wsl --export 发行版名称 导出文件完整路径
wsl --export Ubuntu-22.04 D:\WSL\backup\ubuntu2204.tar
```

Wait for export to complete, takes 1-3 minutes depending on disk speed. No error means success. / 等待导出完成，根据磁盘速度约 1-3 分钟，无报错即为成功。

**3.6 Unregister Default Distro on C: / 注销 C 盘的默认发行版**
```powershell
# Format: wsl --unregister <distro-name>
# 命令格式：wsl --unregister 发行版名称
wsl --unregister Ubuntu-22.04
```

After execution, the C: drive distro files are completely removed. / 执行后，C 盘的发行版文件会被完全删除。

**3.7 Import Distro to Target Drive / 导入发行版到目标盘**
```powershell
# Format: wsl --import <custom-distro-name> <target-install-dir> <exported-tar-path> --version 2
# 命令格式：wsl --import 自定义发行版名称 目标安装目录 导出 tar 文件路径 --version 2
wsl --import Ubuntu-22.04 D:\WSL\Ubuntu2204 D:\WSL\backup\ubuntu2204.tar --version 2
```

**Parameter Explanation / 参数说明**:
- `Ubuntu-22.04`: Custom distro name, use this name to boot later / 自定义的发行版名称，后续启动用这个名字
- `D:\WSL\Ubuntu2204`: Target install directory, all WSL files stored here / 目标安装目录，WSL 所有文件都会存放在这里
- `--version 2`: Force use WSL2 version **this is mandatory** / 强制使用 WSL2 版本，必须添加

**3.8 Set Default Login User (CRITICAL!) / 设置默认登录用户（关键！）**

After import, default login is root. You can choose: / 导入完成后默认会以 root 身份登录，你有两种选择：

### Option 1: Create normal user (recommended, follows Linux best practice) / 方案一：创建普通用户登录（推荐，符合 Linux 最佳实践）

First enter the imported Ubuntu system: / 先进入导入的 Ubuntu 系统：
```powershell
wsl -d Ubuntu-22.04
```

Run these commands in order (replace `openclaw` with your username): / 进入系统后依次执行（替换 `openclaw` 为你的用户名）：
```bash
# 1. Create user, auto-create home dir, set default shell to bash
# 创建用户，自动创建家目录，设置默认 shell 为 bash
useradd -m -s /bin/bash openclaw

# 2. Set password for user (no echo on screen, normal behavior, remember it!)
# 给用户设置密码（输入时无回显，务必牢记）
passwd openclaw

# 3. Add user to sudo group for admin privileges
# 给用户赋予 sudo 管理员权限
usermod -aG sudo openclaw

# 4. Configure WSL default login to be the newly created user
# 配置 WSL 默认登录用户为刚创建的用户
echo -e "[user]\ndefault = openclaw" >> /etc/wsl.conf

# 5. (Recommended) Configure passwordless sudo to avoid repeated typing during install
# 配置 sudo 免密（推荐，避免安装过程频繁输入密码）
echo "openclaw ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
```

After complete, type `exit` to leave WSL, back to Windows terminal. / 执行完成后，输入 `exit` 退出 WSL，回到 Windows 终端。

**3.9 Restart WSL to Activate Configuration / 重启 WSL 使配置生效**
```powershell
# Terminate distro / 终止发行版
wsl --terminate Ubuntu-22.04

# Re-enter system, verify default user / 重新进入系统，验证默认用户
wsl -d Ubuntu-22.04
```

**Success Criteria / 成功标准**: After entering system, prompt shows your created username (e.g. `openclaw@...`), NOT `root`. / 进入系统后，命令行前缀显示你创建的用户名（如 `openclaw@...`），而非 `root`。

### Option 2: Use root directly (simpler, for experienced users) / 方案二：直接使用 root（更简单，适合经验丰富的用户）

If you prefer simplicity and don't want to create a separate user, you can just keep using root. No extra configuration needed.
如果你喜欢简单，不想创建单独用户，可以直接一直用 root 登录，**不需要任何额外配置**。

**Main differences / 主要区别**:
- ✅ Pros: No need to create user, no sudo password required for every command / 优点：不用创建用户，每个命令都不需要输 sudo 密码
- ⚠️ Notes: Runs everything with full root permissions, less secure than normal user / 注意：所有程序都以完整 root 权限运行，安全性不如普通用户

Both options work fine for installing and running OpenClaw. / 两种方式都能正常安装和运行 OpenClaw，按个人习惯选择即可。

**3.10 Verify Install Path & Version / 验证安装路径与版本**
```powershell
wsl --list --verbose
```

**Success Criteria / 成功标准**:
- STATE column shows Running / STATE 列显示 Running
- VERSION column shows 2 / VERSION 列显示 2
- LOCATION column shows your target drive path / LOCATION 列显示你设置的目标盘路径

---

## Chapter 4: OpenClaw Specific Environment Optimization / 第四章：OpenClaw 专属环境优化配置

**4.1 Configure .wslconfig (Optimize Network & Memory) / 配置 .wslconfig（优化网络和内存）**

Mirror networking mode needs global configuration: / 镜像网络模式需要全局配置：

1. Open File Explorer, navigate to: `C:\Users\<your-username>\` / 打开文件资源管理器，导航到：`C:\Users\<你的用户名>\`
2. Create file named `.wslconfig` (note the leading dot) / 创建名为 `.wslconfig` 的文件（注意前面的点号）
3. Open with Notepad, add the following configuration: / 用记事本打开，添加以下配置：

```ini
[wsl2]
# Enable mirrored networking mode - THIS IS THE MOST IMPORTANT CONFIG
# 启用镜像网络模式 - 这是最重要的配置
networkingMode=mirrored
# Enable DNS tunneling, prevents DNS resolution failure under VPN
# 启用 DNS 隧道，防止 VPN 环境下域名解析失效
dnsTunneling=true
# Force WSL to use Windows HTTP proxy settings
# 强制 WSL 使用 Windows 的 HTTP 代理设置
autoProxy=true
# Enable integrated firewall support
# 启用集成防火墙支持
firewall=true

[experimental]
# Gradually auto-reclaim unused memory, improves performance
# 自动回收闲置内存，优化性能
autoMemoryReclaim=gradual
# Enable host loopback access support
# 支持主机回环地址访问
hostAddressLoopback=true
```

4. Save file, run in Windows terminal: / 保存文件，在 Windows 终端执行：
```powershell
wsl --shutdown
```

5. Wait ~8 seconds to ensure VM is fully shut down, then restart Ubuntu. / 等待约 8 秒钟确保虚拟机彻底关闭，然后重新启动 Ubuntu。

**4.2 Configure Windows Firewall Rule / 配置 Windows 防火墙规则**

In mirrored networking mode, need to allow OpenClaw port access: / 镜像网络模式下，需要允许 OpenClaw 端口访问：
```powershell
New-NetFirewallRule -DisplayName "OpenClaw-Service" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 18789
```

> ⚠️ **Note / 说明**: Windows 10 doesn't support mirrored networking mode, it will automatically fall back to NAT mode. This doesn't affect normal OpenClaw usage.
> Windows 10 不支持镜像网络模式，会自动回退到 NAT 模式，不影响 OpenClaw 正常使用。

**4.3 Install OpenClaw / 安装 OpenClaw**

Run after entering WSL: / 进入 WSL 后执行：
```bash
curl -fsSL https://molt.bot/install.sh | bash
```

**4.4 Fix PATH Environment Variable / 修复 PATH 环境变量**

If after installation it says `openclaw` command not found, that means npm global bin directory isn't in PATH: / 如果安装完成后提示 `openclaw` 命令找不到，说明 npm 全局 bin 目录没有加入 PATH：
```bash
echo 'export PATH="/home/openclaw/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify: / 验证：
```bash
which openclaw
openclaw --version
```

**4.5 Run Initialization Wizard / 运行初始化向导**
```bash
openclaw setup
```

Follow the wizard prompts to complete configuration. / 按照向导提示完成配置即可。

---

## Chapter 5: LLM Model Configuration / 第五章：LLM 模型配置

After installing OpenClaw, you need to configure your own LLM API key in the setup wizard. You can choose any LLM provider that fits your needs. Common options include:
安装完成后，你需要在安装向导中配置自己的 LLM API 密钥。你可以根据需求选择任意 LLM 服务商，常见选项包括：

- **GLM (Zhipu)** - Free for new users, easy to configure / 新用户可以免费使用，设置方便
- **SiliconFlow (硅基流动)** - Free tier for beginners, many models available / 新手可以免费使用很多模型
- **Volcano Engine (ByteDance)** / **Doubao** - Stable coding model service, affordable pricing / 火山引擎方舟，稳定的代码模型服务，价格实惠

---

## Chapter 6: Startup & Verification / 第六章：启动与验证

**Start OpenClaw / 启动 OpenClaw**:
```powershell
# 1. From Windows PowerShell
wsl -d Ubuntu
```
```bash
# 2. Inside WSL
openclaw gateway start
```

**Verify Installation / 验证安装**:
```bash
which openclaw
openclaw --version
openclaw gateway status
```

---

## Chapter 7: Troubleshooting - Pitfalls & Solutions (Collected from Community Experience) / 第七章：常见问题排查（作者 + 社区踩坑经验汇总）

This section collects troubleshooting experience from **Deepwhite 深白色**, **workfisher**, and other community contributors who installed OpenClaw on Windows WSL2.
本节收集了作者 Deepwhite 深白色、workfisher 以及社区其他人在 Windows WSL2 安装 OpenClaw 实际遇到的各种报错和解决方法。

---

### Pitfall 1: System built-in wsl.exe is too old / 坑 1：系统自带 wsl.exe 版本太旧
- **Symptom / 现象**: `wsl --update`, `wsl --set-default-version 2` only prints help text, doesn't execute / `wsl --update`、`wsl --set-default-version 2` 只打印帮助文档不执行
- **Cause / 原因**: Windows 10 built-in wsl.exe is very old, doesn't support modern parameters / Windows 10 内置的 wsl.exe 版本很老，不支持现代参数
- **Solution / 解决**: Manually download latest WSL MSI package from GitHub and install, add to PATH / 手动从 GitHub 下载最新 WSL MSI 包安装，然后加入 PATH  
  Download: https://github.com/microsoft/WSL/releases/latest

---

### Pitfall 2: GitHub connection fails / 坑 2：GitHub 直连失败
- **Symptom / 现象**: "Connection closed unexpectedly" error when downloading from GitHub / 下载 GitHub 文件报错"连接意外终止"
- **Cause / 原因**: Network connectivity to GitHub is unstable in China / 国内网络访问 GitHub 不稳定
- **Solution / 解决**: Use ghproxy.com mirror to download, e.g.: / 使用 ghproxy.com 镜像下载，例如：
  ```bash
  curl -fSL https://ghproxy.com/https://github.com/microsoft/WSL/releases/download/2.3.26/wsl.2.3.26.0.x64.msi -o wsl-install.msi
  ```

---

### Pitfall 3: Hyper-V components not enabled / 坑 3：Hyper-V 组件未启用
- **Symptom / 现象**: `wsl --status` constantly reports `WSL_E_WSL_OPTIONAL_COMPONENT_REQUIRED` / `wsl --status` 持续报 `WSL_E_WSL_OPTIONAL_COMPONENT_REQUIRED`
- **Cause / 原因**: Core components like `Microsoft-Hyper-V-Hypervisor` are not enabled by default / `Microsoft-Hyper-V-Hypervisor` 等核心组件默认未开启
- **Solution / 解决**: Enable all required Hyper-V components one-by-one with `Enable-WindowsOptionalFeature` / 逐一用 `Enable-WindowsOptionalFeature` 启用所有 Hyper-V 组件（详见第三章）

---

### Pitfall 4: WSL kernel driver files missing / 坑 4：WSL 内核驱动文件缺失
- **Symptom / 现象**: All components show as Enabled, but WSL still can't start / 所有组件都 Enabled，但 WSL 始终无法启动
- **Cause / 原因**: `lxcore.sys` and `lxss.sys` kernel drivers are missing / `lxcore.sys` 和 `lxss.sys` 两个关键内核驱动不存在
- **Solution / 解决**: **Upgrade Windows 10 to latest cumulative update**, drivers will be installed automatically / **升级 Windows 10 到最新累积更新**，驱动会自动到位

---

### Pitfall 5: Mirrored networking mode not supported / 坑 5：镜像网络模式不支持
- **Symptom / 现象**: Entering WSL prompts "mirrored networking mode not supported" / 进入 WSL 提示"不支持镜像网络模式"
- **Cause / 原因**: Mirrored networking is Windows 11 exclusive feature, not available on Windows 10 / 镜像网络模式是 Windows 11 专属功能，Windows 10 不支持
- **Impact / 影响**: Automatically falls back to NAT mode, doesn't affect normal OpenClaw usage / 自动回退到 NAT 模式，不影响 OpenClaw 正常使用

---

### Pitfall 6: apt download speed extremely slow / 坑 6：apt 下载速度极慢
- **Symptom / 现象**: `apt update` speed under 20KB/s / `apt update` 速度 20KB/s 以下
- **Cause / 原因**: Default connects to overseas Ubuntu official servers / 默认连接境外 Ubuntu 官方源
- **Solution / 解决**: Replace with Aliyun China mirror (commands in Chapter 4) / 替换为阿里云国内镜像源（本文第四章有命令）

---

### Pitfall 7: PATH not configured / 坑 7：PATH 未配置
- **Symptom / 现象**: After installing OpenClaw, prompts `PATH missing npm global bin dir` / 安装完 OpenClaw 后提示 `PATH missing npm global bin dir`
- **Cause / 原因**: npm global install path `/home/openclaw/.npm-global/bin` not added to PATH / npm 全局安装路径 `/home/openclaw/.npm-global/bin` 未加入 PATH
- **Solution / 解决**: Fix commands in Chapter 4 / 本文第四章有修复命令

---

### Pitfall 8: Gateway startup error, requires systemd / 坑 8：Gateway 启动报错，需要 systemd
- **Symptom / 现象**: Startup error says systemd is required / 启动 gateway 报错说需要 systemd
- **Solution / 解决**:
```bash
sudo tee /etc/wsl.conf << 'EOF'
[boot]
systemd=true
EOF
```
Then run in Windows PowerShell: / 然后在 Windows PowerShell 执行：
```powershell
wsl --shutdown
```
Restart WSL then start OpenClaw again / 重启 WSL 后再启动 OpenClaw。

---

### Pitfall 9: Gateway service disabled / 坑 9：Gateway service disabled
- **Symptom / 现象**: After startup prompts `Gateway service disabled` / 启动后提示 `Gateway service disabled`
- **Solution / 解决**:
```bash
openclaw gateway install
systemctl --user start openclaw-gateway.service
```
Then check status: / 然后检查状态：
```bash
openclaw gateway status
```

---

### Pitfall 10: WSL installation fails with 0x80070005 error / 坑 10：WSL 安装失败，报错 0x80070005
- **Symptom / 现象**: `wsl --install` fails with error code 0x80070005 / `wsl --install` 失败，错误代码 0x80070005
- **Cause / 原因**: Permission issue, antivirus software blocking / 权限问题，杀毒软件拦截
- **Solution / 解决**:
  1. Temporarily disable third-party antivirus / 暂时关闭第三方杀毒软件
  2. Run installer as administrator / 以管理员身份运行安装程序
  3. If still fails, try manual download and install Ubuntu from Microsoft Store / 如果还是失败，尝试从微软应用商店手动下载安装 Ubuntu

---

### Pitfall 11: WSL2 fails to start with 0x80370114 error / 坑 11：WSL2 无法启动，报错 0x80370114
- **Symptom / 现象**: WSL immediately closes after opening, error 0x80370114 / WSL 打开后立即关闭，报错 0x80370114
- **Cause / 原因**: Corrupted WSL installation or third-party security software blocking / WSL 安装损坏，或者第三方安全软件拦截
- **Solution / 解决**:
  1. Disable Core Isolation in Windows Defender: Windows Security → Device Security → Core Isolation → Memory Integrity → Off / 在 Windows Defender 中关闭内核隔离：Windows 安全中心 → 设备安全性 → 内核隔离 → 内存完整性 → 关闭
  2. Reboot and try again / 重启后重试
  3. If that doesn't work, uninstall WSL completely and reinstall / 如果不行，彻底卸载 WSL 重新安装

---

### Pitfall 12: Error: "The requested operation could not be completed due to a virtual disk system limitation" / 坑 12：报错 "由于虚拟磁盘系统限制，无法完成请求的操作"
- **Symptom / 现象**: When importing WSL distro, error about virtual disk size limit / 导入 WSL 发行版时，报虚拟磁盘大小限制错误
- **Cause / 原因**: Target drive is FAT32 format, which doesn't support files larger than 4GB / 目标盘是 FAT32 格式，不支持大于 4GB 的文件
- **Solution / 解决**: Convert drive to NTFS format, or choose another NTFS drive / 将目标盘转换为 NTFS 格式，或者选择另一个 NTFS 格式的磁盘

---

### Pitfall 13: "Function not processed" error when enabling Hyper-V / 坑 13：启用 Hyper-V 时报"该功能无法处理"
- **Symptom / 现象**: `Enable-WindowsOptionalFeature` fails with error / `Enable-WindowsOptionalFeature` 执行失败
- **Cause / 原因**: Windows is Home edition, Hyper-V is not supported on Home edition / 你的 Windows 是家庭版，家庭版不支持 Hyper-V
- **Solution / 解决**:
  - Method 1: Upgrade Windows 10/11 from Home to Pro edition / 方案一：将 Windows 10/11 从家庭版升级到专业版
  - Method 2: Enable WSL without Hyper-V using third-party scripts (not officially supported, use at your own risk) / 方案二：使用第三方脚本在不开启 Hyper-V 的情况下启用 WSL（非官方支持，风险自负）

---

### Pitfall 14: After Windows update, WSL disappears / 坑 14：Windows 更新后，WSL 消失了
- **Symptom / 现象**: `wsl --list --verbose` shows no distributions / `wsl --list --verbose` 显示没有发行版
- **Cause / 原因**: Windows update sometimes resets WSL registration / Windows 更新有时候会重置 WSL 注册
- **Solution / 解决**: If you still have the rootfs tarball, re-import the distro. If not, you need to reinstall. / 如果你还有 rootfs 压缩包，重新导入即可。如果没有，需要重新安装。

---

### Pitfall 15: npm install fails with EACCES permission denied / 坑 15：npm install 遇到 EACCES 权限错误
- **Symptom / 现象**: npm global install fails with permission denied / npm 全局安装遇到权限拒绝错误
- **Cause / 原因**: Wrong permissions on npm global directory / npm 全局目录权限不正确
- **Solution / 解决**:
```bash
# Change ownership of npm directory to current user
sudo chown -R $USER:$USER ~/.npm-global
```
Then re-run install / 然后重新运行安装命令。

---

### Pitfall 16: WSL clock drift, time wrong / 坑 16：WSL 时钟漂移，时间不对
- **Symptom / 现象**: SSL certificate error because system time is wrong / 因为系统时间不对导致 SSL 证书错误
- **Solution / 解决**:
```powershell
# Run in Windows PowerShell
wsl --shutdown
```
Restart WSL, time will sync automatically / 关闭 WSL 再重新启动，时间会自动同步。

---

### Pitfall 17: "The operation could not be started because the swap file could not be created" / 坑 17："因为无法创建交换文件，所以无法启动操作"
- **Symptom / 现象**: WSL fails to start after import, error creating swap file / 导入后 WSL 无法启动，创建交换文件失败
- **Cause / 原因**: Windows disk is full, or permissions issue on Windows temporary directory / Windows 磁盘满了，或者 Windows 临时目录权限问题
- **Solution / 解决**:
  1. Free up disk space on Windows system drive / 释放 Windows 系统盘磁盘空间
  2. Clear Windows temp folder / 清理 Windows 临时文件夹
  3. Disable swap in .wslconfig if problem persists: / 如果问题仍然存在，可以在 .wslconfig 中禁用 swap：
     ```ini
     [wsl2]
     swap=0
     ```

---

### Issue 1: `wsl --install` error: need to update kernel / 问题 1：执行 `wsl --install` 报错，提示需要更新内核
- **Solution / 解决**: Manually download and install official Microsoft WSL2 kernel update package: https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package. After install, rerun command. / 手动下载安装微软官方 WSL2 内核更新包，安装后重新执行命令。

### Issue 2: `wsl --list --verbose` shows VERSION is 1, not 2 / 问题 2：`wsl --list --verbose` 显示 VERSION 是 1，不是 2
- **Solution / 解决**:
  1. Verify CPU virtualization is enabled / 确认 CPU 虚拟化已开启
  2. Run `wsl --set-default-version 2` / 执行 `wsl --set-default-version 2`
  3. Run `wsl --set-version <your-distro-name> 2`, wait for conversion to complete / 执行 `wsl --set-version <你的发行版名称> 2`，等待转换完成

### Issue 3: Forgot Ubuntu user password / 问题 3：忘记 Ubuntu 用户密码
- **Solution / 解决**:
  1. Run `wsl -d <distro-name> -u root` in Windows terminal to login as root / 在 Windows 终端执行 `wsl -d <发行版名称> -u root`，以 root 身份进入系统
  2. Run `passwd <your-username>` to reset password / 执行 `passwd <你的用户名>`，重新设置密码
  3. Run `exit` and login with new password / 执行 `exit` 退出，用新密码登录即可

### Issue 4: Mirrored mode not working, IP still starts with 172 / 问题 4：镜像模式不生效，IP 还是 172 开头
- **Solution / 解决**:
  1. Verify `.wslconfig` is in correct user directory, filename correct (must be `.wslconfig`, not `wslconfig.txt`) / 确认 `.wslconfig` 文件放在正确的用户目录下，文件名正确（必须是 `.wslconfig`，不是 `wslconfig.txt`）
  2. Run `wsl --shutdown` to fully close WSL, wait 10 seconds then restart / 执行 `wsl --shutdown` 完全关闭 WSL，等待 10 秒后再启动
  3. Run `wsl --update` to update WSL to latest version / 执行 `wsl --update` 更新 WSL 到最新版本

### Issue 5: Import distro error: invalid path / 问题 5：导入发行版报错，提示路径无效
- **Solution / 解决**: Check target path for Chinese characters, spaces, special characters. Change to pure ASCII path like `D:\WSL\Ubuntu2204`, do NOT use paths with spaces/Chinese. / 检查目标路径是否有中文、空格、特殊字符，换成纯英文路径，比如 `D:\WSL\Ubuntu2204`，不要使用带空格/中文的路径。

### Issue 6: Can't access OpenClaw web UI from Windows / 问题 6：从 Windows 无法访问 OpenClaw Web UI
- **Symptom / 现象**: In WSL OpenClaw is running, but `http://localhost:18789` doesn't load from browser / 在 WSL 中 OpenClaw 在运行，但浏览器访问 `http://localhost:18789` 打不开
- **Solution / 解决**:
  1. For mirrored networking mode: Check Windows firewall, allow port 18789 / 镜像网络模式：检查 Windows 防火墙，允许 18789 端口访问
  2. For NAT mode: Get WSL IP with `hostname -I` inside WSL, then access `http://<wsl-ip>:18789` / NAT 模式：在 WSL 内用 `hostname -I` 获取 IP，然后访问 `http://<wsl-ip>:18789`

---

## Chapter 8: Browser Extension / 第八章：浏览器扩展

Install Chrome extension for quick access: / 安装 Chrome 扩展方便快捷连接：  
https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp

---

## Chapter 9: Feishu Integration (Optional) / 第九章：飞书集成（可选）

If you need Feishu integration, create app in Feishu Developer Portal and configure required permissions: / 如果你需要飞书集成，在飞书开发后台创建应用，并配置好相应权限：
https://open.feishu.cn/?lang=zh-CN

After configuration, run inside WSL: / 配置完成后，在 WSL 中执行：
```bash
openclaw pairing approve feishu <your-code>
```

---

## Chapter 10: Daily Usage / 第十章：日常使用

**Start OpenClaw / 启动 OpenClaw**:
```powershell
# From Windows PowerShell
wsl -d Ubuntu
```
```bash
# Inside WSL
openclaw gateway start
```

**Shutdown WSL / 关闭 WSL**:
```powershell
wsl --shutdown
```

---

## Author & Credits / 作者与致谢

- **Author / 作者**: Deepwhite 深白色
- **Contributor / 贡献者**: workfisher
- **Acknowledgements / 致谢**: This guide collects troubleshooting experience from many community members who installed OpenClaw on WSL2. Thank you to everyone who shared their pitfalls and solutions.

This guide is a complete step-by-step installation experience summary based on actual installation of OpenClaw on Windows WSL2, collected and organized by the author and workfisher. We hope it helps more people successfully install OpenClaw on Windows.

