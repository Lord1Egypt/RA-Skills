---
id: module-11
name: 注册表与启动项安全审计
description: 检测恶意持久化机制（注册表自启动、计划任务、WMI 订阅）。
keywords: ['有没有可疑的自启动程序', '检查一下持久化威胁']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 11：注册表与启动项安全审计




<details>
<summary>📋 展开查看：🆕 模块 11：注册表与启动项安全审计</summary>

**用途**：检测恶意持久化机制（注册表自启动、计划任务、WMI 订阅）。

**常你说**：`"有没有可疑的自启动程序"` / `"检查一下持久化威胁"`

> ⚠️ **本模块所有操作均为只读分析，绝不修改注册表或删除任何键值。**

### 11.1 经典自启动注册表位置扫描




```powershell
$runKeys = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"
)

Write-Host "════════ 自启动注册表项 ════════"
foreach ($key in $runKeys) {
    if (Test-Path $key) {
        Write-Host "`n  📁 $($key.Split('\')[-1..-1] -join '\')"
        Get-ItemProperty $key -ErrorAction SilentlyContinue |
            Get-Member -MemberType NoteProperty |
            Where-Object { $_.Name -notlike 'PS*' } |
            ForEach-Object {
                $val = (Get-ItemProperty $key -Name $_.Name -ErrorAction SilentlyContinue).$($_.Name)
                Write-Host "    🔹 $($_.Name) = $val"
            }
    }
}
Write-Host "`n═══════════════════════════════"
Write-Host "  💡 不认识的程序请搜索确认，不要直接删除"
```



### 11.2 计划任务审计




```powershell
Write-Host "════════ 计划任务列表 ════════"
Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' } |
    Select-Object @{N='任务名';E={$_.TaskName}},
        @{N='状态';E={$_.State}},
        @{N='作者';E={$_.Author}},
        @{N='运行方式';E={$_.Principal.UserId}} |
    Format-Table -AutoSize

Write-Host "`n════════ 最近修改的任务 ════════"
Get-ScheduledTask | Sort-Object LastWriteTime -Descending |
    Select-Object -First 10 @{N='任务名';E={$_.TaskName}},
        @{N='修改时间';E={$_.LastWriteTime}} |
    Format-Table -AutoSize
```



### 11.3 WMI 持久化检测




```powershell
Write-Host "════════ WMI 事件订阅 ════════"
try {
    $wmiSubs = Get-CimInstance -Namespace root\subscription -ClassName __EventFilter -ErrorAction SilentlyContinue
    if ($wmiSubs) {
        $wmiSubs | Select-Object @{N='名称';E={$_.Name}},
            @{N='查询';E={$_.Query}} |
            Format-Table -AutoSize
    } else {
        Write-Host "  ✅ 未发现 WMI 事件订阅"
    }
} catch {
    Write-Host "  ⚠️ WMI 查询失败，可能需要管理员权限"
}
```



### 11.4 系统服务异常检测




```powershell
Write-Host "════════ 非微软服务列表 ════════"
Get-Service | Where-Object {
    $_.DisplayName -notlike '*Microsoft*' -and
    $_.DisplayName -notlike '*Windows*' -and
    $_.DisplayName -notlike '*Intel*' -and
    $_.DisplayName -notlike '*NVIDIA*' -and
    $_.DisplayName -notlike '*AMD*' -and
    $_.DisplayName -notlike '*Realtek*' -and
    $_.DisplayName -notlike '*HP*' -and
    $_.DisplayName -notlike '*Dell*'
} | Select-Object @{N='服务名';E={$_.Name}},
    @{N='显示名';E={$_.DisplayName}},
    @{N='状态';E={$_.Status}},
    @{N='启动类型';E={$_.StartType}} |
    Format-Table -AutoSize
```



**风险等级**：🟢 无（只读审计）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access to the path is denied` | 权限不足 | 管理员身份运行 |
| `Requested registry access is not allowed` | 注册表权限限制 | 提升权限执行 |
| `Get-CimInstance` 报错 | WMI 服务未启动 | 检查 Winmgmt 服务 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| Run 键值超多（>20个） | 正常软件也会注册，重点排查不认识的 |
| WMI 订阅存在未知项 | 可能是恶意软件持久化，需进一步分析 |
| 服务名随机字符串 | 典型恶意软件特征，需立即排查 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-12"></a>

