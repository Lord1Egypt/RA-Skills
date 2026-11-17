---
id: module-22
name: 关键服务崩溃与自动恢复状态
description: 查看服务异常停止记录、自动恢复策略、"应该运行却未运行"的服务。
keywords: ['哪些服务崩过', '服务崩溃记录', '服务自动恢复设置', '有服务没跑起来吗']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 22：关键服务崩溃与自动恢复状态




<details>
<summary>📋 展开查看：🆕 模块 22：关键服务崩溃与自动恢复状态</summary>

**用途**：查看服务异常停止记录、自动恢复策略、"应该运行却未运行"的服务。

**常你说**：`"哪些服务崩过"` / `"服务崩溃记录"` / `"服务自动恢复设置"` / `"有服务没跑起来吗"`

> ⚠️ **本模块仅读，不会启动、停止或修改任何服务。**

### 22.1 已停止但设为自动启动的服务（"应跑未跑"）




```powershell
Write-Host "════════ 应运行却已停止的服务 ════════"
$deadServices = Get-Service | Where-Object {
    $_.StartType -in @('Automatic', 'AutomaticDelayedStart') -and
    $_.Status -eq 'Stopped'
}

if ($deadServices) {
    $deadServices | Select-Object @{N='服务名';E={$_.Name}},
        @{N='显示名';E={$_.DisplayName}},
        @{N='启动类型';E={$_.StartType}},
        @{N='状态';E={$_.Status}} |
        Sort-Object 显示名 |
        Format-Table -AutoSize
    Write-Host "`n⚠️ 以上服务设置了自动启动但当前已停止，需要排查原因"
} else {
    Write-Host "✅ 所有自动启动的服务均在运行"
}
```



### 22.2 服务崩溃事件记录（事件日志 7034/7036）




```powershell
Write-Host "════════ 服务崩溃记录（最近 7 天）════════"
$events = Get-WinEvent -FilterHashtable @{
    LogName   = 'System'
    Id        = @(7034, 7035, 7036, 7031, 7040)
    StartTime = (Get-Date).AddDays(-7)
} -ErrorAction SilentlyContinue

if ($events) {
    $events | Select-Object @{N='时间';E={$_.TimeCreated}},
        @{N='事件ID';E={$_.Id}},
        @{N='说明';E={
            switch ($_.Id) {
                7034 { "❌ 服务意外停止: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(80,$_.Message.Length)) }
                7031 { "❌ 服务停止后触发恢复动作: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                7035 { "→ 服务控制: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                7036 { "● 服务状态变更: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                7040 { "⚙️ 启动类型变更: " + ($_.Message -replace "`r`n",' ').Substring(0,[Math]::Min(60,$_.Message.Length)) }
                default { $_.Message.Substring(0,[Math]::Min(80,$_.Message.Length)) }
            }
        }} |
        Where-Object { $_.事件ID -in @(7034, 7031) } |
        Sort-Object 时间 -Descending |
        Select-Object -First 20 |
        Format-Table -AutoSize -Wrap
} else {
    Write-Host "✅ 最近 7 天无服务崩溃记录"
}
```



### 22.3 服务自动恢复策略查看




```powershell
Write-Host "════════ 关键服务恢复策略 ════════"
$keyServices = @(
    'W3SVC',       # IIS
    'MSSQLSERVER', # SQL Server
    'WSearch',     # Windows Search
    'Spooler',     # 打印机
    'EventLog',    # 事件日志
    'WinRM',       # 远程管理
    'Schedule',    # 计划任务
    'LanmanServer' # 文件共享
)

foreach ($svcName in $keyServices) {
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if ($svc) {
        # 使用 sc.exe 读取恢复策略
        $scOutput = sc.exe qfailure $svcName 2>&1
        $resetPeriod = ($scOutput | Select-String 'RESET_PERIOD') -replace '.*: ', ''
        $actions = ($scOutput | Select-String 'FAILURE_ACTIONS') -replace '.*: ', ''

        Write-Host "  $($svc.DisplayName) [$svcName]"
        Write-Host "    状态: $($svc.Status)"
        Write-Host "    恢复动作: $(if($actions){$actions}else{'(未配置)'} )"
        Write-Host ""
    }
}
Write-Host "💡 未配置恢复动作的关键服务，崩溃后不会自动重启，需手动干预"
```



### 22.4 服务依赖关系检查（关键服务是否有依赖未启动）




```powershell
Write-Host "════════ 关键服务依赖链检查 ════════"
$keyServices = @('W3SVC', 'MSSQLSERVER', 'WinRM', 'Schedule', 'Netlogon')

foreach ($svcName in $keyServices) {
    $svc = Get-Service -Name $svcName -ErrorAction SilentlyContinue
    if ($svc) {
        $deps = $svc.ServicesDependedOn
        $brokenDeps = $deps | Where-Object { $_.Status -ne 'Running' }

        if ($brokenDeps) {
            Write-Host "⚠️ $($svc.DisplayName) 依赖以下未运行的服务:"
            $brokenDeps | ForEach-Object {
                Write-Host "    ❌ $($_.Name) ($($_.Status))"
            }
        } else {
            Write-Host "✅ $($svc.DisplayName) — 所有依赖服务正常"
        }
    }
}
```



**风险等级**：🟢 无（只读，不启动/停止/修改任何服务）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-WinEvent` 无权限 | 需管理员权限 | 管理员身份执行 |
| `sc.exe qfailure` 返回空 | 部分服务无恢复策略 | 正常，说明未配置 |
| `Get-Service` 找不到服务 | 该服务未安装 | 跳过该服务 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| IIS 停止但事件日志无崩溃记录 | 可能是被人为停止 |
| 服务崩溃但无恢复动作 | 需通过"服务属性 → 恢复"配置自动重启 |
| 依赖服务未运行导致主服务无法启动 | 先启动依赖服务 |
| 事件 7034 大量重复 | 服务反复崩溃重启，存在底层问题 |



---


</details>

[↑ 返回顶部](#module-1)

---

<a name="module-23"></a>

