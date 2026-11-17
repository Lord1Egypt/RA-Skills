---
id: module-24
name: 存储池与虚拟磁盘管理（Storage Spaces）
description: 查看存储池健康状态、虚拟磁盘状态、物理磁盘健康、存储层使用情况，提前预警存储故障。
keywords: ['存储池正常吗', '虚拟磁盘状态', '物理磁盘健康', '存储池容量预警']
permission: admin
mode: readonly
subset: disk-management
---

## 🆕 模块 24：存储池与虚拟磁盘管理（Storage Spaces）


<details>
<summary>📋 展开查看：🆕 模块 24：存储池与虚拟磁盘管理（Storage Spaces）</summary>

**用途**：查看存储池健康状态、虚拟磁盘状态、物理磁盘健康、存储层使用情况，提前预警存储故障。

**常你说**：`"存储池正常吗"` / `"虚拟磁盘状态"` / `"物理磁盘健康"` / `"存储池容量预警"`

> ⚠️ **本模块仅读，不创建/删除/修改任何存储池或虚拟磁盘配置。**


```powershell
Write-Host "════════ 存储池健康状态 ════════"
Get-StoragePool | Where-Object { $_.IsPrimordial -eq $false } |
    Select-Object @{N='名称';E={$_.FriendlyName}},
        @{N='状态';E={$_.HealthStatus}},
        @{N='操作状态';E={$_.OperationalStatus}},
        @{N='物理磁盘数';E={$_.PhysicalDisks.Count}},
        @{N='已用空间';E={[math]::Round($_.AllocatedSize/1GB,1)}},
        @{N='总容量';E={[math]::Round($_.Size/1GB,1)}},
        @{N='使用率';E={[math]::Round(($_.AllocatedSize/$_.Size)*100,1)}} |
    Format-Table -AutoSize
```



```powershell
Write-Host "════════ 虚拟磁盘状态 ════════"
Get-VirtualDisk | Select-Object @{N='名称';E={$_.FriendlyName}},
    @{N='状态';E={$_.HealthStatus}},
    @{N='操作状态';E={$_.OperationalStatus}},
    @{N='RAID类型';E={$_.ResiliencySettingName}},
    @{N='已用空间';E={[math]::Round($_.AllocatedSize/1GB,1)}},
    @{N='总容量';E={[math]::Round($_.Size/1GB,1)}},
    @{N='使用率';E={[math]::Round(($_.AllocatedSize/$_.Size)*100,1)}} |
    Format-Table -AutoSize
```



```powershell
Write-Host "════════ 存储池中物理磁盘健康 ════════"
Get-StoragePool | Where-Object { $_.IsPrimordial -eq $false } |
    Get-PhysicalDisk | Select-Object @{N='磁盘';E={$_.FriendlyName}},
        @{N='状态';E={$_.HealthStatus}},
        @{N='操作状态';E={$_.OperationalStatus}},
        @{N='使用时长(小时)';E={[math]::Round($_.UsageHours,0)}},
        @{N='温度';E={if($_.Temperature){"$($_.Temperature)°C"}else{"-"}}},
        @{N='读取错误';E={(Get-StorageReliabilityCounter -PhysicalDisk $_ -ErrorAction SilentlyContinue).ReadErrorsTotal}} |
    Format-Table -AutoSize
```



```powershell
Write-Host "════════ 存储层使用情况 ════════"
Get-StorageTier | Select-Object @{N='名称';E={$_.FriendlyName}},
    @{N='总容量';E={[math]::Round($_.Size/1GB,1)}},
    @{N='已用';E={[math]::Round(($_.Size - $_.AllocatedSize)/1GB,1)}},
    @{N='媒体类型';E={$_.MediaType}} |
    Format-Table -AutoSize
```


**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `No MSFT_StoragePool objects` | 系统未配置存储池 | 仅适用于 Storage Spaces 环境 |
| `Get-VirtualDisk` 报错 | 需要管理员权限 | 提升执行 |
| `HealthStatus` 显示 `Warning` | 存储池存在降级 | 立即检查物理磁盘 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 存储池状态显示 `Degraded` | 有物理磁盘离线或故障 |
| 虚拟磁盘显示 `Incomplete` | 部分成员磁盘离线，需尽快恢复 |
| 容量使用率 >90% | 需要扩容，否则写入将失败 |
| 物理磁盘 `UsageHours` 异常高 | 磁盘可能过热或长期高负载 |


</details>

[↑ 返回顶部](#module-1)

---

<a name="module-25"></a>

