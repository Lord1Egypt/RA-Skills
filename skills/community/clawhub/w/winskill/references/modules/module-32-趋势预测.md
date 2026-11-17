---
id: module-32
name: 趋势预测
description: 性能基线与 SMART 趋势预测（7 天基线 P50/P95，偏离 P95 输出异常报告，SMART 劣化斜率预警磁盘故障）
keywords: ['趋势预测', '性能基线', 'P50', 'P95', 'SMART', '磁盘故障预警']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 32：性能基线与 SMART 趋势预测

> ⚠️ 本模块基于模块 31 采集的历史数据做趋势分析，**只读**，不修改任何配置。首次启用监控并采集 7 天后基线最准。

<details>
<summary>📋 展开查看：模块 32：性能基线与 SMART 趋势预测</summary>

### 32.1 性能基线（P50/P95）与偏离报告

```powershell
$outDir  = "$env:USERPROFILE\.workbuddy\output\winskill"
$metrics = Join-Path $outDir "metrics.csv"
if (-not (Test-Path $metrics)) { Write-Host "❌ 尚未采集数据，请先安装监控（模块 31）"; exit 1 }
$data = Import-Csv $metrics
if ($data.Count -lt 20) { Write-Host "⚠️ 数据不足（$($data.Count) 条），建议采集满 7 天再分析" }

# 百分位函数
function Pct($arr,$p){
    $s = ($arr | Sort-Object)
    $idx = [math]::Floor($p/100*$s.Count)
    if($idx -ge $s.Count){$idx=$s.Count-1}
    [double]$s[$idx]
}

$cpuArr  = $data | %{[double]$_.CPU_Pct}
$memArr  = $data | %{[double]$_.Mem_Pct}
$diskArr = $data | %{[double]$_.Disk_Pct}

$cpuP50=Pct $cpuArr 50;  $cpuP95=Pct $cpuArr 95
$memP50=Pct $memArr 50;  $memP95=Pct $memArr 95
$diskP50=Pct $diskArr 50; $diskP95=Pct $diskArr 95

$cpuNow=(Get-CimInstance Win32_Processor).LoadPercentage
$mem=Get-CimInstance Win32_OperatingSystem
$memNow=[math]::Round(($mem.TotalVisibleMemorySize-$mem.FreePhysicalMemory)/$mem.TotalVisibleMemorySize*100,1)
$disk=Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"|?{$_.DeviceID-eq 'C:'}
$diskNow=[math]::Round(($disk.Size-$disk.FreeSpace)/$disk.Size*100,1)

Write-Host "`n📈 性能基线（P50/P95）与偏离报告"
Write-Host ("="*64)
Write-Host ("{0,-6}{1,8}{2,8}{3,10}{4,12}{5,8}" -f "指标","P50","P95","当前","偏离P95","状态")
function Report($name,$p50,$p95,$now){
    $dev = if($p95 -gt 0){[math]::Round($now/$p95,2)}else{0}
    $st = if($now -ge $p95){"🚨越界"}elseif($now -ge $p50){"⚠️偏高"}else{"✅正常"}
    $devStr = "$dev" + "x"
    Write-Host ("{0,-6}{1,8}{2,8}{3,10}{4,12}{5,8}" -f $name,$p50,$p95,$now,$devStr,$st)
}
Report "CPU" $cpuP50 $cpuP95 $cpuNow
Report "MEM" $memP50 $memP95 $memNow
Report "DISK" $diskP50 $diskP95 $diskNow
Write-Host ("="*64)
```

### 32.2 SMART 趋势预测（磁盘故障提前预警）

```powershell
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
$smart  = Join-Path $outDir "smart_history.csv"
if (Test-Path $smart) {
    $sdata = Import-Csv $smart -Header Timestamp,DeviceID,Realloc,Pending,POH -ErrorAction SilentlyContinue
    $grouped = $sdata | Group-Object DeviceID
    foreach ($g in $grouped) {
        $rows = $g.Group | Where-Object {$_.Realloc -match '^\d+$'} | Sort-Object {[datetime]::ParseExact($_.Timestamp,'yyyy-MM-dd HH:mm:ss',$null)}
        if ($rows.Count -ge 2) {
            $first = [int]$rows[0].Realloc
            $last  = [int]$rows[-1].Realloc
            $days  = (([datetime]::ParseExact($rows[-1].Timestamp,'yyyy-MM-dd HH:mm:ss',$null)) - ([datetime]::ParseExact($rows[0].Timestamp,'yyyy-MM-dd HH:mm:ss',$null))).TotalDays
            $slope = if($days -gt 0){($last-$first)/$days}else{0}
            Write-Host ("`n💽 磁盘 {0}: 重映射扇区 {1}→{2}，斜率 {3:F2}/天" -f $g.Name,$first,$last,$slope)
            if ($last -gt 0 -and $slope -gt 0.5) { Write-Host "   🔴 劣化加速，建议立即备份并更换磁盘" }
            elseif ($last -gt 0) { Write-Host "   ⚠️ 存在重映射扇区，持续观察" }
            else { Write-Host "   ✅ 扇区健康" }
        }
    }
} else { Write-Host "`n💽 尚无 SMART 数据（需监控运行数日后积累，见模块 31）" }
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `数据不足` | 监控刚启用 | 等待采集满 7 天，基线更准 |
| SMART 无数据 | 存储模块缺失/无权限 | 不影响 CPU/内存/磁盘使用率趋势 |
| 百分位异常 | CSV 中存在空行 | 删除 metrics.csv 末尾空行或重建监控 |

</details>

[↑ 返回顶部](#module-1)

---
