---
id: module-16
name: 用户会话与登录状态监控
description: 监控当前登录的用户、远程会话、僵尸会话、账户状态。
keywords: ['谁在服务器上', '有没有异常登录', '查看远程会话']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 16：用户会话与登录状态监控




<details>
<summary>📋 展开查看：🆕 模块 16：用户会话与登录状态监控</summary>

**用途**：监控当前登录的用户、远程会话、僵尸会话、账户状态。

**常你说**：`"谁在服务器上"` / `"有没有异常登录"` / `"查看远程会话"`

> ⚠️ **本模块仅读，不会结束会话、锁定账户或修改密码策略。**

### 16.1 当前登录用户概览




```powershell
Write-Host "════════ 当前登录用户 ════════"
Get-CimInstance Win32_LogonSession | Where-Object { $_.LogonType -ne 0 } |
    Select-Object @{N='用户名';E={
        $user = Get-CimInstance Win32_ComputerSystem | Select-Object UserName
        $user.UserName ?? "未知"
    }},
    @{N='会话ID';E={$_.LogonId}},
    @{N='登录类型';E={
        switch ($_.LogonType) {
            2 {'交互 (本地登录)'}
            3 {'网络登录'}
            4 {'批处理'}
            5 {'服务'}
            7 {'解锁'}
            8 {'网络明文'}
            9 {'新凭据'}
            10 {'远程交互 (RDP)'}
            11 {'缓存交互'}
            default {"其他 ($($_.LogonType))"}
        }
    }},
    @{N='登录时间';E={$_.StartTime}} |
    Format-Table -AutoSize
```



### 16.2 远程桌面会话监控




```powershell
Write-Host "════════ 远程桌面会话 (RDP) ════════"
Get-CimInstance Win32_LogonSession | Where-Object { $_.LogonType -eq 10 } |
    Select-Object @{N='用户名';E={
        $user = Get-CimInstance Win32_ComputerSystem | Select-Object UserName
        $user.UserName ?? "未知"
    }},
    @{N='会话ID';E={$_.LogonId}},
    @{N='登录时间';E={$_.StartTime}},
    @{N='空闲时间(分钟)';E={
        if ($_.StartTime) {
            [math]::Round(((Get-Date) - $_.StartTime).TotalMinutes, 0)
        } else { 0 }
    }} |
    Format-Table -AutoSize
Write-Host "`n💡 空闲 >60 分钟的会话可能为僵尸会话"
```



### 16.3 异常登录检测（多 IP / 异地登录）




```powershell
Write-Host "════════ 最近 7 天的登录来源 ════════"
Get-WinEvent -FilterHashtable @{
    LogName='Security';
    ID=4624;
    StartTime=(Get-Date).AddDays(-7)
} -ErrorAction SilentlyContinue |
    Where-Object { $_.Properties[18].Value -ne '-' } |
    Select-Object @{N='登录时间';E={$_.TimeCreated}},
        @{N='用户名';E={$_.Properties[5].Value}},
        @{N='来源IP';E={$_.Properties[18].Value}},
        @{N='登录类型';E={
            switch ($_.Properties[8].Value) {
                2 {'交互(本地)'}
                3 {'网络'}
                10 {'远程(RDP)'}
                default {"其他"}
            }
        }} |
    Group-Object SourceIP |
    Sort-Object Count -Descending |
    Select-Object -First 10 @{N='来源IP';E={$_.Name}},
        @{N='登录次数';E={$_.Count}},
        @{N='最近登录';E={$_.Group[0].TimeCreated}} |
    Format-Table -AutoSize

Write-Host "`n💡 任何未知来源IP 的登录都值得警惕"
```



### 16.4 系统账户状态检查




```powershell
Write-Host "════════ 本地用户账户状态 ════════"
Get-LocalUser | Where-Object { $_.Enabled -eq $true } |
    Select-Object @{N='账户名';E={$_.Name}},
        @{N='状态';E={if ($_.Enabled) {'启用'}else{'禁用'}}},
        @{N='最后登录';E={$_.LastLogon}},
        @{N='密码过期';E={
            if ($_.PasswordExpires) { $_.PasswordExpires } else { '永不过期 ⚠️' }
        }},
        @{N='需要密码';E={if ($_.PasswordRequired) {'是'}else{'否 ⚠️'}}} |
    Format-Table -AutoSize

Write-Host "`n⚠️ 标记的账户存在安全风险：无密码或密码永不过期"
```



**风险等级**：🟢 无（只读监控）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-LocalUser` 报错 | 需要管理员权限 | 管理员身份执行 |
| `Get-CimInstance` 报错 | WMI 未启动 | 检查 Winmgmt |
| `No events found` | 没有相关日志 | 正常 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 多个 RDP 会话来自同一 IP | 可能正常（NAT），也可能为多人共用账户 |
| Guest 账户启用 | 不必要的安全风险，建议禁用 |
| 僵尸 RDP 会话 | 占用资源，闲置超时后应自动断开 |
| 密码永不过期 | 合规风险，建议设置密码策略 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-17"></a>

