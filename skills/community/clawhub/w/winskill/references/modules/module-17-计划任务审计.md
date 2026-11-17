---
id: module-17
name: 计划任务审计
description: 审计所有计划任务，检测可疑的持久化行为（恶意软件常用的自启动方式）。
keywords: ['有没有可疑计划任务', '检查计划任务', '有没有凌晨执行的任务']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 17：计划任务审计




<details>
<summary>📋 展开查看：🆕 模块 17：计划任务审计</summary>

**用途**：审计所有计划任务，检测可疑的持久化行为（恶意软件常用的自启动方式）。

**常你说**：`"有没有可疑计划任务"` / `"检查计划任务"` / `"有没有凌晨执行的任务"`

> ⚠️ **本模块仅读，不会创建/删除/修改任何计划任务。**

### 17.1 所有计划任务清单




```powershell
Write-Host "════════ 所有计划任务 ════════"
$tasks = Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' }
$total = ($tasks | Measure-Object).Count
Write-Host "  总数: $total 个启用的任务`n"

$tasks | Select-Object @{N='任务名';E={$_.TaskName}},
    @{N='路径';E={$_.TaskPath}},
    @{N='状态';E={$_.State}},
    @{N='触发器';E={
        $info = Get-ScheduledTaskInfo -TaskName $_.TaskName -TaskPath $_.TaskPath -ErrorAction SilentlyContinue
        if ($info.LastRunTime) { "上次: $($info.LastRunTime)" } else { "从未执行" }
    }} |
    Sort-Object TaskPath, TaskName |
    Format-Table -AutoSize
```



### 17.2 异常计划任务检测（凌晨执行 / 隐藏窗口 / 临时目录）




```powershell
Write-Host "════════ 异常计划任务检测 ════════"
$suspicious = @()
$tasks = Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' }

foreach ($task in $tasks) {
    $score = 0
    $reasons = @()
    $taskInfo = Get-ScheduledTaskInfo -TaskName $task.TaskName -TaskPath $task.TaskPath -ErrorAction SilentlyContinue
    $lastRun = if ($taskInfo.LastRunTime) { $taskInfo.LastRunTime } else { $null }

    # 检测1: 凌晨执行 (0:00-5:00)
    # 通过检查 Actions 中的命令行参数
    $actions = $task.Actions
    foreach ($action in $actions) {
        $argStr = "$($action.Arguments)" + "$($action.Execute)"
        if ($argStr -match '(-WindowStyle\s+Hidden|/hidden|-w\s+hidden|-hide|/background|/min|-NoLogo\s+-NonInteractive\s+-WindowStyle\s+Hidden)') {
            $score += 2
            $reasons += "隐藏窗口执行"
        }
        if ($argStr -match '(\\Temp\\|\\TMP\\|\\AppData\\Local\\Temp\\)') {
            $score += 3
            $reasons += "从临时目录执行"
        }
        if ($argStr -match '((?:powershell|cmd|wscript|cscript|rundll32|mshta|regsvr32).*?(?:-enc|-e\s|IEX|Invoke-Expression|DownloadString|FromBase64String|eval))') {
            $score += 4
            $reasons += "可疑命令特征(编码/下载)"
        }
    }

    # 检测2: 无描述信息的任务
    if (-not $task.Description -or $task.Description -eq '') {
        $score += 1
        $reasons += "无描述信息"
    }

    if ($score -ge 3) {
        $suspicious += [PSCustomObject]@{
            任务名 = $task.TaskName
            路径 = $task.TaskPath
            风险分 = $score
            原因 = ($reasons -join ', ')
            上次运行 = $lastRun
        }
    }
}

if ($suspicious.Count -gt 0) {
    $suspicious | Sort-Object 风险分 -Descending |
        Format-Table -AutoSize -Wrap
    Write-Host "`n🔴 以上任务存在可疑特征，建议逐条排查"
} else {
    Write-Host "✅ 未发现明显可疑的计划任务"
}
```



### 17.3 按触发条件分类（开机自启 / 定时 / 用户登录触发）




```powershell
Write-Host "════════ 计划任务按触发类型分类 ════════`n"

# 开机自启
Write-Host "═══ 开机/系统启动时触发 ═══"
Get-ScheduledTask | Where-Object {
    $_.Triggers | Where-Object { $_.CimClass.CimClassName -match 'BootTrigger|StartupTrigger' }
} | Select-Object -First 15 @{N='任务名';E={$_.TaskName}},
    @{N='路径';E={$_.TaskPath}},
    @{N='触发器';E={
        ($_.Triggers | ForEach-Object { $_.CimClass.CimClassName }) -join ', '
    }} |
    Format-Table -AutoSize

Write-Host "`n═══ 用户登录时触发 ═══"
Get-ScheduledTask | Where-Object {
    $_.Triggers | Where-Object { $_.CimClass.CimClassName -match 'LogonTrigger' }
} | Select-Object -First 15 @{N='任务名';E={$_.TaskName}},
    @{N='路径';E={$_.TaskPath}},
    @{N='触发器';E={
        ($_.Triggers | ForEach-Object { $_.CimClass.CimClassName }) -join ', '
    }} |
    Format-Table -AutoSize

Write-Host "`n═══ 定时/周期性触发 (数量最多) ═══"
$timeTasks = Get-ScheduledTask | Where-Object {
    $_.Triggers | Where-Object { $_.CimClass.CimClassName -match 'TimeTrigger|DailyTrigger|WeeklyTrigger|MonthlyTrigger' }
}
Write-Host "  总数: $(($timeTasks | Measure-Object).Count) 个"
```



### 17.4 非 Microsoft 创建的任务




```powershell
Write-Host "════════ 非 Microsoft 创建的计划任务 ════════"
$nonMsTasks = Get-ScheduledTask | Where-Object {
    $_.TaskPath -notmatch '\\\\Microsoft\\\\' -and $_.State -ne 'Disabled'
}

if ($nonMsTasks) {
    $nonMsTasks | Select-Object @{N='任务名';E={$_.TaskName}},
        @{N='路径';E={$_.TaskPath}},
        @{N='状态';E={$_.State}},
        @{N='描述';E={
            if ($_.Description) { $_.Description.Substring(0, [Math]::Min(60, $_.Description.Length)) }
            else { '(无描述)' }
        }} |
        Format-Table -AutoSize
    Write-Host "`n💡 第三方任务值得审查，尤其是无描述且来源不明的"
} else {
    Write-Host "✅ 无非 Microsoft 计划任务"
}
```



**风险等级**：🟢 无（只读审计）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access denied` | 权限不足 | 管理员身份执行 |
| `The system cannot find the file specified` | 任务引用的程序已删除 | 正常（残留任务），值得清理 |
| `Task Scheduler service is not running` | 计划任务服务未启动 | `Start-Service Schedule` |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 大量凌晨执行的隐藏窗口任务 | 软件更新常见，但需逐条确认来源 |
| 从 Temp 目录执行的任务 | 高危特征，多数恶意软件行为 |
| 无描述的随机名任务 | 可能是病毒/蠕虫创建，建议隔离排查 |
| 编码命令 (Base64) 执行 | 极高风险，常见于挖矿脚本和外连木马 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-18"></a>

