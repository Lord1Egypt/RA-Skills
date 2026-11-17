---
id: module-10
name: 安全审计与日志分析
description: 检测暴力破解、特权操作、异常登录。
keywords: ['帮我查下有没有被入侵', '有没有异常登录记录']
permission: admin
mode: readonly
subset: performance
---

## 🆕 模块 10：安全审计与日志分析




<details>
<summary>📋 展开查看：🆕 模块 10：安全审计与日志分析</summary>

**用途**：检测暴力破解、特权操作、异常登录。

**常你说**：`"帮我查下有没有被入侵"` / `"有没有异常登录记录"`

### 10.1 检测暴力破解尝试（最近 24 小时）




```powershell
$since = (Get-Date).AddHours(-24)

$failedLogins = Get-WinEvent -FilterHashtable @{
    LogName='Security'; ID=4625; StartTime=$since
} -ErrorAction SilentlyContinue

if ($failedLogins) {
    Write-Host "⚠️ 最近 24h 失败登录 $($failedLogins.Count) 次`n"
    $failedLogins |
        Select-Object TimeCreated,
            @{N='账号';E={$_.Properties[5].Value}},
            @{N='来源IP';E={$_.Properties[19].Value}} |
        Group-Object SourceIP |
        Sort-Object Count -Descending |
        Select-Object -First 10 @{N='攻击源IP';E={$_.Name}},
            @{N='尝试次数';E={$_.Count}} |
        Format-Table -AutoSize
    Write-Host "  💡 尝试次数 >10 的 IP 建议加入防火墙黑名单"
} else {
    Write-Host "  ✅ 最近 24 小时无失败登录记录"
}
```



### 10.2 查看特权提升操作（管理员操作审计）




```powershell
$since = (Get-Date).AddHours(-24)

Write-Host "════════ 特权操作（4672）════════"
Get-WinEvent -FilterHashtable @{
    LogName='Security'; ID=4672; StartTime=$since
} -ErrorAction SilentlyContinue |
    Select-Object TimeCreated,
        @{N='用户';E={$_.Properties[1].Value}},
        @{N='特权';E={$_.Properties[2..($_.Properties.Count-1)].Value -join ', '}} |
    Format-Table -AutoSize
```



### 10.3 本地管理员组成员检查




```powershell
Write-Host "════════ 本地管理员组成员 ════════"
Get-LocalGroupMember -Group "Administrators" |
    Select-Object @{N='用户名';E={$_.Name}},
        @{N='来源';E={$_.PrincipalSource}} |
    Format-Table -AutoSize
```






```powershell
# ⚠️ 仅当用户明确说「确认导出」后才执行！
# $logPath = "C:\Logs\Security_$(Get-Date -Format 'yyyyMMdd').evtx"
# if (-not (Test-Path "C:\Logs")) { New-Item -ItemType Directory -Path "C:\Logs" -Force }
# wevtutil epl Security $logPath
# Write-Host "  ✅ 安全日志已导出到: $logPath"
```



**风险等级**：🟢 只读审计 / 🟡 导出需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `No events were found ...` | 没有符合条件的日志 | 正常，说明期间无异常 |
| `The requested operation cannot be performed on a file ...` | 日志文件被占用 | 复制到另一路径导出 |
| `Get-LocalGroupMember` 报错 | 需要管理员权限 | 提升执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 某 IP 失败登录 >100 次 | 暴力破解，建议防火墙封禁 |
| 4672 事件频繁 | 有人在频繁执行管理员操作，需排查 |
| 管理员组成员异常多了不认识账号 | 立即排查是否被入侵后留后门，删非法账号 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-11"></a>

