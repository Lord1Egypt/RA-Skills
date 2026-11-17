---
id: module-21
name: Windows 防火墙规则审计
description: 列出所有防火墙规则，识别过度开放（Any/Any）、可疑来源的规则，找出安全漏洞。
keywords: ['防火墙规则有没有问题', '防火墙审计', '哪些端口对外开放', '有没有高危防火墙规则']
permission: admin
mode: readonly
subset: network-security
---

## 🆕 模块 21：Windows 防火墙规则审计




<details>
<summary>📋 展开查看：🆕 模块 21：Windows 防火墙规则审计</summary>

**用途**：列出所有防火墙规则，识别过度开放（Any/Any）、可疑来源的规则，找出安全漏洞。

**常你说**：`"防火墙规则有没有问题"` / `"防火墙审计"` / `"哪些端口对外开放"` / `"有没有高危防火墙规则"`

> ⚠️ **本模块仅读，不会新增、删除或修改任何防火墙规则。**

### 21.1 所有入站规则概览




```powershell
Write-Host "════════ 入站防火墙规则（启用中）════════"
$inbound = Get-NetFirewallRule -Direction Inbound -Enabled True -ErrorAction SilentlyContinue

Write-Host "  启用的入站规则总数: $(($inbound | Measure-Object).Count)"
Write-Host ""

$inbound | ForEach-Object {
    $rule = $_
    $filter = $rule | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
    $addrFilter = $rule | Get-NetFirewallAddressFilter -ErrorAction SilentlyContinue
    [PSCustomObject]@{
        规则名     = $rule.DisplayName.Substring(0, [Math]::Min(40, $rule.DisplayName.Length))
        协议       = if ($filter.Protocol) { $filter.Protocol } else { '任意' }
        本地端口   = if ($filter.LocalPort) { $filter.LocalPort -join ',' } else { '任意' }
        来源地址   = if ($addrFilter.RemoteAddress) { ($addrFilter.RemoteAddress -join ',').Substring(0, [Math]::Min(30, ($addrFilter.RemoteAddress -join ',').Length)) } else { '任意' }
        动作       = $rule.Action
    }
} | Select-Object -First 30 | Format-Table -AutoSize
```



### 21.2 高危规则检测（Any → Any / 暴露全端口）




```powershell
Write-Host "════════ 高危防火墙规则扫描 ════════"
$risks = @()

Get-NetFirewallRule -Direction Inbound -Action Allow -Enabled True -ErrorAction SilentlyContinue | ForEach-Object {
    $rule = $_
    $portFilter = $rule | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
    $addrFilter  = $rule | Get-NetFirewallAddressFilter -ErrorAction SilentlyContinue

    $anyPort = ($portFilter.LocalPort -eq 'Any' -or -not $portFilter.LocalPort)
    $anyAddr = ($addrFilter.RemoteAddress -eq 'Any' -or $addrFilter.RemoteAddress -contains 'Any' -or -not $addrFilter.RemoteAddress)

    if ($anyPort -and $anyAddr) {
        $risks += [PSCustomObject]@{
            风险等级 = '🔴 高危'
            规则名   = $rule.DisplayName
            说明     = '允许任意来源访问任意端口'
            建议     = '收紧来源地址或端口范围'
        }
    } elseif ($anyAddr) {
        # 检查是否暴露高危端口（135/445/3389/5985）
        $dangerousPorts = @('135','445','3389','5985','5986','23','21','1433','3306','6379')
        $portStr = ($portFilter.LocalPort -join ',')
        foreach ($p in $dangerousPorts) {
            if ($portStr -match "\b$p\b" -or $anyPort) {
                $risks += [PSCustomObject]@{
                    风险等级 = '⚠️ 中危'
                    规则名   = $rule.DisplayName
                    说明     = "端口 $p 对任意来源开放"
                    建议     = '限制来源 IP 白名单'
                }
                break
            }
        }
    }
}

if ($risks.Count -gt 0) {
    $risks | Format-Table -AutoSize -Wrap
    Write-Host "`n建议: 使用「来源 IP 白名单」替代「任意来源」"
} else {
    Write-Host "✅ 未发现明显高危防火墙规则"
}
```



### 21.3 按端口查看谁在放行




```powershell
# 修改此处为你想查询的端口
$targetPorts = @('3389', '445', '80', '443', '1433', '3306')

Write-Host "════════ 关键端口放行规则 ════════"
foreach ($port in $targetPorts) {
    $rules = Get-NetFirewallRule -Direction Inbound -Action Allow -Enabled True -ErrorAction SilentlyContinue | Where-Object {
        $pf = $_ | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
        ($pf.LocalPort -eq 'Any' -or $pf.LocalPort -contains $port)
    }

    if ($rules) {
        Write-Host "`n  端口 $port — 有 $(($rules | Measure-Object).Count) 条放行规则:"
        $rules | Select-Object -First 5 @{N='规则名';E={$_.DisplayName}} |
            ForEach-Object { Write-Host "    - $($_.规则名)" }
    } else {
        Write-Host "`n  端口 $port — 无放行规则（默认拒绝）"
    }
}
```



### 21.4 防火墙配置文件状态




```powershell
Write-Host "════════ 防火墙配置文件状态 ════════"
Get-NetFirewallProfile | Select-Object @{N='配置文件';E={$_.Name}},
    @{N='是否启用';E={if($_.Enabled){'✅ 启用'}else{'❌ 已禁用 ⚠️'}}},
    @{N='入站默认';E={$_.DefaultInboundAction}},
    @{N='出站默认';E={$_.DefaultOutboundAction}},
    @{N='通知';E={$_.NotifyOnListen}} |
    Format-Table -AutoSize

Write-Host "`n💡 防火墙应对所有配置文件均启用，入站默认「Block」"
Write-Host "💡 如果任一配置文件显示「已禁用」，立即排查原因"
```



**风险等级**：🟢 无（只读审计，不修改任何规则）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-NetFirewallRule` 报错 | 需管理员权限 | 管理员身份执行 |
| `WinRM` 相关报错 | 防火墙服务异常 | 检查 `mpssvc` 服务状态 |
| `Access denied on Get-NetFirewallPortFilter` | 域策略限制 | 以域管理员身份执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 防火墙被关闭（Enabled=False） | 极高风险，任何连接均可进入 |
| 3389 对 Any 开放 | RDP 暴力破解首要目标 |
| 445 对 Any 开放 | WannaCry/勒索病毒入侵路径 |
| 大量"Any → Any"规则 | 常见于软件安装时自动添加，需逐条清理 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-22"></a>

