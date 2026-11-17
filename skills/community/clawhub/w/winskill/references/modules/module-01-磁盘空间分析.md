---
id: module-01
name: 磁盘空间分析
description: 扫描指定路径，找出占用空间的大文件和目录。
keywords: ['扫一下 C 盘大文件', 'D 盘哪个最占空间']
permission: admin
mode: readonly
subset: disk-management
---

### 模块 1：磁盘空间分析

> ⚠️ 此模块已合并到 **模块 34「磁盘体检」**。直接对 AI 说「帮我看看磁盘」即可获取完整报告。本模块代码保留，避免外部脚本失效。






<details>
<summary>📋 展开查看：模块 1：磁盘空间分析</summary>

**用途**：扫描指定路径，找出占用空间的大文件和目录。

**常你说**：`"扫一下 C 盘大文件"` / `"D 盘哪个最占空间"`




```powershell
$scanPath = "C:\"   # ← 改成你要扫的盘符或目录

Get-ChildItem -Path $scanPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 100MB } |
    Sort-Object Length -Descending |
    Select-Object -First 50 @{N='路径';E={$_.FullName}},
        @{N='大小(GB)';E={[math]::Round($_.Length/1GB,2)}},
        @{N='最后修改';E={$_.LastWriteTime}}
```



**风险等级**：🟢 无（只读）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Access to the path 'xxx' is denied` | 权限不足 | 管理员身份运行 PowerShell |
| `Could not find a part of the path` | 目录不存在 | 确认路径 |




</details>

[↑ 返回顶部](#module-1)

---

<a name="module-2"></a>

