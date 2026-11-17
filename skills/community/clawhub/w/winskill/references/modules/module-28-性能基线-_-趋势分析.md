---
id: module-28
name: 性能基线 & 趋势分析
description: 性能基线 & 趋势分析
keywords: ['性能基线 & 趋势分析']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 28：性能基线 & 趋势分析

> ⚠️ **本模块所有操作均为只读分析，不会修改任何系统配置。**

<details>
<summary>📋 展开查看：模块 28：性能基线 & 趋势分析</summary>

### 28.1 性能基线建立（7 天采集）

**硬件自适应策略**：根据 CPU 核心数动态调整采集频率，避免拖累低配服务器。

```powershell
# 硬件自适应：确定采集间隔
$cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$intervalMinutes = if ($cpuCores -le 4) { 15 } else { 5 }
$tagFile = "$env:USERPROFILE\.workbuddy\output\winskill\baseline_tag.txt"
$csvFile = "$env:USERPROFILE\.workbuddy\output\winskill\perf_baseline.csv"

# 创建输出目录
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.workbuddy\output\winskill" | Out-Null

# 检查是否已注册定时任务
$taskName = "Winskill_PerfBaseline"
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if (-not $existingTask) {
    # 注册定时任务（需管理员权限）
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument @"
-Command "& {`$csv='$csvFile'; `$cpu=(Get-CimInstance Win32_Processor).LoadPercentage; `$mem=(Get-CimInstance Win32_OperatingSystem); `$memPct=[math]::Round(($mem.TotalVisibleMemorySize - `$mem.FreePhysicalMemory)/`$mem.TotalVisibleMemorySize*100,1); `$disk=(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Where-Object DeviceID -eq 'C:'); `$diskPct=[math]::Round((`$disk.Size-`$disk.FreeSpace)/`$disk.Size*100,1); `$net=(Get-CimInstance Win32_PerfFormattedData_Tcpip_NetworkInterface | Where-Object Name -notlike '*Loopback*' | Measure-Object BytesTotalPersec -Sum).Sum; `$ts=Get-Date -Format 'yyyy-MM-dd HH:mm:ss'; if(-not(Test-Path `$csv)){'Timestamp,CPU_Pct,Mem_Pct,Disk_Pct,Net_BytesPerSec' | Out-File `$csv -Encoding utf8}; '`$ts,`$cpu,`$memPct,`$diskPct,`$net' | Out-File `$csv -Append -Encoding utf8}"
'@
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $intervalMinutes) -RepetitionDuration (New-TimeSpan -Days 7)
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Description "Winskill 性能基线采集（7 天）" -Force
    Write-Host "✅ 已注册定时任务 '$taskName'，每 $intervalMinutes 分钟采集一次，持续 7 天"
} else {
    Write-Host "⚠️ 定时任务 '$taskName' 已存在，无需重复注册"
}

# 显示当前基线状态
if (Test-Path $csvFile) {
    $data = Import-Csv $csvFile
    Write-Host "`n📊 当前基线数据：$($data.Count) 条记录"
    Write-Host "CPU 基线：$(($data | Measure-Object CPU_Pct -Average).Average)%（均值）"
    Write-Host "内存 基线：$(($data | Measure-Object Mem_Pct -Average).Average)%（均值）"
    Write-Host "磁盘 基线：$(($data | Measure-Object Disk_Pct -Average).Average)%（均值）"
} else {
    Write-Host "📋 尚未开始采集，注册定时任务后自动开始"
}
```

### 28.2 异常偏离告警（当前值 vs 基线）

```powershell
$csvFile = "$env:USERPROFILE\.workbuddy\output\winskill\perf_baseline.csv"
$thresholdMultiplier = 2.0  # 偏离基线 200% 触发告警

if (-not (Test-Path $csvFile)) {
    Write-Host "❌ 尚未建立基线，请先运行 28.1 建立基线"
    exit 1
}

$data = Import-Csv $csvFile
if ($data.Count -lt 10) {
    Write-Host "⚠️ 基线数据不足（$($data.Count) 条），建议至少采集 10 条后再分析"
}

