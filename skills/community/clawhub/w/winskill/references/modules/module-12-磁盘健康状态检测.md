---
id: module-12
name: 磁盘健康状态检测
description: 检测磁盘 SMART 状态、坏道预警、磁盘寿命预测。
keywords: ['硬盘还健康吗？', '有没有坏道', '磁盘寿命还剩多久']
permission: admin
mode: readonly
subset: disk-management
---

## 🆕 模块 12：磁盘健康状态检测




<details>
<summary>📋 展开查看：🆕 模块 12：磁盘健康状态检测</summary>

**用途**：检测磁盘 SMART 状态、坏道预警、磁盘寿命预测。

**常你说**：`"硬盘还健康吗？"` / `"有没有坏道"` / `"磁盘寿命还剩多久"`

> ⚠️ **本模块所有操作均为只读检测，不会执行磁盘修复或擦除操作。**

### 12.1 SMART 状态概览




```powershell
Write-Host "════════ 磁盘 SMART 状态 ════════"
Get-PhysicalDisk | Select-Object @{N='磁盘';E={$_.FriendlyName}},
    @{N='状态';E={$_.HealthStatus}},
    @{N='使用时长';E={[math]::Round($_.UsageHours,0)}},
    @{N='温度(°C)';E={$_.Temperature}},
    @{N='剩余寿命%';E={$_.RemainingLifetimePercent}} |
    Format-Table -AutoSize
```



### 12.2 磁盘坏道与错误计数




```powershell
Write-Host "════════ 磁盘错误统计 ════════"
Get-PhysicalDisk | ForEach-Object {
    $disk = $_
    $errors = Get-StorageReliabilityCounter -PhysicalDisk $disk -ErrorAction SilentlyContinue
    if ($errors) {
        [PSCustomObject]@{
            磁盘 = $disk.FriendlyName
            读取错误 = $errors.ReadErrorsTotal
            写入错误 = $errors.WriteErrorsTotal
            重映射扇区 = $errors.ReallocatedSectors
            待映射扇区 = $errors.PendingSectors
            不可修复错误 = $errors.UncorrectableErrors
        }
    }
} | Format-Table -AutoSize

Write-Host "`n  💡 重映射扇区 >0 或待映射扇区 >0 表示磁盘开始老化"
Write-Host "  💡 不可修复错误 >0 建议立即备份数据并更换磁盘"
```



### 12.3 磁盘温度监控




```powershell
Write-Host "════════ 磁盘温度监控 ════════"
Get-PhysicalDisk | ForEach-Object {
    $temp = $_.Temperature
    if ($temp -gt 50)     { $icon = '🔴' }
    elseif ($temp -gt 40) { $icon = '🟡' }
    else                  { $icon = '🟢' }
    [PSCustomObject]@{
        磁盘 = $_.FriendlyName
        温度 = "${temp}°C"
        状态 = $icon
    }
} | Format-Table -AutoSize

Write-Host "`n  💡 温度 >50°C 需检查散热，>60°C 立即停机检查"
```



### 12.4 磁盘 I/O 延迟分析




```powershell
Write-Host "════════ 磁盘 I/O 延迟 ════════"
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Read',
              '\PhysicalDisk(*)\Avg. Disk sec/Write' |
    Select-Object -ExpandProperty CounterSamples |
    Where-Object { $_.CookedValue -gt 0 } |
    Select-Object @{N='磁盘';E={
        $_.Path -replace '\\PhysicalDisk\((.*)\)\\.*$','$1'
    }}, @{N='平均延迟(ms)';E={[math]::Round($_.CookedValue * 1000, 2)}} |
    Format-Table -AutoSize

Write-Host "`n  💡 读延迟 >20ms 或写延迟 >20ms 表示磁盘性能下降"
```



**风险等级**：🟢 无（只读检测）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `No MSFT_PhysicalDisk ...` | 系统不支持存储诊断 | 需 Windows Server 2016+ |
| `Temperature` 属性不存在 | 磁盘不支持温度传感器 | 用第三方工具检测 |
| `Get-StorageReliabilityCounter` 报错 | 需要管理员权限 | 提升执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| SMART 状态显示 "Warning" | 磁盘开始老化，立即备份数据 |
| 重映射扇区持续增长 | 磁盘寿命将尽，尽快更换 |
| I/O 延迟突然飙升 | 可能磁盘故障前兆，检查 SMART |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-13"></a>

