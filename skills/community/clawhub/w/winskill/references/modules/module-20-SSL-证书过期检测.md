---
id: module-20
name: SSL 证书过期检测
description: 检测本机 IIS / 所有 HTTPS 站点的 SSL 证书到期时间，提前预警，避免网站突然报"证书无效"。
keywords: ['SSL 证书快到期了吗', '证书检查', 'HTTPS 站点证书还有多久', '哪些证书要过期了']
permission: admin
mode: readonly
subset: network-security
---

## 🆕 模块 20：SSL 证书过期检测




<details>
<summary>📋 展开查看：🆕 模块 20：SSL 证书过期检测</summary>

**用途**：检测本机 IIS / 所有 HTTPS 站点的 SSL 证书到期时间，提前预警，避免网站突然报"证书无效"。

**常你说**：`"SSL 证书快到期了吗"` / `"证书检查"` / `"HTTPS 站点证书还有多久"` / `"哪些证书要过期了"`

> ⚠️ **本模块仅读，不会申请、续签或删除任何证书。**

### 20.1 本机证书仓库扫描（个人 + 机器）




```powershell
Write-Host "════════ 本机证书过期检查 ════════"
$warningDays = 30
$now = Get-Date

$stores = @(
    [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine,
    [System.Security.Cryptography.X509Certificates.StoreLocation]::CurrentUser
)
$storeNames = @('My', 'WebHosting', 'Root', 'CA')

$certs = foreach ($loc in $stores) {
    foreach ($name in $storeNames) {
        try {
            $store = [System.Security.Cryptography.X509Certificates.X509Store]::new($name, $loc)
            $store.Open('ReadOnly')
            foreach ($cert in $store.Certificates) {
                $daysLeft = ($cert.NotAfter - $now).Days
                [PSCustomObject]@{
                    主体       = ($cert.Subject -replace 'CN=', '' -split ',')[0].Trim()
                    存储位置   = "$loc\$name"
                    到期时间   = $cert.NotAfter.ToString('yyyy-MM-dd')
                    剩余天数   = $daysLeft
                    状态       = if ($daysLeft -lt 0) { '❌ 已过期' }
                                 elseif ($daysLeft -lt $warningDays) { '⚠️ 即将过期' }
                                 else { '✅ 正常' }
                    颁发者     = ($cert.Issuer -replace 'CN=', '' -split ',')[0].Trim()
                }
            }
            $store.Close()
        } catch {}
    }
}

$result = $certs | Where-Object { $_.剩余天数 -lt 90 } |
    Sort-Object 剩余天数

if ($result) {
    $result | Format-Table -AutoSize
} else {
    Write-Host "✅ 未发现 90 天内到期的证书"
}
```



### 20.2 IIS 绑定的 HTTPS 证书检查




```powershell
Write-Host "════════ IIS HTTPS 绑定证书 ════════"
Import-Module WebAdministration -ErrorAction SilentlyContinue

$httpsBindings = Get-WebBinding | Where-Object { $_.protocol -eq 'https' }
if (-not $httpsBindings) {
    Write-Host "  未发现 HTTPS 绑定"
} else {
    foreach ($binding in $httpsBindings) {
        $hash = $binding.certificateHash
        if ($hash) {
            $cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Thumbprint -eq $hash }
            if ($cert) {
                $daysLeft = ($cert.NotAfter - (Get-Date)).Days
                $status = if ($daysLeft -lt 0) { '❌ 已过期' }
                           elseif ($daysLeft -lt 30) { '⚠️ 即将过期' }
                           else { '✅ 正常' }
                Write-Host "  站点: $($binding.bindingInformation)"
                Write-Host "  证书: $($cert.Subject)"
                Write-Host "  到期: $($cert.NotAfter.ToString('yyyy-MM-dd'))  剩余: $daysLeft 天  $status"
                Write-Host ""
            }
        }
    }
}
```



### 20.3 远程域名证书探测（本地无证书的站点）




```powershell
# 将下方域名替换为你需要检测的站点
$domains = @('www.baidu.com', 'www.taobao.com')  # 示例，替换为你的域名

Write-Host "════════ 远程域名 SSL 证书检测 ════════"
foreach ($domain in $domains) {
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient($domain, 443)
        $sslStream  = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false, { $true })
        $sslStream.AuthenticateAsClient($domain)
        $cert = $sslStream.RemoteCertificate
        $expiry = [DateTime]::Parse($cert.GetExpirationDateString())
        $daysLeft = ($expiry - (Get-Date)).Days
        $status = if ($daysLeft -lt 0) { '❌ 已过期' }
                   elseif ($daysLeft -lt 30) { '⚠️ 即将过期' }
                   else { '✅ 正常' }
        Write-Host "  $domain → 到期: $($expiry.ToString('yyyy-MM-dd'))  剩余: $daysLeft 天  $status"
        $sslStream.Close()
        $tcpClient.Close()
    } catch {
        Write-Host "  $domain → ❌ 连接失败: $($_.Exception.Message.Split('.')[0])"
    }
}
```



### 20.4 即将过期证书汇总报告




```powershell
Write-Host "════════ 30 天内到期证书汇总 ════════"
$now = Get-Date
$soon = @()

foreach ($loc in @('LocalMachine','CurrentUser')) {
    foreach ($name in @('My','WebHosting')) {
        try {
            $store = [System.Security.Cryptography.X509Certificates.X509Store]::new($name, $loc)
            $store.Open('ReadOnly')
            $soon += $store.Certificates | Where-Object {
                ($_.NotAfter - $now).Days -le 30 -and ($_.NotAfter - $now).Days -ge 0
            } | Select-Object @{N='证书名';E={($_.Subject -replace 'CN=','' -split ',')[0].Trim()}},
                @{N='剩余天数';E={($_.NotAfter - $now).Days}},
                @{N='到期日期';E={$_.NotAfter.ToString('yyyy-MM-dd')}},
                @{N='存储';E={"$loc\$name"}}
            $store.Close()
        } catch {}
    }
}

if ($soon.Count -gt 0) {
    $soon | Sort-Object 剩余天数 | Format-Table -AutoSize
    Write-Host "`n🔴 以上证书需要尽快续签！"
} else {
    Write-Host "✅ 30 天内无证书过期"
}
```



**风险等级**：🟢 无（只读，不修改任何证书）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access denied` | 需管理员权限 | 管理员身份执行 |
| `WebAdministration not found` | IIS 未安装 | 跳过模块 20.2 |
| `Connection refused` | 远程域名 443 不可达 | 检查域名和防火墙 |
| `AuthenticationException` | SSL 握手失败 | 域名可能证书异常 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 证书显示"已过期"但网站仍在访问 | 浏览器有缓存，实际用户已经开始看到警告 |
| IIS 绑定的证书和仓库里的不一致 | IIS 用指纹引用，需手动在 IIS 管理器重新绑定 |
| Let's Encrypt 证书 90 天到期周期 | 需设置自动续签（如 win-acme） |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-21"></a>

