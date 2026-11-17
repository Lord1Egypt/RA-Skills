# windows-health-scan · Windows 磁盘+性能健康诊断脚本 v1.0
# 用法：powershell -ExecutionPolicy Bypass -File scan.ps1          快速扫描
#       powershell -ExecutionPolicy Bypass -File scan.ps1 -Deep    深度诊断（大文件 + node_modules）
#
# 铁律：本脚本只输出报告和候选命令，不自动删除任何文件。

param([switch]$Deep)

$Date = Get-Date -Format 'yyyy-MM-dd HH:mm'
Write-Host "━━━ Windows Health 诊断报告 · $Date ━━━"
Write-Host ""

# ── 权限检测 ────────────────────────────────────────────────────────────
$IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Host "权限：$(if ($IsAdmin) { '管理员' } else { '普通用户（管理员级动作需另行提权）' })"
Write-Host ""

# ── 磁盘概况 ────────────────────────────────────────────────────────────
Write-Host "📊 磁盘概况"
Get-PSDrive -PSProvider FileSystem | Where-Object { $null -ne $_.Used } | ForEach-Object {
  $usedGB = [math]::Round($_.Used / 1GB, 1)
  $freeGB = [math]::Round($_.Free / 1GB, 1)
  $total = $_.Used + $_.Free
  $pct = if ($total -gt 0) { [math]::Round($_.Used / $total * 100, 0) } else { 0 }
  Write-Host ("  {0}: 已用 {1}GB | 可用 {2}GB | 使用率 {3}%" -f $_.Name, $usedGB, $freeGB, $pct)
}
Write-Host ""

# ── 性能诊断（只读 · Microsoft 官方口径）───────────────────────────────
Write-Host "📈 性能诊断（只读 · Microsoft 官方口径）"
$os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
if ($os) {
  $totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
  $freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
  Write-Host ("  物理内存: {0}GB | 可用: {1}GB" -f $totalGB, $freeGB)
}
Write-Host "  高 CPU 进程（前 8）:"
Get-Process | Sort-Object CPU -Descending | Select-Object -First 8 | ForEach-Object {
  Write-Host ("    {0,-28} CPU {1,10:N1}s  MEM {2,12:N0} KB" -f $_.ProcessName, $_.CPU, ($_.WorkingSet64 / 1KB))
}
Write-Host "  启动项（Win32_StartupCommand · 前 15）:"
Get-CimInstance Win32_StartupCommand -ErrorAction SilentlyContinue | Select-Object -First 15 | ForEach-Object {
  Write-Host ("    {0}  <-  {1}" -f $_.Name, $_.Location)
}
Write-Host "  💡 判定：页面文件/内存打满 = 内存不足强信号；C 盘可用空间极低时优先官方释放顺序（存储感知/磁盘清理/卸载 App/清空回收站）。"
Write-Host ""

# ── 缓存热点（TIER 1 · 需用户确认后执行）──────────────────────────────
Write-Host "🗑️  可安全清理的缓存（TIER 1 · 需用户确认后执行）"
$caches = @("$env:TEMP", "$env:LOCALAPPDATA\Temp", "$env:LOCALAPPDATA\npm-cache", "$env:APPDATA\npm-cache", "$env:LOCALAPPDATA\pip\Cache")
foreach ($c in $caches) {
  if (Test-Path $c) {
    $size = (Get-ChildItem $c -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    Write-Host ("  {0,12:N0} KB  {1}" -f ($size / 1KB), $c)
  }
}
Write-Host ""

# ── 回收站 ──────────────────────────────────────────────────────────────
Write-Host "📋 回收站（清空不可恢复，需单独确认）"
Write-Host "  命令（未执行）：Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
Write-Host ""

# ── 最近使用（双击代理）─────────────────────────────────────────────────
Write-Host "🖱️  最近使用（Recent Items · 仅双击代理）"
Get-ChildItem "$env:APPDATA\Microsoft\Windows\Recent" -Filter *.lnk -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
    Write-Host ("  {0}" -f $_.Name)
  }
Write-Host ""

# ── 深度诊断 ─────────────────────────────────────────────────────────────
if ($Deep) {
  Write-Host "📦 大文件（>200MB，不含 AppData\Roaming）"
  Get-ChildItem $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 200MB -and $_.FullName -notmatch '\\AppData\\Roaming' } |
    Sort-Object Length -Descending | Select-Object -First 20 | ForEach-Object {
      Write-Host ("  {0,8:N2} GB  {1}" -f ($_.Length / 1GB), $_.FullName)
    }
  Write-Host ""

  Write-Host "🧶 node_modules（可用 npm install 重建 · 前 10）"
  Get-ChildItem $env:USERPROFILE -Recurse -Directory -Filter node_modules -ErrorAction SilentlyContinue |
    Select-Object -First 10 | ForEach-Object {
      $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
      Write-Host ("  {0,12:N0} KB  {1}" -f ($size / 1KB), $_.FullName)
    }
  Write-Host ""
}

Write-Host "━━━ 诊断完成 · 本脚本不删除任何文件，所有清理命令需用户确认后执行 ━━━"
