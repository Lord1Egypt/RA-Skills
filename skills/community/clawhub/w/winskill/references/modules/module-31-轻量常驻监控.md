---
id: module-31
name: 轻量常驻监控
description: 轻量常驻监控（schtasks 定时采样 CPU/内存/磁盘/服务/事件日志，写入 metrics.csv，阈值超限写入 alerts）
keywords: ['常驻监控', '定时采样', '性能监控', '告警', 'metrics']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 31：轻量常驻监控

> ⚠️ 本模块通过 Windows 计划任务（schtasks）周期性采样，**不常驻进程**，零内存占用、抗重启，这是与商业监控软件的定位差异。

<details>
<summary>📋 展开查看：模块 31：轻量常驻监控</summary>

### 31.1 安装监控（注册计划任务 + 采样器）

> 需管理员权限。采样器脚本在**运行时**生成到 `~/.workbuddy/output/winskill/`（不进 skill 仓库，符合禁止文件类型规则），再由计划任务调用。

```powershell
# ===== 安装轻量常驻监控 =====
$outDir  = "$env:USERPROFILE\.workbuddy\output\winskill"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# 1) 采样器脚本（运行时生成）
$sampler = @'
$ErrorActionPreference = 'SilentlyContinue'
$outDir  = "$env:USERPROFILE\.workbuddy\output\winskill"
$metrics = Join-Path $outDir "metrics.csv"
$alerts  = Join-Path $outDir "alerts.csv"
$smart   = Join-Path $outDir "smart_history.csv"
$thFile  = Join-Path $outDir "thresholds.yaml"

# --- 读取阈值（扁平键值，PowerShell 5.1 原生可解析）---
$t = @{}
if (Test-Path $thFile) {
    Get-Content $thFile | ForEach-Object {
        $l = $_.Trim()
        if ($l -and -not $l.StartsWith('#') -and $l -match '^(.+?):\s*(.+)$') {
            $t[$matches[1].Trim()] = $matches[2].Trim().Trim('"')
        }
    }
}
function N($k,$d){ if($t.ContainsKey($k)){try{[int]$t[$k]}catch{$d}}else{$d} }
$cpuW=N 'cpu_warn' 80;  $cpuA=N 'cpu_alert' 90
$memW=N 'mem_warn' 85;  $memA=N 'mem_alert' 95
$diskW=N 'disk_warn' 85; $diskA=N 'disk_alert' 95
$evtWin=N 'evt_window_min' 15; $evtMax=N 'evt_max' 50
$dedup=N 'dedup_min' 30
$svcList = if($t.ContainsKey('svc_check')){($t['svc_check'] -split ','|%{$_.Trim()})}else{@('Spooler','Winmgmt','Dnscache')}

# --- 采样 ---
$cpu = (Get-CimInstance Win32_Processor).LoadPercentage
$mem = Get-CimInstance Win32_OperatingSystem
$memPct = [math]::Round(($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory)/$mem.TotalVisibleMemorySize*100,1)
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Where-Object DeviceID -eq 'C:'
$diskPct = [math]::Round(($disk.Size-$disk.FreeSpace)/$disk.Size*100,1)
$svcDown = ($svcList | ForEach-Object { $s=Get-Service -Name $_ -ErrorAction SilentlyContinue; if($s -and $s.Status -ne 'Running'){$_} }) -join ','
$since = (Get-Date).AddMinutes(-$evtWin)
$evtErr = (Get-WinEvent -FilterHashtable @{LogName='System';Level=2;StartTime=$since} -ErrorAction SilentlyContinue).Count
$ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

if (-not (Test-Path $metrics)) { "Timestamp,CPU_Pct,Mem_Pct,Disk_Pct,SvcDown,EvtErr" | Out-File $metrics -Encoding utf8 }
"$ts,$cpu,$memPct,$diskPct,$svcDown,$evtErr" | Out-File $metrics -Append -Encoding utf8

# --- SMART 快照（供趋势预测使用）---
try {
    foreach ($d in (Get-Disk)) {
        $rc = $d | Get-StorageReliabilityCounter -ErrorAction SilentlyContinue
        if ($rc) {
            $realloc = $rc.ReallocatedSectors
            $pending = $rc.PendingSectors
            $poh = $rc.PowerOnHours
            if (-not (Test-Path $smart)) { "Timestamp,DeviceID,Realloc,Pending,POH" | Out-File $smart -Encoding utf8 }
            "$ts,$($d.DeviceID),$realloc,$pending,$poh" | Out-File $smart -Append -Encoding utf8
        }
    }
} catch {}

# --- 阈值检查 + 告警（带去抖）---
function Write-Alert($metric,$val,$th,$level,$rec){
    if (Test-Path $alerts) {
        $recent = Get-Content $alerts -Tail 200 | Where-Object { $_ -match $metric -and $_ -match $level }
        foreach ($r in $recent) {
            $parts = $r -split ','
            try { $rt = [datetime]::ParseExact($parts[0],'yyyy-MM-dd HH:mm:ss',$null) } catch { $rt = [datetime]::MinValue }
            if (((Get-Date)-$rt).TotalMinutes -lt $dedup) { return }
        }
    }
    if (-not (Test-Path $alerts)) { "Timestamp,Host,Metric,Value,Threshold,Level,Recommend" | Out-File $alerts -Encoding utf8 }
    "$ts,$env:COMPUTERNAME,$metric,$val,$th,$level,$rec" | Out-File $alerts -Append -Encoding utf8
}

if ($cpu -ge $cpuA) { Write-Alert 'CPU' $cpu $cpuA 'ALERT' '检查高 CPU 进程（模块 9.2）' }
elseif ($cpu -ge $cpuW) { Write-Alert 'CPU' $cpu $cpuW 'WARN' '关注 CPU 负载' }
if ($memPct -ge $memA) { Write-Alert 'MEM' $memPct $memA 'ALERT' '检查内存占用 Top 进程' }
elseif ($memPct -ge $memW) { Write-Alert 'MEM' $memPct $memW 'WARN' '关注内存使用' }
if ($diskPct -ge $diskA) { Write-Alert 'DISK' $diskPct $diskA 'ALERT' '立即清理磁盘空间' }
elseif ($diskPct -ge $diskW) { Write-Alert 'DISK' $diskPct $diskW 'WARN' '规划磁盘清理' }
if ($svcDown) { Write-Alert 'SVC' $svcDown 'Running' 'ALERT' "重启服务: $svcDown" }
if ($evtErr -ge $evtMax) { Write-Alert 'EVT' $evtErr $evtMax 'WARN' '检查系统日志错误' }
'@
$samplerPath = Join-Path $outDir "monitor_sampler.ps1"
Set-Content -Path $samplerPath -Value $sampler -Encoding utf8

# 2) 默认阈值文件（用户可编辑此副本）
$thDefault = @'
version: "1.0.0"
updated: "2026-09-11"
# 扁平键值格式，PowerShell 5.1 原生可解析；修改后下一采样周期自动生效
cpu_warn: 80
cpu_alert: 90
mem_warn: 85
mem_alert: 95
disk_warn: 85
disk_alert: 95
svc_check: Spooler,Winmgmt,Dnscache,W32Time
evt_window_min: 15
evt_max: 50
dedup_min: 30
'@
$thPath = Join-Path $outDir "thresholds.yaml"
if (-not (Test-Path $thPath)) { Set-Content -Path $thPath -Value $thDefault -Encoding utf8 }

# 3) 注册计划任务（每 10~15 分钟，SYSTEM 账户，不常驻进程）
$cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$interval = if ($cpuCores -le 4) { 15 } else { 10 }
$taskName = "Winskill_Monitor"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$samplerPath`""
# 重复时长上限约 248 天（Windows 限制），取 248 天等效"长期运行"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $interval) -RepetitionDuration (New-TimeSpan -Days 248)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -User "SYSTEM" -RunLevel Highest -Force
Write-Host "✅ 监控已安装：计划任务 '$taskName' 每 $interval 分钟采样一次（CPU $cpuCores 核）"
Write-Host "   指标: $metrics"
Write-Host "   告警: $alerts"
Write-Host "   阈值: $thPath （可编辑，改完下一周期生效）"
```

### 31.2 查看实时指标

```powershell
$metrics = "$env:USERPROFILE\.workbuddy\output\winskill\metrics.csv"
if (-not (Test-Path $metrics)) { Write-Host "❌ 尚无数据，请先运行 31.1 安装监控"; exit 1 }
$data = Import-Csv $metrics
Write-Host "`n📊 最近 10 条采样："
$data | Select-Object -Last 10 | Format-Table Timestamp, CPU_Pct, Mem_Pct, Disk_Pct, SvcDown, EvtErr -AutoSize
Write-Host ("总计 {0} 条记录" -f $data.Count)
```

### 31.3 查看告警

```powershell
$alerts = "$env:USERPROFILE\.workbuddy\output\winskill\alerts.csv"
if (-not (Test-Path $alerts)) { Write-Host "✅ 无告警记录"; exit 0 }
Import-Csv $alerts | Select-Object -Last 20 | Format-Table Timestamp, Host, Metric, Value, Threshold, Level, Recommend -AutoSize
```

### 31.4 卸载监控

```powershell
$taskName = "Winskill_Monitor"
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "✅ 已卸载监控计划任务 '$taskName'（历史数据保留在 output 目录，可手动清理）"
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `Register-ScheduledTask 拒绝访问` | 需要管理员权限 | 以管理员身份运行 PowerShell |
| `在此系统上禁止运行脚本` | 执行策略限制 | 安装脚本已用 `-ExecutionPolicy Bypass`，若仍报错先 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `Get-StorageReliabilityCounter 找不到` | 存储模块未加载 | 非致命，SMART 数据会缺失，趋势预测（模块 32）跳过该项 |
| 采样数据为空 | 计划任务未触发 | `taskschd.msc` 查看 Winskill_Monitor 上次运行结果 |

</details>

[↑ 返回顶部](#module-1)

---
