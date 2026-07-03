# Remote Copy - 远程文件复制 Skill

## 概述
通过 SSH/SCP 从远程电脑（Windows/Mac/Linux）复制文件到本地 Mac。
支持任意两台电脑之间的文件传输，自动处理路径格式、SSH 诊断、中文编码。

## 触发词
- "从XX电脑复制资料"
- "远程拷贝"
- "scp 传输"
- "从XX IP 拉文件"
- "remote copy"
- "复制远程文件"
- "从服务器下载文件"

---

## 使用方式

### 基础用法
```
从 192.168.6.81 复制 F:\公司资料\一冶大模型\资料
```

### 完整参数
```
从 vip@192.168.6.81 复制 F:\公司资料 到 ~/公司资料/
```

### Linux 示例
```
从 root@192.168.1.100 复制 /home/user/dataset 到 ~/data/
```

### Mac 示例
```
从 192.168.1.50 复制 /Users/john/Documents/project 到 ~/project/
```

---

## 执行流程

### Step 1: 解析参数
从用户输入中提取：

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| remote_ip | ✅ | - | 远程 IP 地址 |
| remote_path | ✅ | - | 远程路径（支持 Windows/Mac/Linux 格式） |
| remote_user | ❌ | 询问或 `vip` | 远程用户名 |
| local_dest | ❌ | `~/远程资料/{ip}/` | 本地目标路径 |

### Step 2: 路径格式自动转换
根据路径格式自动判断远程系统类型：

| 路径格式 | 系统 | SCP 路径转换 |
|----------|------|-------------|
| `F:\公司资料` 或 `C:/xxx` | Windows | `/f/公司资料` |
| `/Users/xxx` | macOS | 直接使用 |
| `/home/xxx` 或 `/root/xxx` | Linux | 直接使用 |

**Windows 路径转换规则：**
- `F:\xxx` → `/f/xxx`
- `D:\` → `/d/`
- 反斜杠 `\` → 正斜杠 `/`
- 驱动器号小写并加 `/` 前缀

### Step 3: SSH 连接测试
```bash
ssh -o ConnectTimeout=5 -o BatchMode=yes {user}@{ip} "echo ok" 2>&1
```

### Step 4a: 连接成功 → 执行复制

#### 方案 A: scp（简单场景）
```bash
mkdir -p {local_dest}
scp -r -o StrictHostKeyChecking=no {user}@{ip}:"{converted_path}" {local_dest}
```

#### 方案 B: tar 管道（推荐，解决中文路径问题）
```bash
mkdir -p {local_dest}
ssh -o StrictHostKeyChecking=no {user}@{ip} 'chcp 65001 >nul && cd /d "{remote_path}" && tar cf - .' | tar xf - -C {local_dest}
```

> Windows 中文路径必须用 tar 管道方式，scp 会因 GBK 编码乱码失败

### Step 4b: 连接失败 → 诊断 + 修复方案

自动检测失败原因并给出对应系统的修复命令：

---

## SSH 开启指南（按系统）

### Windows（需手动开启 OpenSSH）

**检查是否已安装：**
```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

**安装 OpenSSH 服务器：**
```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

**启动服务：**
```powershell
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
```

**放通防火墙：**
```powershell
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

**验证：**
```powershell
Get-Service sshd          # 应显示 Running
netstat -an | findstr :22  # 应显示 LISTENING
```

---

### macOS（默认已开启）

**开启远程登录：**
```bash
# 图形界面：系统设置 → 通用 → 共享 → 远程登录 → 打开

# 命令行：
sudo systemsetup -setremotelogin on
```

**验证：**
```bash
ssh localhost  # 应能连接
```

---

### Linux

**Ubuntu/Debian：**
```bash
sudo apt update && sudo apt install openssh-server -y
sudo systemctl start sshd
sudo systemctl enable sshd
```

**CentOS/RHEL/Rocky：**
```bash
sudo yum install openssh-server -y
sudo systemctl start sshd
sudo systemctl enable sshd
```

**放通防火墙：**
```bash
# Ubuntu (ufw)
sudo ufw allow 22/tcp

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

**验证：**
```bash
sudo systemctl status sshd  # 应显示 active (running)
```

---

## 前置条件清单

| 条件 | Windows | macOS | Linux |
|------|---------|-------|-------|
| SSH 服务 | ❌ 需手动安装 | ✅ 默认有 | ❌ 需安装 |
| 防火墙放通 22 | ❌ 需手动 | ✅ 自动 | ❌ 需手动 |
| 用户名 | 登录账号 | 登录账号 | 登录账号 |
| 密码/密钥 | 需要 | 需要 | 需要 |

---

## 高级功能

### 密码认证（首次连接）
当密钥认证失败时，使用 sshpass：
```bash
sshpass -p "{password}" scp -r -o StrictHostKeyChecking=no {user}@{ip}:"{path}" {local_dest}
```

> 密码仅在当前会话使用，不会被保存

### 免密配置（推荐）
首次连接后配置密钥免密：
```bash
# 生成密钥（如果没有）
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

# 复制公钥到远程
ssh-copy-id -i ~/.ssh/id_ed25519.pub {user}@{ip}
```

### 大文件传输（>1GB）
自动切换 rsync（支持断点续传）：
```bash
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" {user}@{ip}:"{path}" {local_dest}
```

### 批量传输
支持多路径：
```
从 192.168.6.81 复制 F:\资料1 和 F:\资料2
```

---

## 传输完成
- 显示复制的文件数量和总大小
- 显示本地存储路径
- 可选：在 Finder 中打开目录

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Connection closed | SSH 服务未开启 | 按上方指南开启 |
| Permission denied | 密码错误或用户不存在 | 检查 whoami 和密码 |
| 中文乱码 | Windows GBK 编码 | 使用 tar 管道 + chcp 65001 |
| No such file | 路径格式错误 | 检查 Windows 路径转换 |
| Host key verification failed | 首次连接未信任 | 加 -o StrictHostKeyChecking=no |
| Connection timed out | 防火墙阻断 | 放通 22 端口 |

---

## 实战案例

### 从 Windows 复制
```
用户: 从 192.168.6.81 复制 F:\公司资料\一冶大模型\资料
助手:
1. 检测到 Windows 路径，转换为 /f/公司资料/一冶大模型/资料
2. 测试 SSH 连接...
3. 连接成功，使用 tar 管道传输（解决中文路径问题）
4. 完成！共复制 109 个文件，保存在 ~/远程资料/192.168.6.81/
```

### 从 Linux 复制
```
用户: 从 root@192.168.1.100 复制 /home/user/dataset
助手:
1. 检测到 Linux 路径
2. 测试 SSH 连接...
3. 连接成功，使用 scp 传输
4. 完成！共复制 256 个文件，保存在 ~/远程资料/192.168.1.100/
```

### 从 Mac 复制
```
用户: 从 192.168.1.50 复制 /Users/john/Projects/app
助手:
1. 检测到 macOS 路径
2. 测试 SSH 连接...
3. 连接成功，使用 scp 传输
4. 完成！保存在 ~/远程资料/192.168.1.50/
```

---

## 版本信息
- 版本：1.0.0
- 作者：龙虾 (Lobster)
- 更新日期：2026-06-17
- 平台：macOS (OpenClaw)
- 依赖：sshpass (brew install sshpass)
