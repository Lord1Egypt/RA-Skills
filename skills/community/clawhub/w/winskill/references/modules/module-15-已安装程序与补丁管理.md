---
id: module-15
name: 已安装程序与补丁管理
description: 查看所有已安装的软件、补丁，检测缺失或不一致情况。
keywords: ['看看系统安装了哪些软件', '服务器装了什么程序', '补丁检查']
permission: admin
mode: readonly
subset: basic
---

## 🆕 模块 15：已安装程序与补丁管理




<details>
<summary>📋 展开查看：🆕 模块 15：已安装程序与补丁管理</summary>

**用途**：查看所有已安装的软件、补丁，检测缺失或不一致情况。

**常你说**：`"看看系统安装了哪些软件"` / `"服务器装了什么程序"` / `"补丁检查"`

> ⚠️ **本模块仅读，不会卸载/安装/修改任何软件。**

### 15.1 已安装程序清单




```powershell
Write-Host "════════ 已安装程序清单 ════════"
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -and $_.UninstallString -notlike '*{*' } |
    Select-Object @{N='程序名';E={$_.DisplayName}},
        @{N='版本';E={$_.DisplayVersion}},
        @{N='安装日期';E={$_.InstallDate}},
        @{N='大小';E={if($_.EstimatedSize){[math]::Round($_.EstimatedSize/1MB,1)}else{'?'}}} |
    Sort-Object DisplayName |
    Format-Table -AutoSize
```



### 15.2 已安装 Windows 补丁




```powershell
Write-Host "════════ 已安装 Windows 补丁 ════════"
Get-HotFix | Sort-Object InstalledOn -Descending |
    Select-Object @{N='补丁ID';E={$_.HotFixID}},
        @{N='安装日期';E={$_.InstalledOn}},
        @{N='描述';E={$_.Description}} |
    Format-Table -AutoSize
```



### 15.3 安装时间线分析




```powershell
Write-Host "════════ 最近安装的软件 ════════"
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.InstallDate } |
    Sort-Object InstallDate -Descending |
    Select-Object -First 20 @{N='程序名';E={$_.DisplayName}},
        @{N='版本';E={$_.DisplayVersion}},
        @{N='安装日期';E={$_.InstallDate}} |
    Format-Table -AutoSize
```



### 15.4 补丁对比（检测缺失）




```powershell
$hotfixes = Get-HotFix -ErrorAction SilentlyContinue | Select-Object -ExpandProperty HotFixID
$currentBuild = [System.Environment]::OSVersion.Version
$expectedPatches = @()

# 检测 Windows 10/11 常见缺失补丁
if ($currentBuild.Major -ge 10) {
    $kbToCheck = @(
        "KB5034441",  # Secure Boot DBX
        "KB5036897",  # 最新 .NET
        "KB5037771"   # 最新累积
    )
    foreach ($kb in $kbToCheck) {
        if ($hotfixes -notcontains $kb) {
            $expectedPatches += "$kb - 缺失"
        }
    }
}

Write-Host "════════ 补丁一致性检查 ════════"
Write-Host "  当前版本: $($currentBuild.Major).$($currentBuild.Minor).$($currentBuild.Build)"
Write-Host ""
if ($expectedPatches.Count -gt 0) {
    Write-Host "  ⚠️ 缺失补丁:"
    foreach ($p in $expectedPatches) { Write-Host "    ❌ $p" }
} else {
    Write-Host "  ✅ 常用补丁均已安装"
}
```



**风险等级**：🟢 无（只读阅读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Requested registry access is not allowed` | 部分注册表权限限制 | 管理员身份执行 |
| `Get-HotFix` 报错 | 需要管理员权限 | 管理员身份执行 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| 某台服务器明显比其他机器少很多补丁 | 可能 WSUS/自动更新未运行 |
| 安装时间线上出现未知日期的软件 | 可能未经授权安装，需排查 |
| KB 补丁安装失败 | Windows Update 服务或缓存异常 |



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-16"></a>

