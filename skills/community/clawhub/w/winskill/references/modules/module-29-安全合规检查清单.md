---
id: module-29
name: 安全合规检查清单
description: 安全合规检查清单
keywords: ['安全合规检查清单']
permission: admin
mode: readonly
subset: advanced
---

## 🆕 模块 29：安全合规检查清单

> ⚠️ **本模块所有操作均为只读检测，不会修改任何系统配置。**

<details>
<summary>📋 展开查看：模块 29：安全合规检查清单</summary>

### 29.1 等保 2.0 检查项

```powershell
Write-Host "`n📋 等保 2.0 合规检查报告"
Write-Host ("=" * 60)
Write-Host ("检查时间：{0:yyyy-MM-dd HH:mm:ss}" -f (Get-Date))
Write-Host ("计算机名：$env:COMPUTERNAME")
Write-Host ("=" * 60)

$results = @()

# 1. 密码策略
Write-Host "`n【1. 密码策略】"
$pwdPolicy = net accounts | Out-String
$minPwdLen = if ($pwdPolicy -match 'Minimum password length\s+(\d+)') { $matches[1] } else { "0" }
$maxPwdAge = if ($pwdPolicy -match 'Maximum password age \(days\)\s+(\d+|Unlimited)') { $matches[1] } else { "Unknown" }
$minPwdAge = if ($pwdPolicy -match 'Minimum password age \(days\)\s+(\d+)') { $matches[1] } else { "0" }
$pwdHistory = if ($pwdPolicy -match 'Password history length\s+(\d+)') { $matches[1] } else { "0" }

