---
id: module-13
name: 网络连接与端口监控
description: 检测异常网络连接、监听端口、可疑外连行为。
keywords: ['谁在连我的服务器', '有没有异常外连', '检查监听端口']
permission: admin
mode: readonly
subset: network-security
---

## 🆕 模块 13：网络连接与端口监控




<details>
<summary>📋 展开查看：🆕 模块 13：网络连接与端口监控</summary>

**用途**：检测异常网络连接、监听端口、可疑外连行为。

**常你说**：`"谁在连我的服务器"` / `"有没有异常外连"` / `"检查监听端口"`

> ⚠️ **本模块所有操作均为只读检测，不会修改防火墙规则或终止连接。**

### 13.1 活动网络连接概览




```powershell
Write-Host "════════ 活动网络连接 ════════"
Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue |
    Select-Object @{N='本地地址';E={$_.LocalAddress}},
        @{N='本地端口';E={$_.LocalPort}},
        @{N='远程地址';E={$_.RemoteAddress}},
        @{N='远程端口';E={$_.RemotePort}},
        @{N='状态';E={$_.State}},
        @{N='进程';E={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).Name}} |
    Sort-Object RemoteAddress |
    Format-Table -AutoSize
```



### 13.2 监听端口审计




```powershell
Write-Host "════════ 监听端口列表 ════════"
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Select-Object @{N='本地地址';E={$_.LocalAddress}},
        @{N='监听端口';E={$_.LocalPort}},
        @{N='进程';E={
            $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
            if ($proc) { "$($proc.Name) (PID: $($proc.Id))" } else { "未知" }
        }} |
    Sort-Object LocalPort |
    Format-Table -AutoSize
```



### 13.3 可疑外连检测（高频连接分析）




```powershell
Write-Host "════════ 高频外连目标 ════════"
Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue |
    Group-Object RemoteAddress |
    Where-Object { $_.Count -gt 5 } |
    Sort-Object Count -Descending |
    Select-Object -First 15 @{N='远程IP';E={$_.Name}},
        @{N='连接数';E={$_.Count}},
        @{N='进程';E={
            $proc = Get-Process -Id ($_.Group[0].OwningProcess) -ErrorAction SilentlyContinue
            if ($proc) { $proc.Name } else { "未知" }
        }} |
    Format-Table -AutoSize

Write-Host "`n  💡 连接数 >20 的 IP 需重点排查是否为恶意外连"
```



### 13.4 防火墙规则审计




```powershell
Write-Host "════════ 防火墙入站规则 ════════"
Get-NetFirewallRule -Direction Inbound -Enabled True -ErrorAction SilentlyContinue |
    Where-Object { $_.Action -eq 'Allow' } |
    Select-Object @{N='规则名';E={$_.DisplayName}},
        @{N='操作';E={$_.Action}},
        @{N='本地端口';E={$_.LocalPort}},
        @{N='远程地址';E={$_.RemoteAddress}} |
    Format-Table -AutoSize
```



**风险等级**：🟢 无（只读检测）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-NetTCPConnection` 报错 | 需要管理员权限 | 提升执行 |
| `Get-NetFirewallRule` 报错 | 防火墙服务未启动 | 检查 mpssvc 服务 |
| `OwningProcess` 为 0 | 系统进程，正常 | 无需处理 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 未知进程监听 80/443 端口 | 可能是 Web 服务或恶意软件，需排查 |
| 大量外连到同一 IP | 可能是 C2 通信，立即断网排查 |
| 防火墙规则异常宽松 | 建议收紧为最小权限原则 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-14"></a>

