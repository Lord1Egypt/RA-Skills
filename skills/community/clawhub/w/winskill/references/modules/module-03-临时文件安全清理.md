---
id: module-03
name: 临时文件安全清理
description: 扫描安全可删的临时文件，先预览后确认再清理。
keywords: ['帮我清理临时文件', 'C 盘快满了帮清 temp']
permission: user
mode: confirm
subset: basic
---

### 模块 3：临时文件安全清理






<details>
<summary>📋 展开查看：模块 3：临时文件安全清理</summary>

**用途**：扫描安全可删的临时文件，先预览后确认再清理。

**常你说**：`"帮我清理临时文件"` / `"C 盘快满了帮清 temp"`

**安全清理路径**：

| 路径 | 说明 | 安全天数 |
|------|------|---------|
| `%TEMP%\*` | 用户临时文件 | >7 天 |
| `C:\Windows\Temp\*` | 系统临时文件 | >7 天 |
| `C:\Windows\SoftwareDistribution\Download\*` | Windows Update 下载缓存 | 任意 |
| `C:\Windows\Prefetch\*` | 程序预取 | >30 天 |
| `IIS Temporary Compressed Files\*` | IIS 压缩缓存 | >1 天 |




```powershell
$tempPath = $env:TEMP
$daysOld = 7
$cutoff = (Get-Date).AddDays(-$daysOld)

$tempFiles = Get-ChildItem -Path $tempPath -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $cutoff }

Write-Host "═══════════════════════════════════════════"
Write-Host "  📋 扫描结果: $tempPath"
Write-Host "  过期临时文件数: $($tempFiles.Count) 个"
Write-Host "═══════════════════════════════════════════"

$tempFiles | Sort-Object Length -Descending |
    Select-Object -First 20 |
    Select-Object @{N='文件路径';E={$_.FullName}},
        @{N='大小(KB)';E={[math]::Round($_.Length/1KB,1)}},
        @{N='最后修改';E={$_.LastWriteTime}} |
    Format-Table -AutoSize

$totalKB = ($tempFiles | Measure-Object -Property Length -Sum).Sum
Write-Host "  预计可释放空间: $([math]::Round($totalKB/1MB,2)) MB"
Write-Host "  ⚠️ 确认删除请说 '确认清理'"
```






```powershell
# ⚠️ 仅当用户明确说「确认清理」后才执行！
Write-Host "  正在移到回收站..."
$shell = New-Object -ComObject Shell.Application
$rb = $shell.NameSpace(0x0a)
$totalFiles = 0
foreach ($f in $tempFiles) {
    try {
        $rb.MoveHere($f.FullName)
        $totalFiles++
    } catch { }
}
Write-Host "  ✅ 已完成！已将 $totalFiles 个文件移到回收站"
Write-Host "  如需彻底删除，请手动清空回收站"
```



**风险等级**：🟡 中（需确认后删除）

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Cannot find path ... does not exist` | temp 目录下某些路径不存在 | 自动跳过 |
| `Access is denied` | 系统临时文件正在使用中 | 跳过，正常现象 |
| `MoveHere` 失败 | 回收站操作异常 | 手动清或用其他方式 |




</details>

[↑ 返回顶部](#module-1)

---

<a name="module-4"></a>

