---
id: module-09
name: 实时性能监控与进程资源分析
description: 定位 CPU/内存/磁盘 I/O 瓶颈，按进程排序找到罪魁祸首。
keywords: ['服务器变卡了，帮我看看', '哪个进程吃内存最多']
permission: admin
mode: readonly
subset: performance
---

## 🆕 模块 9：实时性能监控与进程资源分析




<details>
<summary>📋 展开查看：🆕 模块 9：实时性能监控与进程资源分析</summary>

**用途**：定位 CPU/内存/磁盘 I/O 瓶颈，按进程排序找到罪魁祸首。

**常你说**：`"服务器变卡了，帮我看看"` / `"哪个进程吃内存最多"`

### 9.1 实时性能计数器（只读）




```powershell
Get-Counter '\Processor(_Total)\% Processor Time',
              '\Memory\Available MBytes',
              '\Memory\% Used',
              '\PhysicalDisk(_Total)\% Disk Time',
              '\PhysicalDisk(_Total)\Current Disk Queue Length' |
    Select-Object -ExpandProperty CounterSamples |
    Select-Object @{N='指标';E={$_.Path.Split('\')[-2..-1] -join '\'}},
        @{N='当前值';E={[math]::Round($_.CookedValue, 1)}} |
    Format-Table -AutoSize
```



### 9.2 内存占用 Top 10 进程




```powershell
Get-Process | Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 @{N='进程名';E={$_.Name}},
        @{N='内存(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}},
        @{N='CPU(s)';E={[math]::Round($_.CPU,1)}} |
    Format-Table -AutoSize
```



### 9.3 磁盘 I/O 详细统计（按进程）




```powershell
Get-Counter '\Process(*)\Read Bytes/sec',
              '\Process(*)\Write Bytes/sec' |
    Select-Object -ExpandProperty CounterSamples |
    Where-Object { $_.CookedValue -gt 0 } |
    Sort-Object CookedValue -Descending |
    Select-Object -First 15 @{N='进程';E={
        $_.Path -replace '\\Process\((.*)\)\\Read Bytes/sec$','$1' |
        ForEach-Object { if ($_ -eq 'idle') { 'System Idle' } else { $_ }
    }}, @{N='Bytes/s';E={[math]::Round($_.CookedValue, 0)}} |
    Format-Table -AutoSize
```






```powershell
# ⚠️ 仅当用户明确说「确认创建」后才执行！
# $collector = New-DataCollectorSet -Name "ServerPerf_$(Get-Date -Format 'yyyyMMdd')" -Path "C:\PerfLogs"
# $collector.DataCollectors.Create(0, "Counter", 0,
#     '\Processor(_Total)\% Processor Time',
#     '\Memory\Available MBytes',
#     '\PhysicalDisk(_Total)\% Disk Time'
# )
# $collector.Commit("C:\PerfLogs\ServerPerf", 0, 0x01) | Out-Null
# Write-Host "  ✅ 已创建性能采集器，数据将保存到 C:\PerfLogs"
```



**风险等级**：🟢 实时查看 / 🟡 创建采集器需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `The specified counter is not found` | 计数器未注册 | 运行 `lodctr /R` 重建计数器 |
| `Access denied` | 需要管理员权限 | 提升后执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| CPU 持续 >90% | 按进程排序定位异常进程 |
| 可用内存 <500MB | 判断是否内存泄漏， IIS 应用池是否需回收 |
| 磁盘队列长度 >2 | I/O 瓶颈，检查是否日志写入过多 |
| 计数器全为零 | `lodctr /R` 重建性能计数器 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-10"></a>

