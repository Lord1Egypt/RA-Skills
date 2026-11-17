---
id: module-19
name: DNS 解析与网卡诊断
description: DNS 缓存查看与清空、解析链路测试、网卡 IP 配置、路由表检查。
keywords: ['DNS 解析正常吗', '网卡配置', '网络诊断', '路由表']
permission: user
mode: readonly
subset: network-security
---

## 🆕 模块 19：DNS 解析与网卡诊断




<details>
<summary>📋 展开查看：🆕 模块 19：DNS 解析与网卡诊断</summary>

**用途**：DNS 缓存查看与清空、解析链路测试、网卡 IP 配置、路由表检查。

**常你说**：`"DNS 解析正常吗"` / `"网卡配置"` / `"网络诊断"` / `"路由表"`

> ⚠️ **本模块操作：DNS 缓存查看/清空（可恢复）+ 网卡 IP 查看（只读）。DNS 清空后会重新从服务器获取，非破坏性。**

### 19.1 DNS 缓存与解析测试




```powershell
Write-Host "════════ DNS 缓存 ════════"
$dnsCache = Get-DnsClientCache -ErrorAction SilentlyContinue
if ($dnsCache) {
    Write-Host "  缓存条目: $(($dnsCache | Measure-Object).Count)"
    $dnsCache | Select-Object -First 20 @{N='域名';E={$_.Entry}},
        @{N='类型';E={$_.RecordType}},
        @{N='IP地址';E={$_.Data}},
        @{N='TTL(秒)';E={$_.TimeToLive}} |
        Format-Table -AutoSize
} else {
    Write-Host "  当前无 DNS 缓存"
}

Write-Host "`n════════ DNS 缓存中异常的记录 (TTL异常长) ════════"
if ($dnsCache) {
    $abnormal = $dnsCache | Where-Object { $_.TimeToLive -gt 86400 }
    if ($abnormal) {
        $abnormal | Select-Object Entry, Data, TimeToLive | Format-Table -AutoSize
    } else {
        Write-Host "  ✅ 无异常记录"
    }
}

Write-Host "`n💡 如需清空 DNS 缓存，说：「确认清空 DNS 缓存」"
Write-Host "  清空命令: Clear-DnsClientCache  (清空后会自动从DNS服务器重新获取)"
```



### 19.2 DNS 服务器配置与解析链路测试




```powershell
Write-Host "════════ DNS 服务器配置 ════════"
Get-DnsClientServerAddress -AddressFamily IPv4 |
    Where-Object { $_.ServerAddresses.Count -gt 0 } |
    Select-Object @{N='网卡';E={$_.InterfaceAlias}},
        @{N='索引';E={$_.InterfaceIndex}},
        @{N='DNS 服务器';E={($_.ServerAddresses -join ', ')}} |
    Format-Table -AutoSize

Write-Host "`n════════ 解析链路测试 (逐级 DNS) ════════"
$testDomains = @('www.baidu.com', 'www.google.com', 'portal.azure.com')
foreach ($domain in $testDomains) {
    try {
        $result = Resolve-DnsName -Name $domain -Type A -ErrorAction Stop
        $ip = ($result | Where-Object { $_.Type -eq 'A' } | Select-Object -First 1).IPAddress
        if ($ip) { Write-Host "  ✅ $domain → $ip" }
        else { Write-Host "  ❌ $domain → 解析失败" }
    } catch {
        Write-Host "  ❌ $domain → $($_.Exception.Message.Split('.')[0])"
    }
}
```



### 19.3 网卡 IP 配置概览




```powershell
Write-Host "════════ 网卡 IP 配置 ════════"
Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.InterfaceAlias -notmatch 'Loopback' -and $_.IPAddress -ne '127.0.0.1' } |
    Select-Object @{N='网卡';E={$_.InterfaceAlias}},
        @{N='IP 地址';E={$_.IPAddress}},
        @{N='子网掩码';E={$_.PrefixLength}},
        @{N='网关';E={
            $ifIndex = $_.InterfaceIndex
            $gw = Get-NetRoute -InterfaceIndex $ifIndex -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue
            if ($gw) { $gw.NextHop } else { '-' }
        }},
        @{N='状态';E={$_.AddressState}} |
    Format-Table -AutoSize

Write-Host "`n════════ 网卡 MAC 地址与速率 ════════"
Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
    Select-Object @{N='网卡名';E={$_.Name}},
        @{N='MAC';E={$_.MacAddress}},
        @{N='速率';E={if($_.LinkSpeed){ "$([math]::Round($_.LinkSpeed/1e9,1)) Gbps" }else{'未知'}}},
        @{N='状态';E={$_.Status}} |
    Format-Table -AutoSize
```



### 19.4 路由表检查




```powershell
Write-Host "════════ IPv4 路由表 ════════"
Get-NetRoute -AddressFamily IPv4 |
    Where-Object { $_.DestinationPrefix -ne '255.255.255.255/32' } |
    Sort-Object @{E={if ($_.DestinationPrefix -eq '0.0.0.0/0') {0} else {1}}},
        @{E='RouteMetric'} |
    Select-Object @{N='目标网络';E={$_.DestinationPrefix}},
        @{N='下一跳';E={$_.NextHop}},
        @{N='接口';E={$_.InterfaceAlias}},
        @{N='跃点数';E={$_.RouteMetric}},
        @{N='协议';E={$_.Protocol}} |
    Format-Table -AutoSize

Write-Host "`n💡 跃点数越小优先级越高"
Write-Host "💡 0.0.0.0/0 为默认路由（所有出网流量由此控制）"
```



**风险等级**：🟡 中（含 DNS 缓存清空操作，需用户确认）

| 操作 | 风险 | 说明 |
|------|------|------|
| DNS 缓存查看 | 🟢 无 | 纯只读 |
| DNS 解析测试 | 🟢 无 | 纯只读，零风险 |
| 网卡配置查看 | 🟢 无 | 纯只读 |
| 路由表查看 | 🟢 无 | 纯只读 |
| **DNS 缓存清空** | 🟡 中 | 清空后需用户说「确认清空 DNS 缓存」，清空后自动从 DNS 服务器重建，非破坏性 |

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Resolve-DnsName` 超时 | DNS 服务器不可达 | 检查 DNS 服务器配置和网络连通性 |
| `Get-NetIPAddress` 为空 | 网卡未分配 IPv4 | 检查 DHCP 或静态 IP 配置 |
| `Get-NetRoute` 无默认路由 | 无互联网出口 | 检查网关配置 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| DNS 缓存中大量 TTL 异常长的记录 | 可能 DNS 服务器配置问题或域名劫持 |
| 多网卡存在多个默认路由 | 路由冲突导致网络不稳定 |
| DNS 服务器指向不可达 IP | 域名解析全部失败 |
| 网卡速率不匹配（1Gbps vs 100Mbps） | 网线/交换机端口故障 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-20"></a>

