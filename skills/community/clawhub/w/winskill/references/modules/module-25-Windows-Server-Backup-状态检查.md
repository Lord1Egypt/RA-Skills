---
id: module-25
name: Windows Server Backup 状态检查
description: 检查 Windows Server Backup 配置、最近备份状态、备份目标健康，确保备份作业正常运行。
keywords: ['备份正常吗', '上次备份时间', '备份失败了', '恢复点检查']
permission: user
mode: readonly
subset: basic
---

## 🆕 模块 25：Windows Server Backup 状态检查


<details>
<summary>📋 展开查看：🆕 模块 25：Windows Server Backup 状态检查</summary>

**用途**：检查 Windows Server Backup 配置、最近备份状态、备份目标健康，确保备份作业正常运行。

**常你说**：`"备份正常吗"` / `"上次备份时间"` / `"备份失败了"` / `"恢复点检查"`

> ⚠️ **本模块仅读，不会启动、停止或配置任何备份任务。**


```powershell
Write-Host "════════ Windows Server Backup 状态 ════════"

# 检查备份策略
try {
    $policy = Get-WBPolicy -ErrorAction Stop
    Write-Host "  ✅ 备份策略已配置"
    Write-Host "  备份目标: $($policy.BackupTargets | ForEach-Object { $_.Path })"
    Write-Host "  包含卷: $($policy.VolumesToBackup | ForEach-Object { $_.Path })"
} catch {
    Write-Host "  ⚠️ 未配置备份策略"
}

# 查看最近备份
Write-Host "`n════════ 最近备份历史 ════════"
$backups = Get-WBSummary -ErrorAction SilentlyContinue
if ($backups) {
    $backups | Select-Object @{N='最后备份时间';E={$_.LastBackupTime}},
        @{N='备份大小';E={[math]::Round($_.TotalBackupSize/1GB,2)}},
        @{N='状态';E={if($_.LastBackupTime){"✅ 成功"}else{"❌ 无记录"}}} |
        Format-Table -AutoSize
} else {
    Write-Host "  ⚠️ 没有备份历史记录"
}
```



```powershell
Write-Host "════════ 备份目标磁盘检查 ════════"
$policy = Get-WBPolicy -ErrorAction SilentlyContinue
if ($policy -and $policy.BackupTargets.Count -gt 0) {
    foreach ($target in $policy.BackupTargets) {
        $targetPath = $target.Path
        $vol = Get-Volume -FilePath $targetPath -ErrorAction SilentlyContinue
        if ($vol) {
            $freeGB = [math]::Round($vol.SizeRemaining/1GB,1)
            $totalGB = [math]::Round($vol.Size/1GB,1)
            $pctFree = [math]::Round(($vol.SizeRemaining/$vol.Size)*100,1)
            Write-Host "  目标: $targetPath"
            Write-Host "  容量: ${totalGB} GB  剩余: ${freeGB} GB (${pctFree}%)"
            if ($pctFree -lt 10) {
                Write-Host "  ⚠️ 备份目标即将写满！"
            }
        }
    }
} else {
    Write-Host "  ⚠️ 未配置备份目标"
}
```



```powershell
Write-Host "════════ 可用还原点 ════════"
Get-WBBackupSet -ErrorAction SilentlyContinue | Sort-Object BackupTime -Descending |
    Select-Object -First 10 @{N='备份时间';E={$_.BackupTime}},
        @{N='备份大小(GB)';E={[math]::Round($_.TotalBackupSize/1GB,2)}},
        @{N='卷数';E={$_.Volumes.Count}},
        @{N='应用一致性';E={if($_.ApplicationConsistent){"✅"}else{"-"}}} |
    Format-Table -AutoSize
```



```powershell
Write-Host "════════ 当前备份作业状态 ════════"
$job = Get-WBJob -ErrorAction SilentlyContinue
if ($job) {
    Write-Host "  状态: $($job.JobState)"
    Write-Host "  当前操作: $($job.CurrentOperation)"
    Write-Host "  进度: $($job.Progress)%"
} else {
    Write-Host "  ✅ 当前无备份作业运行"
}
```


**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-WBPolicy` 报错 | Windows Server Backup 功能未安装 | `Install-WindowsFeature Windows-Server-Backup` |
| `Get-WBSummary` 返回空 | 无备份历史 | 先配置并运行一次备份 |
| `The operation is not supported` | 非 Server 版本 | 仅适用于 Windows Server |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 备份目标剩余 <10% | 备份将失败，需清理或扩容 |
| 备份作业状态显示 `Running` 但长时间无进度 | 可能卡住，检查日志 |
| 应用一致性为 `false` | VSS 卷影复制失败，检查 VSS 服务 |
| 无可用还原点 | 备份从未成功，需排查 |

</details>





[↑ 返回顶部](#module-1)

---

<a name="module-26"></a>

