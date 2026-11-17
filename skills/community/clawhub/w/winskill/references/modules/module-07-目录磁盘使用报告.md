---
id: module-07
name: 目录磁盘使用报告
description: 用进度条样式一眼看出各目录占用。
keywords: ['看看各个目录的空间占用']
permission: user
mode: readonly
subset: disk-management
---

### 模块 7：目录磁盘使用报告

> ⚠️ 此模块已合并到 **模块 34「磁盘体检」**。直接对 AI 说「帮我看看磁盘」即可获取完整报告。本模块代码保留，避免外部脚本失效。






<details>
<summary>📋 展开查看：模块 7：目录磁盘使用报告</summary>

**用途**：用进度条样式一眼看出各目录占用。

**常你说**：`"看看各个目录的空间占用"`




```powershell
function Get-DirectorySize([string]$Path) {
    (Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue |
     Measure-Object -Property Length -Sum).Sum
}

$dirs = @("C:\inetpub", "C:\Windows\Temp", "C:\ProgramData",
          "$env:TEMP", "C:\Users",
          "C:\Windows\SoftwareDistribution", "D:\")

foreach ($d in $dirs) {
    if (Test-Path $d) {
        $sizeGB = [math]::Round((Get-DirectorySize $d) / 1GB, 2)
        if ($sizeGB -gt 10)     { $icon = '🔴' }
        elseif ($sizeGB -gt 5) { $icon = '🟡' }
        else                  { $icon = '🟢' }
        Write-Host "  $icon $d : ${sizeGB} GB"
    }
}
```



**风险等级**：🟢 无（只读）



</details>

[↑ 返回顶部](#module-1)

---

<a name="module-8"></a>