# 计算基线均值
$cpuAvg = ($data | Measure-Object CPU_Pct -Average).Average
$memAvg = ($data | Measure-Object Mem_Pct -Average).Average
$diskAvg = ($data | Measure-Object Disk_Pct -Average).Average

# 获取当前值
$cpuNow = (Get-CimInstance Win32_Processor).LoadPercentage
$mem = (Get-CimInstance Win32_OperatingSystem)
$memNow = [math]::Round(($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize * 100, 1)
$disk = (Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Where-Object DeviceID -eq 'C:')
$diskNow = [math]::Round(($disk.Size - $disk.FreeSpace) / $disk.Size * 100, 1)

Write-Host "`n📊 偏离分析报告"
Write-Host ("=" * 50)
Write-Host ("指标     当前值    基线均值    偏离倍数    状态")
Write-Host ("-" * 50)

$alerts = @()

$cpuDev = if ($cpuAvg -gt 0) { $cpuNow / $cpuAvg } else { 0 }
$status = if ($cpuDev -ge $thresholdMultiplier) { "🚨 告警" } elseif ($cpuDev -ge 1.5) { "⚠️ 警告" } else { "✅ 正常" }
Write-Host ("CPU      {0,6}%    {1,6}%    {2,6:F1}x      {3}" -f $cpuNow, $cpuAvg, $cpuDev, $status)
if ($cpuDev -ge $thresholdMultiplier) { $alerts += "CPU 使用率偏离基线 ${cpuDev:F1} 倍（当前 $cpuNow%，基线 $cpuAvg%）" }

$memDev = if ($memAvg -gt 0) { $memNow / $memAvg } else { 0 }
$status = if ($memDev -ge $thresholdMultiplier) { "🚨 告警" } elseif ($memDev -ge 1.5) { "⚠️ 警告" } else { "✅ 正常" }
Write-Host ("内存     {0,6}%    {1,6}%    {2,6:F1}x      {3}" -f $memNow, $memAvg, $memDev, $status)
if ($memDev -ge $thresholdMultiplier) { $alerts += "内存使用率偏离基线 ${memDev:F1} 倍（当前 $memNow%，基线 $memAvg%）" }

$diskDev = if ($diskAvg -gt 0) { $diskNow / $diskAvg } else { 0 }
$status = if ($diskDev -ge 1.3) { "🚨 告警" } elseif ($diskDev -ge 1.1) { "⚠️ 警告" } else { "✅ 正常" }
Write-Host ("磁盘     {0,6}%    {1,6}%    {2,6:F1}x      {3}" -f $diskNow, $diskAvg, $diskDev, $status)
if ($diskDev -ge 1.3) { $alerts += "磁盘使用率偏离基线 ${diskDev:F1} 倍（当前 $diskNow%，基线 $diskAvg%）" }

Write-Host ("=" * 50)

if ($alerts.Count -eq 0) {
    Write-Host "`n✅ 所有指标正常，无异常偏离"
} else {
    Write-Host "`n🚨 发现 $($alerts.Count) 项异常偏离："
    $alerts | ForEach-Object { Write-Host "  ⚠️ $_" }
}
```

### 28.3 趋势预测（磁盘耗尽时间）

```powershell
$csvFile = "$env:USERPROFILE\.workbuddy\output\winskill\perf_baseline.csv"

if (-not (Test-Path $csvFile)) {
    Write-Host "❌ 尚未建立基线，请先运行 28.1 建立基线"
    exit 1
}

$data = Import-Csv $csvFile
if ($data.Count -lt 5) {
    Write-Host "⚠️ 数据不足（$($data.Count) 条），无法预测"
    exit 1
}

# 简单线性回归预测磁盘耗尽时间
$diskValues = $data | ForEach-Object { [double]$_.Disk_Pct }
$n = $diskValues.Count

# 计算斜率（每天增长百分比）
$sumX = ($n - 1) * $n / 2
$sumY = ($diskValues | Measure-Object -Sum).Sum
$sumXY = 0
$sumX2 = 0
for ($i = 0; $i -lt $n; $i++) {
    $sumXY += $i * $diskValues[$i]
    $sumX2 += $i * $i
}
$slope = ($n * $sumXY - $sumX * $sumY) / ($n * $sumX2 - $sumX * $sumX)

$currentDisk = $diskValues[-1]

Write-Host "`n📈 趋势预测报告"
Write-Host ("=" * 50)
Write-Host ("当前磁盘使用率：{0}%" -f $currentDisk)

if ($slope -le 0) {
    Write-Host ("趋势：磁盘使用率稳定或下降（斜率 {0:F4}%/采集周期）" -f $slope)
    Write-Host "✅ 磁盘空间充足，无需担心"
} else {
    # 估算耗尽时间（基于采集间隔）
    $cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
    $intervalMinutes = if ($cpuCores -le 4) { 15 } else { 5 }
    $periodsPerDay = 24 * 60 / $intervalMinutes
    $daysToFull = (100 - $currentDisk) / ($slope * $periodsPerDay)
    
    Write-Host ("增长速率：{0:F4}%/采集周期（约 {1:F2}%/天）" -f $slope, ($slope * $periodsPerDay))
    
    if ($daysToFull -gt 365) {
        Write-Host ("预计耗尽时间：> 1 年（约 {0:F0} 天）" -f $daysToFull)
        Write-Host "✅ 磁盘空间充足"
    } elseif ($daysToFull -gt 30) {
        Write-Host ("预计耗尽时间：约 {0:F0} 天（{1:F1} 个月）" -f $daysToFull, ($daysToFull / 30))
        Write-Host "⚠️ 建议关注磁盘使用趋势"
    } elseif ($daysToFull -gt 7) {
        Write-Host ("预计耗尽时间：约 {0:F0} 天" -f $daysToFull)
        Write-Host "🚨 建议尽快清理磁盘空间"
    } else {
        Write-Host ("预计耗尽时间：约 {0:F0} 天" -f $daysToFull)
        Write-Host "🔴 磁盘即将耗尽！请立即清理"
    }
}

# 内存趋势预测
$memValues = $data | ForEach-Object { [double]$_.Mem_Pct }
$sumY = ($memValues | Measure-Object -Sum).Sum
$sumXY = 0
for ($i = 0; $i -lt $n; $i++) {
    $sumXY += $i * $memValues[$i]
}
$slope = ($n * $sumXY - $sumX * $sumY) / ($n * $sumX2 - $sumX * $sumX)
$currentMem = $memValues[-1]

Write-Host ("`n当前内存使用率：{0}%" -f $currentMem)
if ($slope -le 0) {
    Write-Host "趋势：内存使用率稳定或下降 ✅"
} else {
    $periodsPerDay = 24 * 60 / $intervalMinutes
    $daysToFull = (95 - $currentMem) / ($slope * $periodsPerDay)  # 95% 作为预警线
    if ($daysToFull -gt 30) {
        Write-Host ("增长速率：{0:F4}%/采集周期 ✅ 内存充足" -f $slope)
    } elseif ($daysToFull -gt 0) {
        Write-Host ("增长速率：{0:F4}%/采集周期 ⚠️ 约 {1:F0} 天后达到 95%" -f $slope, $daysToFull)
    } else {
        Write-Host "🔴 内存使用率持续上升，建议排查内存泄漏"
    }
}
Write-Host ("=" * 50)
```

### 28.4 性能瓶颈关联分析

```powershell
Write-Host "`n🔍 性能瓶颈关联分析"
Write-Host ("=" * 60)

# 采集四维指标
$cpu = (Get-CimInstance Win32_Processor).LoadPercentage
$mem = (Get-CimInstance Win32_OperatingSystem)
$memPct = [math]::Round(($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize * 100, 1)
$disk = Get-CimInstance Win32_PerfFormattedData_PerfDisk_PhysicalDisk | Where-Object Name -eq "_Total"
$diskPct = [math]::Round($disk.PercentDiskTime, 1)
$net = Get-CimInstance Win32_PerfFormattedData_Tcpip_NetworkInterface | Where-Object Name -notlike '*Loopback*'
$netPct = [math]::Round(($net | Measure-Object BytesTotalPersec -Sum).Sum / 1MB, 1)  # MB/s

Write-Host ("CPU 使用率：    {0,6}%" -f $cpu)
Write-Host ("内存使用率：    {0,6}%" -f $memPct)
Write-Host ("磁盘活动时间：  {0,6}%" -f $diskPct)
Write-Host ("网络流量：      {0,6} MB/s" -f $netPct)
Write-Host ("-" * 60)

# 瓶颈判定逻辑
$bottleneck = $null
$severity = "正常"

if ($cpu -ge 90 -and $memPct -ge 85) {
    $bottleneck = "CPU + 内存双重瓶颈"
    $severity = "🔴 严重"
} elseif ($diskPct -ge 90 -and $memPct -ge 85) {
    $bottleneck = "磁盘 I/O + 内存双重瓶颈（可能存在内存交换）"
    $severity = "🔴 严重"
} elseif ($cpu -ge 90) {
    $bottleneck = "CPU 瓶颈"
    $severity = "🚨 高"
} elseif ($memPct -ge 90) {
    $bottleneck = "内存瓶颈"
    $severity = "🚨 高"
} elseif ($diskPct -ge 90) {
    $bottleneck = "磁盘 I/O 瓶颈"
    $severity = "🚨 高"
} elseif ($cpu -ge 70 -and $memPct -ge 70) {
    $bottleneck = "CPU + 内存轻度压力"
    $severity = "⚠️ 中"
} elseif ($diskPct -ge 70 -and $memPct -ge 70) {
    $bottleneck = "磁盘 + 内存轻度压力"
    $severity = "⚠️ 中"
} elseif ($cpu -ge 70) {
    $bottleneck = "CPU 轻度压力"
    $severity = "⚠️ 中"
} elseif ($memPct -ge 70) {
    $bottleneck = "内存轻度压力"
    $severity = "⚠️ 中"
} elseif ($diskPct -ge 70) {
    $bottleneck = "磁盘 I/O 轻度压力"
    $severity = "⚠️ 中"
}

if ($bottleneck) {
    Write-Host ("瓶颈判定：{0}（{1}）" -f $bottleneck, $severity)
} else {
    Write-Host "✅ 系统运行正常，无明显瓶颈"
}

# 关联分析建议
Write-Host ("-" * 60)
Write-Host "关联分析："

if ($memPct -ge 85 -and $diskPct -ge 80) {
    Write-Host "  ⚠️ 内存高 + 磁盘 I/O 高 → 可能发生内存交换（页面文件频繁读写）"
    Write-Host "  建议：检查内存占用 Top 进程（模块 9.2），考虑增加物理内存"
}

if ($cpu -ge 80 -and $diskPct -ge 80) {
    Write-Host "  ⚠️ CPU 高 + 磁盘 I/O 高 → 可能在进行大量文件操作或数据库查询"
    Write-Host "  建议：检查磁盘 I/O 进程（模块 9.3），定位高 I/O 来源"
}

if ($netPct -gt 100 -and $cpu -ge 70) {
    Write-Host "  ⚠️ 网络流量大 + CPU 高 → 可能受到 DDoS 攻击或大量数据传输"
    Write-Host "  建议：检查网络连接（模块 13.1），排查可疑外连（模块 13.3）"
}

if ($cpu -lt 50 -and $memPct -lt 50 -and $diskPct -lt 50) {
    Write-Host "  ✅ 四维指标均正常，系统健康"
}

Write-Host ("=" * 60)
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `Register-ScheduledTask 拒绝访问` | 需要管理员权限 | 以管理员身份运行 PowerShell |
| `无法加载文件，因为在此系统上禁止运行脚本` | 执行策略限制 | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `基线数据不足` | 采集时间太短 | 等待至少 10 个采集周期后再分析 |
| `Get-CimInstance 找不到类` | WMI 服务异常 | 运行 `winmgmt /resetrepository` |

</details>


[↑ 返回顶部](#module-1)

---

<a name="module-29"></a>

