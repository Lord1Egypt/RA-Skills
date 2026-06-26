# OneDrive 记忆同步配置指南

## 📦 方案架构

```
🏠 家里电脑（主记忆库）    ☁️ OneDrive    🏢 公司电脑（工作记忆）
     ↓                         ↓                ↓
  写入记忆                  云端存储          读取记忆
  完整权限                  实时同步          只读权限
```

## 🛠️ 配置步骤

### 第 1 步：设置 OneDrive

1. **启动 OneDrive**
   - 点击任务栏 OneDrive 图标（云朵☁️）
   - 登录微软账号
   - 选择同步文件夹：`C:\Users\Xiabi\OneDrive`

2. **创建工作区文件夹**
   ```
   C:\Users\Xiabi\OneDrive\OpenClaw-Workspace\
   ```

### 第 2 步：家里电脑配置（主记忆库）

**工作区位置：**
```
C:\Users\Xiabi\.openclaw\workspace\  ← 保持原位
```

**同步脚本（手动/自动）：**
```powershell
# sync-to-onedrive.ps1
$source = "C:\Users\Xiabi\.openclaw\workspace"
$dest = "C:\Users\Xiabi\OneDrive\OpenClaw-Workspace"

# 同步记忆文件
Copy-Item "$source\MEMORY.md" -Destination "$dest\" -Force
Copy-Item "$source\memory\" -Destination "$dest\" -Recurse -Force
Copy-Item "$source\USER.md" -Destination "$dest\" -Force
Copy-Item "$source\TOOLS.md" -Destination "$dest\" -Force

Write-Host "✅ 记忆已同步到 OneDrive"
```

**定时同步（可选）：**
```powershell
# 每小时同步一次
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-ExecutionPolicy Bypass -File C:\Users\Xiabi\.openclaw\workspace\sync-to-onedrive.ps1"
$trigger = New-ScheduledTaskTrigger -Hourly -At 0 minutes
Register-ScheduledTask -TaskName "OpenClaw Memory Sync" `
    -Action $action -Trigger $trigger -RunLevel Highest
```

### 第 3 步：公司电脑配置（工作记忆）

**1. 安装 OpenClaw**
```bash
npm install -g openclaw
```

**2. 从 OneDrive 获取记忆**
```powershell
$source = "C:\Users\Xiabi\OneDrive\OpenClaw-Workspace"
$dest = "C:\Users\Xiabi\.openclaw\workspace"

