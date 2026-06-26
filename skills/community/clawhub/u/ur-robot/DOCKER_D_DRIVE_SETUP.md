# Docker Desktop D 盘配置指南

**目的:** 将 Docker 数据和镜像存储迁移到 D 盘，节省 C 盘空间

---

## 📋 方案总览

| 项目 | 默认位置 | 迁移后位置 |
|------|----------|------------|
| Docker 镜像 | C: | D:\Docker\images |
| Docker 容器 | C: | D:\Docker\containers |
| URSim 镜像 (1-2GB) | C: | D:\Docker\images |
| Docker 数据卷 | C: | D:\Docker\volumes |

**预计节省:** 5-10GB+ (取决于镜像数量)

---

## 🔧 配置步骤

### 方式 1: 通过 Docker Desktop 设置 (推荐)

#### 1. 打开 Docker Desktop 设置

1. 右键点击任务栏 Docker 图标
2. 选择 **"Settings"** 或 **"Preferences"**

#### 2. 配置存储位置

**Windows WSL2 后端:**

1. 进入 **Settings → Resources → WSL Integration**
2. 找到 **"Choose where your data is stored"**
3. 选择 **D:\Docker\wsl**

**Windows Hyper-V 后端:**

1. 进入 **Settings → Advanced**
2. 找到 **"Disk image location"**
3. 修改为 **D:\Docker\docker-data**

#### 3. 应用并重启

1. 点击 **"Apply & Restart"**
2. 等待 Docker 重启完成

---

### 方式 2: 手动迁移现有数据

#### 1. 停止 Docker 服务

```powershell
# 以管理员身份运行 PowerShell
Stop-Service com.docker.service -Force
```

#### 2. 迁移 Docker 数据

```powershell
# 创建 D 盘目录
New-Item -ItemType Directory -Path "D:\Docker" -Force

# 停止 Docker Desktop
taskkill /F /IM "Docker Desktop.exe"

# 复制现有数据
Copy-Item -Path "$env:LOCALAPPDATA\Docker" -Destination "D:\Docker" -Recurse -Force
```

#### 3. 创建符号链接

```powershell
# 备份原目录
Move-Item -Path "$env:LOCALAPPDATA\Docker" -Destination "$env:LOCALAPPDATA\Docker.backup" -Force

# 创建符号链接
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\Docker" -Target "D:\Docker" -Force
```

#### 4. 重启 Docker

```powershell
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

---

### 方式 3: 配置 daemon.json (高级)

#### 1. 编辑 Docker 配置文件

**文件位置:**
```
C:\ProgramData\Docker\config\daemon.json
```

#### 2. 添加存储配置

```json
{
  "data-root": "D:\\Docker\\data",
  "exec-opts": ["native.cgroupdriver=windows"]
}
```

#### 3. 重启 Docker 服务

```powershell
Restart-Service docker
```

---

## 🐳 URSim 镜像存储配置

### 拉取镜像到 D 盘

Docker 配置完成后，所有镜像会自动存储到 D 盘：

```bash
# 拉取 URSim 镜像
docker pull universalrobots/ursim_e-series

# 验证镜像位置
docker images
```

**镜像大小:** 约 1-2GB

---

### 使用数据卷 (可选)

如果需要持久化 URSim 数据：

```bash
# 创建 D 盘数据卷目录
New-Item -ItemType Directory -Path "D:\Docker\volumes\ursim" -Force

# 启动时挂载
docker run --rm -it ^
  -p 8080:8080 ^
  -p 30001-30004:30001-30004 ^
  -v D:\Docker\volumes\ursim:/data ^
  --name ursim ^
  universalrobots/ursim_e-series
```

---

## 📊 验证配置

### 1. 检查 Docker 信息

```bash
docker info | findstr "Docker Root"
```

**期望输出:**
```
Docker Root Dir: D:\Docker\data
```

### 2. 检查镜像位置

```bash
docker images
```

**验证:** 镜像应该显示在列表中

### 3. 检查磁盘空间

```powershell
# 检查 C 盘
Get-PSDrive C | Select-Object Name, Used, Free

