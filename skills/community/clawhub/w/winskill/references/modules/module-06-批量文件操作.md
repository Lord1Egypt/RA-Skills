---
id: module-06
name: 批量文件操作
description: 先预览规则，再确认执行批量重命名/移动。
keywords: ['把所有 .log 改成 backup_1.log 格式']
permission: user
mode: confirm
subset: basic
---

### 模块 6：批量文件操作






<details>
<summary>📋 展开查看：模块 6：批量文件操作</summary>

**用途**：先预览规则，再确认执行批量重命名/移动。

**常你说**：`"把所有 .log 改成 backup_1.log 格式"`




```powershell
$sourceDir = "D:\logs"    # ← 源目录
$searchFilter = "*.log"   # ← 文件筛选
$renamePrefix = "backup"  # ← 新文件名前缀

$files = Get-ChildItem -Path $sourceDir -Filter $searchFilter -File
Write-Host "════════ 批量重命名预览 ════════"
Write-Host "  扫描到 $($files.Count) 个 $searchFilter 文件"

$i = 1
foreach ($f in $files) {
    Write-Host "  🔄 $($f.Name) → ${renamePrefix}_${i}${f.Extension}"
    $i++
}

Write-Host "`n  共 $($files.Count) 个文件将被重命名"
Write-Host "  ⚠️ 确认执行请说 '确认重命名'"
```






```powershell
# ⚠️ 仅当用户明确说「确认重命名」后才执行！
# $i = 1
# foreach ($f in $files) {
#     $newName = "${renamePrefix}_${i}${f.Extension}"
#     Rename-Item -Path $f.FullName -NewName $newName
#     Write-Host "  ✅ $($f.Name) → $newName"
#     $i++
# }
```



**风险等级**：🟡 中（需确认）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Cannot rename because item already exists` | 新文件名已存在 | 加时间戳避免重名 |
| `Access to the path is denied` | 文件锁定 | 关相关程序再试 |




</details>

[↑ 返回顶部](#module-1)

---

<a name="module-7"></a>