# 复制记忆文件
Copy-Item "$source\MEMORY.md" -Destination "$dest\" -Force
Copy-Item "$source\memory\" -Destination "$dest\" -Recurse -Force
Copy-Item "$source\USER.md" -Destination "$dest\" -Force
Copy-Item "$source\TOOLS.md" -Destination "$dest\" -Force
```

**3. 配置只读模式（可选）**
```json
// openclaw.json
{
  "memory": {
    "readOnly": true  // 只读，不写入
  }
}
```

### 第 4 步：同步策略

**同步内容：**
- ✅ `MEMORY.md` - 长期记忆
- ✅ `memory/*.md` - 每日记忆
- ✅ `USER.md` - 用户信息
- ✅ `TOOLS.md` - 工具配置
- ❌ `openclaw.json` - 配置（敏感信息）
- ❌ `*.log` - 日志文件

**同步方向：**
- 家里 → OneDrive：完整同步（写入）
- OneDrive → 公司：只读同步（读取）

**同步频率：**
- 家里电脑：每小时同步一次
- 公司电脑：启动时同步，每小时拉取一次

## ⚠️ 注意事项

### 1. 冲突处理

**问题：** 两只小龙虾同时写 MEMORY.md

**解决方案：**
- 方案 A：公司电脑只读，只有家里电脑写入
- 方案 B：用不同文件名（MEMORY-home.md / MEMORY-work.md）
- 方案 C：手动合并冲突

### 2. 敏感信息保护

**不要同步：**
- `openclaw.json` - 包含 API Key
- `.env` 文件 - 环境变量
- 任何包含密码的文件

**建议：**
```bash
# 在 OneDrive 文件夹创建 .gitignore
openclaw.json
*.log
.env
```

### 3. 网络问题

**离线场景：**
- OneDrive 支持离线编辑
- 联网后自动同步
- 可能有版本冲突

**解决：**
- 重要修改后手动触发同步
- 定期检查 OneDrive 同步状态

## 🔄 自动化脚本

### 家里电脑：推送到 OneDrive

```powershell
# sync-push.ps1
param(
    [switch]$Auto  # 自动模式，无输出
)

$source = "C:\Users\Xiabi\.openclaw\workspace"
$dest = "C:\Users\Xiabi\OneDrive\OpenClaw-Workspace"

# 确保目标文件夹存在
if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest -Force
}

# 同步记忆文件
Copy-Item "$source\MEMORY.md" -Destination "$dest\" -Force -ErrorAction SilentlyContinue
Copy-Item "$source\memory\" -Destination "$dest\" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$source\USER.md" -Destination "$dest\" -Force -ErrorAction SilentlyContinue
Copy-Item "$source\TOOLS.md" -Destination "$dest\" -Force -ErrorAction SilentlyContinue

if (-not $Auto) {
    Write-Host "✅ 记忆已推送到 OneDrive" -ForegroundColor Green
    Write-Host "📍 位置：$dest" -ForegroundColor Cyan
}
```

### 公司电脑：从 OneDrive 拉取

```powershell
# sync-pull.ps1
param(
    [switch]$Auto  # 自动模式，无输出
)

$source = "C:\Users\Xiabi\OneDrive\OpenClaw-Workspace"
$dest = "C:\Users\Xiabi\.openclaw\workspace"

# 检查 OneDrive 是否存在
if (-not (Test-Path $source)) {
    Write-Host "❌ OneDrive 文件夹不存在：$source" -ForegroundColor Red
    exit 1
}

# 确保目标文件夹存在
if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest -Force
}

# 同步记忆文件（只读模式）
Copy-Item "$source\MEMORY.md" -Destination "$dest\" -Force -ErrorAction SilentlyContinue
Copy-Item "$source\memory\" -Destination "$dest\" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$source\USER.md" -Destination "$dest\" -Force -ErrorAction SilentlyContinue
Copy-Item "$source\TOOLS.md" -Destination "$dest\" -Force -ErrorAction SilentlyContinue

if (-not $Auto) {
    Write-Host "✅ 记忆已从 OneDrive 拉取" -ForegroundColor Green
    Write-Host "📍 来源：$source" -ForegroundColor Cyan
}
```

## 📊 同步状态检查

```powershell
# check-sync.ps1
Write-Host "📊 记忆同步状态检查`n" -ForegroundColor Cyan

$home = "C:\Users\Xiabi\.openclaw\workspace"
$onedrive = "C:\Users\Xiabi\OneDrive\OpenClaw-Workspace"

Write-Host "家里电脑工作区：$home"
if (Test-Path $home) {
    Write-Host "  ✅ 存在" -ForegroundColor Green
    Write-Host "  📄 MEMORY.md: $((Get-Item "$home\MEMORY.md" -ErrorAction SilentlyContinue).LastWriteTime)"
} else {
    Write-Host "  ❌ 不存在" -ForegroundColor Red
}

Write-Host "`n OneDrive 工作区：$onedrive"
if (Test-Path $onedrive) {
    Write-Host "  ✅ 存在" -ForegroundColor Green
    Write-Host "  📄 MEMORY.md: $((Get-Item "$onedrive\MEMORY.md" -ErrorAction SilentlyContinue).LastWriteTime)"
} else {
    Write-Host "  ❌ 不存在" -ForegroundColor Red
}

Write-Host "`n OneDrive 同步状态："
$onedriveExe = "$env:LOCALAPPDATA\Microsoft\OneDrive\OneDrive.exe"
if (Test-Path $onedriveExe) {
    $process = Get-Process OneDrive -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "  ✅ OneDrive 运行中" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ OneDrive 未运行" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ OneDrive 未安装" -ForegroundColor Red
}
```

## 🎯 推荐配置

### 家里电脑（主记忆库）
- **工作区位置**：`C:\Users\Xiabi\.openclaw\workspace`
- **OneDrive 同步**：每小时推送一次
- **写入权限**：完整（可读写）
- **任务**：创业、个人、长期记忆

### 公司电脑（工作记忆）
- **工作区位置**：`C:\Users\Xiabi\.openclaw\workspace`
- **OneDrive 同步**：启动时拉取 + 每小时拉取
- **写入权限**：只读（或写入独立文件）
- **任务**：周报、会议、工作相关

## 💡 高级技巧

### 1. 工作记忆隔离

如果不想工作记忆污染个人记忆：

```
OneDrive/
├── OpenClaw-Workspace/      # 个人记忆（同步）
│   ├── MEMORY.md
│   └── memory/
└── OpenClaw-Work/           # 工作记忆（不同步）
    └── MEMORY-work.md
```

### 2. 冲突检测

```powershell
# 检查是否有冲突文件
$conflicts = Get-ChildItem "C:\Users\Xiabi\OneDrive" -Recurse -Filter "*冲突*"
if ($conflicts) {
    Write-Host "⚠️ 发现冲突文件：" -ForegroundColor Yellow
    $conflicts | ForEach-Object { Write-Host "  - $($_.Name)" }
}
```

### 3. 手动同步快捷键

创建桌面快捷方式：
- 推送到 OneDrive：`PowerShell.exe -ExecutionPolicy Bypass -File "sync-push.ps1"`
- 从 OneDrive 拉取：`PowerShell.exe -ExecutionPolicy Bypass -File "sync-pull.ps1"`

---

**最后更新**: 2026-03-05  
**版本**: 1.0
