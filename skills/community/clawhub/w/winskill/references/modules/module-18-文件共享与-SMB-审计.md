---
id: module-18
name: 文件共享与 SMB 审计
description: 列出所有共享文件夹、当前 SMB 连接、权限风险检测。
keywords: ['有哪些共享文件夹', '共享权限安全吗', '谁在访问共享', 'SMB 审计']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 18：文件共享与 SMB 审计




<details>
<summary>📋 展开查看：🆕 模块 18：文件共享与 SMB 审计</summary>

**用途**：列出所有共享文件夹、当前 SMB 连接、权限风险检测。

**常你说**：`"有哪些共享文件夹"` / `"共享权限安全吗"` / `"谁在访问共享"` / `"SMB 审计"`

> ⚠️ **本模块仅读，不会关闭共享、断开连接或修改权限。**

### 18.1 已共享文件夹清单




```powershell
Write-Host "════════ 已共享文件夹 ════════"
Get-SmbShare | Where-Object { $_.Name -notin @('IPC$','ADMIN$') -or $_.Special -eq $false } |
    Select-Object @{N='共享名';E={$_.Name}},
        @{N='路径';E={$_.Path}},
        @{N='描述';E={if($_.Description){$_.Description}else{'(无)'}}},
        @{N='最大用户数';E={$_.ConcurrentUserLimit}},
        @{N='缓存模式';E={$_.CachingMode}},
        @{N='共享状态';E={$_.ShareState}} |
    Format-Table -AutoSize

Write-Host "`n💡 ADMIN$ 和 IPC$ 为系统默认管理共享，属正常"
```



### 18.2 共享权限审计




```powershell
Write-Host "════════ 共享权限审计 ════════"
$shares = Get-SmbShare | Where-Object { $_.Name -notin @('IPC$','ADMIN$') -or $_.Special -eq $false }

foreach ($share in $shares) {
    Write-Host "`n═══ 共享: $($share.Name) → $($share.Path) ═══"

    # 共享级别权限
    try {
        $sharePerm = Get-SmbShareAccess -Name $share.Name -ErrorAction SilentlyContinue
        foreach ($perm in $sharePerm) {
            $flag = if ($perm.AccessRight -eq 'Full' -and $perm.AccountName -eq 'Everyone') {
                "🔴 高风险: Everyone 拥有完全控制"
            } elseif ($perm.AccountName -eq 'Everyone') {
                "⚠️ Everyone 可访问"
            } else {
                ""
            }
            Write-Host "  共享权限: $($perm.AccountName) -> $($perm.AccessRight)  $flag"
        }
    } catch {
        Write-Host "  共享权限: 无法获取"
    }

    # NTFS 级别权限（对物理路径）
    if (Test-Path $share.Path) {
        $ntfsPerm = Get-Acl $share.Path -ErrorAction SilentlyContinue
        if ($ntfsPerm) {
            $ntfsPerm.Access | Where-Object { $_.IdentityReference -match 'Everyone|BUILTIN|Guest|ANONYMOUS' } |
                ForEach-Object {
                    Write-Host "  NTFS权限: $($_.IdentityReference) -> $($_.FileSystemRights) ⚠️ 宽松权限"
                }
        }
    }
}
```



### 18.3 当前 SMB 连接会话




```powershell
Write-Host "════════ 当前 SMB 连接会话 ════════"
$sessions = Get-SmbSession -ErrorAction SilentlyContinue |
    Select-Object @{N='客户端';E={$_.ClientComputerName}},
        @{N='用户名';E={$_.UserName}},
        @{N='空闲时间(分钟)';E={[math]::Round($_.IdleTime.TotalMinutes, 0)}},
        @{N='会话时长(分钟)';E={[math]::Round((New-TimeSpan -Start $_.SessionStartTime).TotalMinutes, 0)}} |
    Sort-Object @{E='空闲时间(分钟)';Descending=$true}

if ($sessions) {
    $sessions | Format-Table -AutoSize
    Write-Host "`n💡 空闲 >60 分钟的会话可能为僵尸连接"
} else {
    Write-Host "  当前无活跃 SMB 会话"
}
```



### 18.4 开放共享中的风险项汇总




```powershell
Write-Host "════════ 共享风险汇总 ════════"
$risks = @()
$shares = Get-SmbShare | Where-Object { $_.Name -notin @('IPC$','ADMIN$') -or $_.Special -eq $false }

foreach ($share in $shares) {
    $sharePerm = Get-SmbShareAccess -Name $share.Name -ErrorAction SilentlyContinue
    foreach ($perm in $sharePerm) {
        if ($perm.AccountName -eq 'Everyone') {
            $risks += "🔴 [$($share.Name)] Everyone -> $($perm.AccessRight) 控制权"
        }
        if ($perm.AccountName -eq 'ANONYMOUS LOGON' -or $perm.AccountName -eq 'Guest') {
            $risks += "🔴 [$($share.Name)] $($perm.AccountName) -> $($perm.AccessRight)"
        }
    }

    # 检查共享指向路径不存在
    if (-not (Test-Path $share.Path)) {
        $risks += "⚠️ [$($share.Name)] 共享路径不存在: $($share.Path)"
    }
}

if ($risks.Count -gt 0) {
    $risks | ForEach-Object { Write-Host $_ }
    Write-Host "`n建议: 收紧共享权限为最小访问原则，禁用 Guest/匿名访问"
} else {
    Write-Host "✅ 未发现高风险的共享配置"
}

# 同时检查 SMBv1 是否启用
$smb1 = Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -ErrorAction SilentlyContinue
if ($smb1 -and $smb1.State -eq 'Enabled') {
    Write-Host "`n🔴 SMBv1 已启用！存在 WannaCry 等勒索软件漏洞风险，建议禁用"
}
```



**风险等级**：🟢 无（只读审计）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Get-SmbShare` 报错 | SMB 未启用或无权限 | 管理员身份在服务器上执行 |
| `Get-SmbSession` 为空 | 当前无 SMB 连接 | 正常 |
| `Access denied on Get-Acl` | 部分目录 NTFS 权限限制 | 某些系统目录属正常 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| Everyone 拥有完全控制 | 任何网络用户可读/写，极大风险 |
| SMBv1 仍启用 | 永恒之蓝等漏洞存在，应立即禁用 |
| 指向不存在的路径 | 残留共享，建议删除 |
| 大量僵尸 SMB 会话 | 客户端未正常断开，占用连接数 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-19"></a>

