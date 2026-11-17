---
id: module-02
name: 大文件重复检测
description: 通过 MD5 哈希找出重复文件。
keywords: ['找找 D 盘有没有重复文件']
permission: user
mode: readonly
subset: disk-management
---

### 模块 2：大文件重复检测

> ⚠️ 此模块已合并到 **模块 34「磁盘体检」**（含模糊重复检测）。直接对 AI 说「帮我看看磁盘」即可获取完整报告。本模块代码保留，避免外部脚本失效。






<details>
<summary>📋 展开查看：模块 2：大文件重复检测</summary>

**用途**：通过 MD5 哈希找出重复文件。

**常你说**：`"找找 D 盘有没有重复文件"`




```powershell
$scanPath = "D:\"   # ← 扫描目标目录
$minSize = 1MB      # ← 只检测大于 1MB 的文件

Get-ChildItem -Path $scanPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt $minSize } |
    ForEach-Object {
        $hash = (Get-FileHash $_.FullName -Algorithm MD5 -ErrorAction SilentlyContinue).Hash
        if ($hash) {
            [PSCustomObject]@{
                路径 = $_.FullName
                哈希 = $hash
                大小MB = [math]::Round($_.Length/1MB,2)
            }
        }
    } |
    Group-Object 哈希 |
    Where-Object { $_.Count -gt 1 } |
    ForEach-Object { $_.Group }
```



**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Exception getting file hash` | 文件正在使用 | 跳过 |
| `The specified path is not valid` | 路径格式不对 | 检查路径 |




</details>

[↑ 返回顶部](#module-1)

---

<a name="module-3"></a>