$pass = [int]$minPwdLen -ge 8
$results += [PSCustomObject]@{ Category = "密码策略"; Item = "密码最小长度≥8"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$minPwdLen" }
Write-Host ("  密码最小长度≥8：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $minPwdLen)

$pass = $maxPwdAge -ne "Unlimited" -and [int]$maxPwdAge -le 90
$results += [PSCustomObject]@{ Category = "密码策略"; Item = "密码最长使用期限≤90天"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$maxPwdAge" }
Write-Host ("  密码最长使用期限≤90天：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $maxPwdAge)

$pass = [int]$pwdHistory -ge 5
$results += [PSCustomObject]@{ Category = "密码策略"; Item = "密码历史记录≥5"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$pwdHistory" }
Write-Host ("  密码历史记录≥5：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $pwdHistory)

# 2. 账户锁定策略
Write-Host "`n【2. 账户锁定策略】"
$lockoutThreshold = if ($pwdPolicy -match 'Lockout threshold\s+(\d+|Never)') { $matches[1] } else { "Unknown" }
$lockoutDuration = if ($pwdPolicy -match 'Lockout duration \(minutes\)\s+(\d+|Never)') { $matches[1] } else { "Unknown" }
$lockoutWindow = if ($pwdPolicy -match 'Lockout observation window \(minutes\)\s+(\d+|Never)') { $matches[1] } else { "Unknown" }

$pass = $lockoutThreshold -ne "Never" -and [int]$lockoutThreshold -le 5
$results += [PSCustomObject]@{ Category = "账户锁定"; Item = "锁定阈值≤5次"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$lockoutThreshold" }
Write-Host ("  锁定阈值≤5次：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $lockoutThreshold)

$pass = $lockoutDuration -ne "Never" -and [int]$lockoutDuration -ge 15
$results += [PSCustomObject]@{ Category = "账户锁定"; Item = "锁定时间≥15分钟"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$lockoutDuration" }
Write-Host ("  锁定时间≥15分钟：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $lockoutDuration)

# 3. 审计日志策略
Write-Host "`n【3. 审计日志策略】"
$auditPolicy = auditpol /get /category:* 2>$null | Out-String
$logonEvents = if ($auditPolicy -match 'Logon\s+Success and Failure') { "Success and Failure" } elseif ($auditPolicy -match 'Logon\s+(\w+)') { $matches[1] } else { "Not Configured" }
$objectAccess = if ($auditPolicy -match 'Object Access\s+Success and Failure') { "Success and Failure" } elseif ($auditPolicy -match 'Object Access\s+(\w+)') { $matches[1] } else { "Not Configured" }
$privilegeUse = if ($auditPolicy -match 'Privilege Use\s+Success and Failure') { "Success and Failure" } elseif ($auditPolicy -match 'Privilege Use\s+(\w+)') { $matches[1] } else { "Not Configured" }

$pass = $logonEvents -eq "Success and Failure"
$results += [PSCustomObject]@{ Category = "审计日志"; Item = "登录事件审计（成功+失败）"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$logonEvents" }
Write-Host ("  登录事件审计：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $logonEvents)

$pass = $objectAccess -eq "Success and Failure"
$results += [PSCustomObject]@{ Category = "审计日志"; Item = "对象访问审计（成功+失败）"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "当前值：$objectAccess" }
Write-Host ("  对象访问审计：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $objectAccess)

# 4. 防火墙状态
Write-Host "`n【4. 防火墙状态】"
$firewallProfiles = Get-NetFirewallProfile
$allEnabled = ($firewallProfiles | Where-Object Enabled -eq $false).Count -eq 0
$results += [PSCustomObject]@{ Category = "防火墙"; Item = "所有配置文件已启用防火墙"; Status = if ($allEnabled) { "✅ 合规" } else { "❌ 不合规" }; Detail = "已启用：$(($firewallProfiles | Where-Object Enabled).Count)/3" }
Write-Host ("  防火墙全部启用：{0}（已启用 {1}/3）" -f $(if ($allEnabled) { "✅" } else { "❌" }), (($firewallProfiles | Where-Object Enabled).Count))

# 5. 补丁更新状态
Write-Host "`n【5. 补丁更新状态】"
$hotfixes = Get-HotFix | Sort-Object InstalledOn -Descending
$pass = $false
if ($hotfixes.Count -gt 0) {
    $lastUpdate = $hotfixes[0].InstalledOn
    $daysSinceUpdate = ((Get-Date) - $lastUpdate).Days
    $pass = $daysSinceUpdate -le 30
} else {
    $lastUpdate = "无记录"
    $daysSinceUpdate = 9999
    $pass = $false
}
$results += [PSCustomObject]@{ Category = "补丁更新"; Item = "最近 30 天内有补丁更新"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "最后更新：$lastUpdate（$($daysSinceUpdate.Days) 天前）" }
Write-Host ("  最近 30 天有补丁：{0}（最后：{1:yyyy-MM-dd}，{2} 天前）" -f $(if ($pass) { "✅" } else { "❌" }), $lastUpdate, $daysSinceUpdate.Days)

# 6. 远程桌面安全
Write-Host "`n【6. 远程桌面安全】"
$rdpEnabled = (Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections -ErrorAction SilentlyContinue).fDenyTSConnections
$rdpStatus = if ($rdpEnabled -eq 0) { "已启用" } else { "已禁用" }
$nlaEnabled = (Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name UserAuthentication -Error Action SilentlyContinue).UserAuthentication
$nlaStatus = if ($nlaEnabled -eq 1) { "已启用" } else { "未启用" }

$pass = $rdpEnabled -ne 0 -or $nlaEnabled -eq 1  # 如果 RDP 启用，必须启用 NLA
$results += [PSCustomObject]@{ Category = "远程桌面"; Item = "RDP 网络级身份验证（NLA）"; Status = if ($pass) { "✅ 合规" } else { "❌ 不合规" }; Detail = "RDP：$rdpStatus，NLA：$nlaStatus" }
Write-Host ("  NLA 已启用：{0}（RDP：{1}，NLA：{2}）" -f $(if ($pass) { "✅" } else { "❌" }), $rdpStatus, $nlaStatus)

# 汇总
$compliant = ($results | Where-Object Status -like "✅*").Count
$nonCompliant = ($results | Where-Object Status -like "❌*").Count
$total = $results.Count
$rate = [math]::Round($compliant / $total * 100, 1)

Write-Host ("`n" + "=" * 60)
Write-Host ("📊 合规汇总：{0}/{1} 项合规（合规率 {2}%）" -f $compliant, $total, $rate)
Write-Host ("✅ 合规：$compliant 项")
Write-Host ("❌ 不合规：$nonCompliant 项")
Write-Host ("=" * 60)

if ($nonCompliant -gt 0) {
    Write-Host "`n❌ 不合规项详情："
    $results | Where-Object Status -like "❌*" | ForEach-Object {
        Write-Host ("  [{0}] {1}：{2}" -f $_.Category, $_.Item, $_.Detail)
    }
}
```

### 29.2 CIS Benchmark 检查（精选关键控制项）

```powershell
Write-Host "`n🔒 CIS Benchmark 检查（Windows Server 精选）"
Write-Host ("=" * 60)

$cisResults = @()

# CIS 1.1.1 - 密码最小长度（CIS 要求 14）
Write-Host "`n【密码策略】"
$minLen = (net accounts | Select-String 'Minimum password length').ToString() -replace '.*?\s+(\d+).*','$1'
$pass = [int]$minLen -ge 14
$cisResults += [PSCustomObject]@{ Control = "1.1.1"; Item = "密码最小长度≥14"; Status = if ($pass) { "✅" } else { "❌" }; Detail = "当前：$minLen" }
Write-Host ("  1.1.1 密码最小长度≥14：{0}（当前：{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $minLen)

# CIS 1.1.2 - 密码复杂度
$complexity = (Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name PasswordComplexity -ErrorAction SilentlyContinue).PasswordComplexity
$pass = $complexity -eq 1
$cisResults += [PSCustomObject]@{ Control = "1.1.2"; Item = "密码复杂度已启用"; Status = if ($pass) { "✅" } else { "❌" }; Detail = "当前：$(if ($complexity -eq 1) { '已启用' } else { '未启用' })" }
Write-Host ("  1.1.2 密码复杂度：{0}" -f $(if ($pass) { "✅" } else { "❌" }))

# CIS 2.2.1 - 禁止 Guest 账户
Write-Host "`n【账户策略】"
$guestAccount = Get-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
$pass = $guestAccount -and $guestAccount.Enabled -eq $false
$cisResults += [PSCustomObject]@{ Control = "2.2.1"; Item = "Guest 账户已禁用"; Status = if ($pass) { "✅" } else { "❌" }; Detail = "当前：$(if ($guestAccount.Enabled -eq $false) { '已禁用' } else { '已启用' })" }
Write-Host ("  2.2.1 Guest 已禁用：{0}" -f $(if ($pass) { "✅" } else { "❌" }))

# CIS 2.3.1.1 - 限制空密码登录
$limitBlank = (Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name LimitBlankPasswordUse -ErrorAction SilentlyContinue).LimitBlankPasswordUse
$pass = $limitBlank -eq 1
$cisResults += [PSCustomObject]@{ Control = "2.3.1.1"; Item = "限制空密码登录"; Status = if ($pass) { "✅" } else { "❌" }; Detail = "当前：$(if ($limitBlank -eq 1) { '已限制' } else { '未限制' })" }
Write-Host ("  2.3.1.1 空密码限制：{0}" -f $(if ($pass) { "✅" } else { "❌" }))

# CIS 5.1 - Windows Update 服务
Write-Host "`n【系统服务】"
$wuService = Get-Service -Name wuauserv -ErrorAction SilentlyContinue
$pass = $wuService -and $wuService.Status -eq "Running"
$cisResults += [PSCustomObject]@{ Control = "5.1"; Item = "Windows Update 服务运行中"; Status = if ($pass) { "✅" } else { "❌" }; Detail = "当前：$($wuService.Status)" }
Write-Host ("  5.1 Windows Update：{0}（{1}）" -f $(if ($pass) { "✅" } else { "❌" }), $wuService.Status)

# CIS 9.1 - Windows Firewall
Write-Host "`n【防火墙】"
$fwProfiles = Get-NetFirewallProfile
$allEnabled = ($fwProfiles | Where-Object Enabled -eq $false).Count -eq 0
$cisResults += [PSCustomObject]@{ Control = "9.1"; Item = "所有防火墙配置文件已启用"; Status = if ($allEnabled) { "✅" } else { "❌" }; Detail = "已启用：$(($fwProfiles | Where-Object Enabled).Count)/3" }
Write-Host ("  9.1 防火墙全部启用：{0}" -f $(if ($allEnabled) { "✅" } else { "❌" }))

# CIS 17.1 - 审计策略
Write-Host "`n【审计策略】"
$auditPolicy = auditpol /get /category:* 2>$null | Out-String
$securityLogon = if ($auditPolicy -match 'Logon\s+Success and Failure') { $true } else { $false }
$cisResults += [PSCustomObject]@{ Control = "17.1"; Item = "登录事件审计（成功+失败）"; Status = if ($securityLogon) { "✅" } else { "❌" }; Detail = "当前：$(if ($securityLogon) { '已配置' } else { '未配置' })" }
Write-Host ("  17.1 登录审计：{0}" -f $(if ($securityLogon) { "✅" } else { "❌" }))

# 汇总
$compliant = ($cisResults | Where-Object Status -eq "✅").Count
$nonCompliant = ($cisResults | Where-Object Status -eq "❌").Count
$total = $cisResults.Count
$rate = [math]::Round($compliant / $total * 100, 1)

Write-Host ("`n" + "=" * 60)
Write-Host ("📊 CIS 汇总：{0}/{1} 项合规（合规率 {2}%）" -f $compliant, $total, $rate)
Write-Host ("=" * 60)
```

### 29.3 合规报告生成（Markdown 文本）

```powershell
# 生成 Markdown 格式合规报告（纯文本，可复制保存为 .md 文件）
$reportTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$reportName = "合规检查报告_$env:COMPUTERNAME`_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

$report = @"
# Windows Server 合规检查报告

| 项目 | 内容 |
|------|------|
| 计算机名 | $env:COMPUTERNAME |
| 检查时间 | $reportTime |
| 操作系统 | $((Get-CimInstance Win32_OperatingSystem).Caption) |
| 版本 | $((Get-CimInstance Win32_OperatingSystem).Version) |

## 等保 2.0 检查结果

| 类别 | 检查项 | 状态 | 详情 |
|------|--------|------|------|
| 密码策略 | 密码最小长度≥8 | 待检查 | - |
| 密码策略 | 密码最长使用期限≤90天 | 待检查 | - |
| 密码策略 | 密码历史记录≥5 | 待检查 | - |
| 账户锁定 | 锁定阈值≤5次 | 待检查 | - |
| 账户锁定 | 锁定时间≥15分钟 | 待检查 | - |
| 审计日志 | 登录事件审计（成功+失败） | 待检查 | - |
| 审计日志 | 对象访问审计（成功+失败） | 待检查 | - |
| 防火墙 | 所有配置文件已启用 | 待检查 | - |
| 补丁更新 | 最近 30 天内有补丁更新 | 待检查 | - |
| 远程桌面 | RDP 网络级身份验证（NLA） | 待检查 | - |

## CIS Benchmark 检查结果

| 控制项 | 检查内容 | 状态 | 详情 |
|--------|----------|------|------|
| 1.1.1 | 密码最小长度≥14 | 待检查 | - |
| 1.1.2 | 密码复杂度已启用 | 待检查 | - |
| 2.2.1 | Guest 账户已禁用 | 待检查 | - |
| 2.3.1.1 | 限制空密码登录 | 待检查 | - |
| 5.1 | Windows Update 服务运行中 | 待检查 | - |
| 9.1 | 所有防火墙配置文件已启用 | 待检查 | - |
| 17.1 | 登录事件审计（成功+失败） | 待检查 | - |

## 说明

- 本报告由 winskill 自动生成，仅作参考
- 实际合规判定需结合企业安全策略和行业标准
- 建议定期运行检查并保存报告备查
"@

# 输出到控制台
Write-Host $report

# 保存到用户输出目录
$outputDir = "$env:USERPROFILE\.workbuddy\output\winskill"
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
$outputFile = Join-Path $outputDir "$reportName.md"
$report | Out-File -FilePath $outputFile -Encoding utf8

Write-Host ("`n✅ 报告已保存到：{0}" -f $outputFile)
Write-Host "提示：可将 .md 文件内容复制到 Word 或在线 Markdown 转 PDF 工具生成 PDF"
```

### 29.4 不合规项修复建议

```powershell
Write-Host "`n🔧 不合规项修复建议"
Write-Host ("=" * 60)
Write-Host "以下命令仅作参考，请确认后再执行：`n"

Write-Host "【密码策略修复】"
Write-Host "net accounts /minpwlen:8              # 设置密码最小长度 8 位"
Write-Host "net accounts /maxpwage:90             # 设置密码最长使用期限 90 天"
Write-Host "net accounts /minpwage:1              # 设置密码最短使用期限 1 天"
Write-Host "net accounts /uniquepy:5              # 密码历史记录 5 个"

Write-Host "`n【账户锁定修复】"
Write-Host "net accounts /lockoutthreshold:5       # 锁定阈值 5 次"
Write-Host "net accounts /lockoutduration:15       # 锁定时间 15 分钟"
Write-Host "net accounts /lockoutwindow:15         # 锁定观察窗口 15 分钟"

Write-Host "`n【审计策略修复】"
Write-Host "auditpol /set /subcategory:'Logon' /success:enable /failure:enable"
Write-Host "auditpol /set /subcategory:'Object Access' /success:enable /failure:enable"
Write-Host "auditpol /set /subcategory:'Privilege Use' /success:enable /failure:enable"

Write-Host "`n【防火墙修复】"
Write-Host "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"

Write-Host "`n【Guest 账户修复】"
Write-Host "Disable-LocalUser -Name 'Guest'        # 禁用 Guest 账户"

Write-Host "`n【RDP NLA 修复】"
Write-Host "Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name UserAuthentication -Value 1"

Write-Host ("`n" + "=" * 60)
Write-Host "⚠️ 以上命令仅供参考，请确认后再执行"
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `auditpol 不是内部或外部命令` | 需要管理员权限 | 以管理员身份运行 PowerShell |
| `Get-NetFirewallProfile 拒绝访问` | 需要管理员权限 | 以管理员身份运行 PowerShell |
| `无法保存报告到输出目录` | 目录不存在或权限不足 | 手动创建 `%USERPROFILE%\.workbuddy\output\winskill` |
| `net accounts 输出格式不符` | 系统语言非中文 | 根据实际输出调整正则匹配 |

</details>


[↑ 返回顶部](#module-1)

---

<a name="module-30"></a>