# 检查 D 盘
Get-PSDrive D | Select-Object Name, Used, Free
```

---

## ⚠️ 常见问题

### 问题 1: Docker 无法启动

**错误:** `Cannot connect to the Docker daemon`

**解决:**
```powershell
# 以管理员身份运行
Restart-Service docker
```

### 问题 2: 符号链接创建失败

**错误:** `Access is denied`

**解决:**
- 以管理员身份运行 PowerShell
- 启用开发者模式

### 问题 3: WSL2 数据迁移

**步骤:**
```bash
# 导出 WSL2 Docker 数据
wsl --export docker-desktop D:\Docker\docker-desktop.tar

# 导入到新位置
wsl --import docker-desktop D:\Docker\wsl D:\Docker\docker-desktop.tar
```

---

## 🎯 快速配置脚本

**保存为 `setup-docker-d-drive.ps1`:**

```powershell
# 以管理员身份运行此脚本

Write-Host "=== Docker D 盘配置脚本 ===" -ForegroundColor Green

# 1. 停止 Docker
Write-Host "`n[1/5] 停止 Docker..." -ForegroundColor Yellow
taskkill /F /IM "Docker Desktop.exe"
Stop-Service com.docker.service -Force -ErrorAction SilentlyContinue

# 2. 创建目录
Write-Host "`n[2/5] 创建 D 盘目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "D:\Docker\wsl" -Force
New-Item -ItemType Directory -Path "D:\Docker\data" -Force
New-Item -ItemType Directory -Path "D:\Docker\volumes" -Force

# 3. 迁移数据 (如果存在)
Write-Host "`n[3/5] 迁移现有数据..." -ForegroundColor Yellow
if (Test-Path "$env:LOCALAPPDATA\Docker") {
    Copy-Item -Path "$env:LOCALAPPDATA\Docker" -Destination "D:\Docker" -Recurse -Force
    Move-Item -Path "$env:LOCALAPPDATA\Docker" -Destination "$env:LOCALAPPDATA\Docker.backup" -Force
    New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\Docker" -Target "D:\Docker" -Force
    Write-Host "数据已迁移并创建符号链接" -ForegroundColor Green
} else {
    Write-Host "无现有数据，跳过迁移" -ForegroundColor Gray
}

# 4. 配置 daemon.json
Write-Host "`n[4/5] 配置 daemon.json..." -ForegroundColor Yellow
$daemonPath = "C:\ProgramData\Docker\config\daemon.json"
$daemonConfig = @{
    "data-root" = "D:\Docker\data"
} | ConvertTo-Json

if (-not (Test-Path (Split-Path $daemonPath))) {
    New-Item -ItemType Directory -Path (Split-Path $daemonPath) -Force
}
$daemonConfig | Out-File -FilePath $daemonPath -Encoding UTF8
Write-Host "daemon.json 已配置" -ForegroundColor Green

# 5. 启动 Docker
Write-Host "`n[5/5] 启动 Docker..." -ForegroundColor Yellow
Start-Service com.docker.service -ErrorAction SilentlyContinue
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

Write-Host "`n=== 配置完成！===" -ForegroundColor Green
Write-Host "请等待 Docker Desktop 完全启动后继续" -ForegroundColor Cyan
```

**运行方式:**
```powershell
# 右键 → 使用 PowerShell 运行
.\setup-docker-d-drive.ps1
```

---

## 📈 预期效果

### 配置前
```
C 盘已用：50GB
D 盘已用：100GB
```

### 配置后
```
C 盘已用：45GB (节省 5GB+)
D 盘已用：105GB
```

**URSim 镜像:** 1-2GB 直接存储到 D 盘

---

## 🎯 下一步

配置完成后，继续 URSim 测试：

```bash
# 1. 验证 Docker
docker ps

# 2. 拉取 URSim 镜像 (存储到 D 盘)
docker pull universalrobots/ursim_e-series

# 3. 启动仿真器
docker run --rm -it -p 8080:8080 -p 30001-30004:30001-30004 universalrobots/ursim_e-series

# 4. 运行测试
python test_ur_real.py
```

---

**配置完成后告诉我，我们继续 URSim 测试！** 🚀
