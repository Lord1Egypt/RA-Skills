# QClaw Restart Skill

重启 QClaw 应用程序。

> ⚠️ **仅限 Windows 系统使用**

## 使用场景

- 用户要求重启 QClaw
- 用户说"重启一下"、"重启你自己"
- 配置修改后需要重启生效

## 重要规则

**重启前必须先询问用户确认！**

不要直接执行重启，先询问：
> "确定要重启 QClaw 吗？重启后配置变更将生效。"

等待用户确认后再执行。

## 重启脚本

脚本路径: `<workspace>/restart-qclaw.ps1`（workspace 为 OpenClaw 工作目录）

**如果脚本不存在，根据下方脚本内容自动创建。**

执行命令:
```powershell
powershell -ExecutionPolicy Bypass -File "<workspace>\restart-qclaw.ps1"
```

## 脚本内容

```powershell
# QClaw 重启脚本 - 仅限 Windows 系统

# 检查操作系统
if ($env:OS -ne "Windows_NT") {
    Write-Host "ERROR: This script only supports Windows."
    exit 1
}

# 从当前运行的 QClaw 进程获取路径
$proc = Get-Process -Name "QClaw" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $proc -or -not $proc.Path) {
    Write-Host "ERROR: QClaw is not running."
    exit 1
}

$qclawExe = $proc.Path
Write-Host "QClaw path: $qclawExe"

# 优雅关闭 QClaw
Write-Host "[1/4] Closing QClaw gracefully..."
$qclawProcs = Get-Process -Name "QClaw" -ErrorAction SilentlyContinue
foreach ($p in $qclawProcs) {
    try {
        $p.CloseMainWindow() | Out-Null
    } catch {}
}

# 等待 3 秒让进程正常关闭
Start-Sleep -Seconds 3

# 检查是否已关闭，未关闭则强制终止
$stillRunning = Get-Process -Name "QClaw" -ErrorAction SilentlyContinue
if ($stillRunning) {
    Write-Host "Force stopping remaining processes..."
    $stillRunning | Stop-Process -Force
}

Write-Host "[2/4] Waiting 5 seconds..."
Start-Sleep -Seconds 5

# 使用 explorer 启动 QClaw
Start-Process "explorer.exe" -ArgumentList "`"$qclawExe`""
Write-Host "[3/4] QClaw started via explorer"

Start-Sleep -Seconds 5
$running = Get-Process -Name "QClaw" -ErrorAction SilentlyContinue
if ($running) {
    Write-Host "[4/4] SUCCESS: QClaw running with $($running.Count) processes"
} else {
    Write-Host "[4/4] FAILED: QClaw not running"
}
```

## 注意事项

- 仅限 Windows 系统使用
- 通过当前运行的 QClaw 进程获取路径（无需硬编码路径）
- 使用 `CloseMainWindow()` 优雅关闭进程，避免强制终止导致数据丢失
- 仅在进程未响应时才会强制终止
- 使用 `explorer.exe` 启动（模拟双击效果）
- QClaw 必须在运行才能执行重启
- 重启后当前会话会中断
