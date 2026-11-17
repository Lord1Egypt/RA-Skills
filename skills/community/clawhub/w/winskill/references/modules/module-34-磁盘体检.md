---
id: module-34
name: 磁盘体检
description: 磁盘体检统一入口（大文件+精确/模糊重复+目录报告→单份HTML报告+三级清理建议）
keywords: ['磁盘体检', '帮我看看磁盘', '磁盘报告', '清理建议', '重复文件', '大文件']
permission: admin
mode: readonly
subset: disk-management
---

## 🆕 模块 34：磁盘体检（统一入口）

> ⚠️ 合并模块 1（空间分析）+ 模块 2（重复检测）+ 模块 7（目录报告）+ 新增模糊重复检测。一次扫描输出一份 HTML 报告，单文件离线可开。

<details>
<summary>📋 展开查看：模块 34：磁盘体检</summary>

### 34.1 运行磁盘体检（完整流程）

```powershell
# ===== 磁盘体检编排器 v3.4.0 =====
# 一次扫描 → 一份 HTML 报告（treemap + 大文件榜 + 重复清单 + 三级清理建议）
# 性能目标：500GB ≤ 10 分钟（硬件自适应）

$scanPath = "C:\"   # ← 改成你要体检的盘符
$outDir   = "$env:USERPROFILE\.workbuddy\output\winskill"
$report   = Join-Path $outDir "disk_health_report.html"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# --- 硬件自适应 ---
$cpuCores = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
$maxThreads = [Math]::Max(1, [Math]::Min($cpuCores, 8))
$minFileSize = 10MB   # 小于此值的文件不参与重复检测（性能优化）
$largeFileThreshold = 100MB  # 大文件：只哈希前 1MB 采样（性能优化）

Write-Host "🔍 磁盘体检开始：$scanPath"
Write-Host "   CPU: $cpuCores 核 | 并行: $maxThreads 线程 | 最小文件: $([math]::Round($minFileSize/1MB,0))MB"
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

# ===== 阶段 1：文件扫描 =====
Write-Host "`n[1/5] 扫描文件..."
$allFiles = [System.Collections.Generic.List[PSCustomObject]]::new()
Get-ChildItem -Path $scanPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -ge $minFileSize } |
    ForEach-Object {
        $allFiles.Add([PSCustomObject]@{
            Path = $_.FullName
            Size = $_.Length
            Ext  = $_.Extension.ToLower()
            Dir  = $_.Directory.Name
            MTime = $_.LastWriteTime
        })
    }
Write-Host "   扫描完成：$($allFiles.Count) 个文件（≥$([math]::Round($minFileSize/1MB,0))MB）"

# ===== 阶段 2：大文件 Top 榜 =====
Write-Host "`n[2/5] 大文件 Top 50..."
$topFiles = $allFiles | Sort-Object Size -Descending | Select-Object -First 50

# ===== 阶段 3：目录占用统计（Treemap 数据） =====
Write-Host "`n[3/5] 目录占用统计..."
$dirStats = $allFiles | Group-Object Dir | ForEach-Object {
    [PSCustomObject]@{
        Dir  = $_.Name
        Size = ($_.Group | Measure-Object Size -Sum).Sum
        Count = $_.Count
    }
} | Sort-Object Size -Descending | Select-Object -First 30

# ===== 阶段 4：重复检测（精确 + 模糊） =====
Write-Host "`n[4/5] 重复检测（精确哈希 + 模糊近似）..."

# --- 阶段 4a：精确 MD5 哈希分组 ---
$hashGroups = @{}
$exactDups = [System.Collections.Generic.List[PSCustomObject]]::new()
$uniqueFiles = [System.Collections.Generic.List[PSCustomObject]]::new()

# 按大小分组（相同大小才可能相同）
$sizeGroups = $allFiles | Group-Object Size | Where-Object { $_.Count -gt 1 }

foreach ($sg in $sizeGroups) {
    foreach ($f in $sg.Group) {
        try {
            if ($f.Size -gt $largeFileThreshold) {
                # 大文件：只哈希前 1MB 采样
                $fs = [System.IO.File]::OpenRead($f.Path)
                $buf = New-Object byte[] (1MB)
                $read = $fs.Read($buf, 0, 1MB)
                $hasher = [System.Security.Cryptography.MD5]::Create()
                $hash = $hasher.ComputeHash($buf, 0, $read)
                $hashStr = [BitConverter]::ToString($hash) -replace '-',''
                $fs.Close()
            } else {
                $hashStr = (Get-FileHash $f.Path -Algorithm MD5 -ErrorAction SilentlyContinue).Hash
            }
            if ($hashStr) {
                if (-not $hashGroups.ContainsKey($hashStr)) {
                    $hashGroups[$hashStr] = [System.Collections.Generic.List[PSCustomObject]]::new()
                }
                $hashGroups[$hashStr].Add($f)
            }
        } catch {
            # 文件正在使用，跳过
        }
    }
}

# 提取精确重复组
foreach ($hg in $hashGroups.Values) {
    if ($hg.Count -gt 1) {
        $exactDups.Add([PSCustomObject]@{
            Hash  = $hg[0].Path  # 用第一个路径做标识
            Files = $hg
            Count = $hg.Count
            Size  = $hg[0].Size
            TotalWaste = $hg[0].Size * ($hg.Count - 1)
        })
    }
    # 唯一文件池（用于模糊检测）
    if ($hg.Count -eq 1) {
        $uniqueFiles.Add($hg[0])
    }
}

Write-Host "   精确重复：$($exactDups.Count) 组"

# --- 阶段 4b：模糊重复检测（唯一文件池内）---
# 两阶段：文件名 SimHash 相似度 + 大小近似
$fuzzyDups = [System.Collections.Generic.List[PSCustomObject]]::new()

# 阈值（从 YAML 读取，可配置；缺失则用默认值）
$thFile = "$env:USERPROFILE\.workbuddy\output\winskill\thresholds.yaml"
$fuzzyCfg = @{}
if (Test-Path $thFile) {
    Get-Content $thFile | ForEach-Object {
        $l = $_.Trim()
        if ($l -and -not $l.StartsWith('#') -and -not $l.StartsWith('version') -and -not $l.StartsWith('updated') -and $l -match '^(.+?):\s*(.+)$') {
            $fuzzyCfg[$matches[1].Trim()] = $matches[2].Trim().Trim('"')
        }
    }
}
$filenameSimThreshold = if ($fuzzyCfg.ContainsKey('fuzzy_filename_similarity_threshold')) { [double]$fuzzyCfg['fuzzy_filename_similarity_threshold'] } else { 0.75 }
$sizeApproxThreshold  = if ($fuzzyCfg.ContainsKey('fuzzy_size_approximation_threshold')) { [double]$fuzzyCfg['fuzzy_size_approximation_threshold'] } else { 0.10 }
$maxCompare = if ($fuzzyCfg.ContainsKey('fuzzy_max_compare_per_bucket')) { [int]$fuzzyCfg['fuzzy_max_compare_per_bucket'] } else { 1000 }

# 按大小分桶（大小相近的才比较）
$sizeBuckets = $uniqueFiles | ForEach-Object {
    $bucketSize = [math]::Max(1MB, [math]::Floor($_.Size / (1MB)) * 1MB)
    [PSCustomObject]@{
        File = $_
        Bucket = $bucketSize
    }
} | Group-Object Bucket

foreach ($bucket in $sizeBuckets) {
    $files = $bucket.Group.File
    if ($files.Count -lt 2) { continue }
    
    # 计算每个文件名的 SimHash 指纹
    $fingerprints = @{}
    foreach ($f in $files) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($f.Path).ToLower()
        $fingerprints[$f.Path] = Get-SimHash $name
    }
    
    # 两两比较（限制比较数量，避免 O(n^2) 爆炸）
    $compareCount = 0
    $fileList = $files
    
    for ($i = 0; $i -lt $fileList.Count - 1; $i++) {
        for ($j = $i + 1; $j -lt $fileList.Count; $j++) {
            if ($compareCount++ -ge $maxCompare) { break }
            
            $sizeDiff = [math]::Abs($fileList[$i].Size - $fileList[$j].Size) / [math]::Max($fileList[$i].Size, $fileList[$j].Size)
            if ($sizeDiff -gt $sizeApproxThreshold) { continue }
            
            $sim = Get-SimHashSimilarity $fingerprints[$fileList[$i].Path] $fingerprints[$fileList[$j].Path]
            if ($sim -ge $filenameSimThreshold) {
                $fuzzyDups.Add([PSCustomObject]@{
                    File1 = $fileList[$i].Path
                    File2 = $fileList[$j].Path
                    Similarity = $sim
                    Size1 = $fileList[$i].Size
                    Size2 = $fileList[$j].Size
                })
            }
        }
        if ($compareCount -ge $maxCompare) { break }
    }
}

Write-Host "   模糊重复：$($fuzzyDups.Count) 对"

# ===== 阶段 5：三级清理建议 =====
Write-Host "`n[5/5] 生成清理建议..."

# 三级分类函数
function Get-SafetyTier {
    param([PSCustomObject]$File)
    $path = $File.Path.ToLower()
    $ext = $File.Ext
    
    # 🔴 禁碰
    $forbiddenPatterns = @(
        'c:\windows\', 'c:\program files\', 'c:\program files (x86)\',
        'c:\programdata\microsoft\', 'c:\users\*\appdata\local\microsoft\',
        'c:\$'
    )
    foreach ($fp in $forbiddenPatterns) {
        if ($path -like "$fp*") { return 'forbidden' }
    }
    if ($path -match 'boot|system volume information|recycler') { return 'forbidden' }
    
    # 🟢 可安全删
    $safePatterns = @(
        '\temp\', '\tmp\', '\cache\', '\logs\',
        'c:\windows\temp\', 'c:\windowspreinstallation\',
        'c:\windows\softwaredistribution\download\'
    )
    $safeExts = @('.tmp', '.log', '.bak', '.old', '.dmp', '.etl')
    foreach ($sp in $safePatterns) {
        if ($path -like "*$sp*") { return 'safe' }
    }
    if ($safeExts -contains $ext) { return 'safe' }
    
    # 🟡 需确认
    return 'confirm'
}

$cleanupItems = [System.Collections.Generic.List[PSCustomObject]]::new()

# 大文件 → 需确认
foreach ($f in $topFiles) {
    if ($f.Size -gt 1GB) {
        $tier = Get-SafetyTier $f
        $cleanupItems.Add([PSCustomObject]@{
            Type = 'large'
            Path = $f.Path
            Size = $f.Size
            Tier = $tier
            TierLabel = if ($tier -eq 'safe') { '🟢 可安全删' } elseif ($tier -eq 'confirm') { '🟡 需确认' } else { '🔴 禁碰' }
        })
    }
}

# 精确重复 → 需确认（保留一份）
foreach ($dup in $exactDups) {
    for ($i = 1; $i -lt $dup.Files.Count; $i++) {
        $tier = Get-SafetyTier $dup.Files[$i]
        $cleanupItems.Add([PSCustomObject]@{
            Type = 'duplicate'
            Path = $dup.Files[$i].Path
            Size = $dup.Files[$i].Size
            Tier = $tier
            TierLabel = if ($tier -eq 'safe') { '🟢 可安全删' } elseif ($tier -eq 'confirm') { '🟡 需确认' } else { '🔴 禁碰' }
        })
    }
}

# 模糊重复 → 需确认
foreach ($fd in $fuzzyDups) {
    $tier = Get-SafetyTier ([PSCustomObject]@{Path=$fd.File2; Ext=[System.IO.Path]::GetExtension($fd.File2).ToLower()})
    $cleanupItems.Add([PSCustomObject]@{
        Type = 'fuzzy'
        Path = $fd.File2
        Size = $fd.Size2
        Tier = $tier
        TierLabel = if ($tier -eq 'safe') { '🟢 可安全删' } elseif ($tier -eq 'confirm') { '🟡 需确认' } else { '🔴 禁碰' }
    })
}

$stopwatch.Stop()
$elapsed = [math]::Round($stopwatch.Elapsed.TotalMinutes, 1)

# ===== HTML 报告生成 =====
Write-Host "`n📊 生成 HTML 报告..."

# Treemap SVG 生成
$treemapSvg = Get-TreemapSvg $dirStats 800 400

# 报告头部
$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>磁盘体检报告 - $scanPath</title>
<style>
  body { font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; margin: 0; padding: 20px; background: #f5f7fa; color: #333; }
  .container { max-width: 1200px; margin: 0 auto; }
  h1 { color: #1a73e8; border-bottom: 3px solid #1a73e8; padding-bottom: 10px; }
  h2 { color: #333; margin-top: 30px; border-left: 4px solid #1a73e8; padding-left: 12px; }
  .summary { display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
  .card { background: #fff; border-radius: 8px; padding: 16px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); min-width: 180px; }
  .card .value { font-size: 28px; font-weight: bold; color: #1a73e8; }
  .card .label { font-size: 13px; color: #666; margin-top: 4px; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
  th { background: #1a73e8; color: #fff; padding: 10px 14px; text-align: left; font-size: 13px; }
  td { padding: 8px 14px; border-bottom: 1px solid #eee; font-size: 13px; }
  tr:hover td { background: #f0f4ff; }
  .tier-safe { color: #0d904f; font-weight: bold; }
  .tier-confirm { color: #f0a500; font-weight: bold; }
  .tier-forbidden { color: #d93025; font-weight: bold; }
  .treemap { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
  .progress { background: #e0e0e0; border-radius: 4px; height: 20px; overflow: hidden; }
  .progress-bar { height: 100%; border-radius: 4px; }
  .footer { margin-top: 30px; padding-top: 16px; border-top: 1px solid #ddd; color: #999; font-size: 12px; }
</style>
</head>
<body>
<div class="container">
<h1>🔍 磁盘体检报告</h1>
<p>扫描路径：<strong>$scanPath</strong> | 生成时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | 耗时：$elapsed 分钟</p>

<div class="summary">
  <div class="card"><div class="value">$($allFiles.Count)</div><div class="label">文件总数</div></div>
  <div class="card"><div class="value">$([math]::Round(($allFiles | Measure-Object Size -Sum).Sum / 1GB, 1)) GB</div><div class="label">总占用</div></div>
  <div class="card"><div class="value">$($exactDups.Count)</div><div class="label">精确重复组</div></div>
  <div class="card"><div class="value">$($fuzzyDups.Count)</div><div class="label">模糊重复对</div></div>
  <div class="card"><div class="value">$([math]::Round(($cleanupItems | Where-Object Tier -eq 'safe' | Measure-Object Size -Sum).Sum / 1MB, 0)) MB</div><div class="label">可安全清理</div></div>
</div>

<h2>📊 目录占用 Treemap</h2>
<div class="treemap">
$treemapSvg
</div>

<h2>📁 大文件 Top 50</h2>
<table>
<tr><th>#</th><th>路径</th><th>大小</th><th>修改时间</th><th>安全分级</th></tr>
$(
    $rank = 0
    foreach ($f in $topFiles) {
        $tier = Get-SafetyTier $f
        $tierClass = "tier-$tier"
        $tierLabel = if ($tier -eq 'safe') { '🟢 可安全删' } elseif ($tier -eq 'confirm') { '🟡 需确认' } else { '🔴 禁碰' }
        $sizeStr = if ($f.Size -gt 1GB) { "$([math]::Round($f.Size/1GB,2)) GB" } else { "$([math]::Round($f.Size/1MB,1)) MB" }
        "<tr><td>$($rank++)</td><td>$($f.Path)</td><td>$sizeStr</td><td>$($f.MTime.ToString('yyyy-MM-dd'))</td><td class='$tierClass'>$tierLabel</td></tr>"
    }
)
</table>

<h2>🔄 精确重复（$($exactDups.Count) 组）</h2>
$(
    if ($exactDups.Count -eq 0) {
        "<p>✅ 未发现精确重复文件</p>"
    } else {
        "<table><tr><th>组</th><th>文件数</th><th>单文件大小</th><th>浪费空间</th><th>路径</th></tr>"
        $gi = 0
        foreach ($dup in $exactDups) {
            $gi++
            $wasteStr = if ($dup.TotalWaste -gt 1GB) { "$([math]::Round($dup.TotalWaste/1GB,2)) GB" } else { "$([math]::Round($dup.TotalWaste/1MB,1)) MB" }
            $sizeStr = if ($dup.Size -gt 1GB) { "$([math]::Round($dup.Size/1GB,2)) GB" } else { "$([math]::Round($dup.Size/1MB,1)) MB" }
            "<tr><td>$gi</td><td>$($dup.Count)</td><td>$sizeStr</td><td>$wasteStr</td><td style='font-size:11px;max-width:400px;overflow:hidden;text-overflow:ellipsis;'>$($dup.Files[0].Path)</td></tr>"
        }
        "</table>"
    }
)

<h2>🔍 模糊重复（$($fuzzyDups.Count) 对）</h2>
$(
    if ($fuzzyDups.Count -eq 0) {
        "<p>✅ 未发现模糊重复文件</p>"
    } else {
        "<table><tr><th>#</th><th>文件1</th><th>文件2</th><th>相似度</th><th>大小</th></tr>"
        $fi = 0
        foreach ($fd in $fuzzyDups) {
            $fi++
            $sizeStr = if ($fd.Size2 -gt 1GB) { "$([math]::Round($fd.Size2/1GB,2)) GB" } else { "$([math]::Round($fd.Size2/1MB,1)) MB" }
            "<tr><td>$fi</td><td style='font-size:11px;max-width:300px;overflow:hidden;text-overflow:ellipsis;'>$($fd.File1)</td><td style='font-size:11px;max-width:300px;overflow:hidden;text-overflow:ellipsis;'>$($fd.File2)</td><td>$([math]::Round($fd.Similarity*100,1))%</td><td>$sizeStr</td></tr>"
        }
        "</table>"
    }
)

<h2>🧹 清理建议（三级分类）</h2>
<h3 class="tier-safe">🟢 可安全删（$($cleanupItems | Where-Object Tier -eq 'safe' | Measure-Object | Select-Object -ExpandProperty Count) 项，共 $([math]::Round(($cleanupItems | Where-Object Tier -eq 'safe' | Measure-Object Size -Sum).Sum/1MB,1)) MB）</h3>
<table><tr><th>类型</th><th>路径</th><th>大小</th></tr>
$(
    foreach ($item in ($cleanupItems | Where-Object Tier -eq 'safe' | Sort-Object Size -Descending)) {
        $sizeStr = if ($item.Size -gt 1GB) { "$([math]::Round($item.Size/1GB,2)) GB" } else { "$([math]::Round($item.Size/1MB,1)) MB" }
        $typeLabel = if ($item.Type -eq 'large') { '大文件' } elseif ($item.Type -eq 'duplicate') { '精确重复' } else { '模糊重复' }
        "<tr><td>$typeLabel</td><td style='font-size:11px'>$($item.Path)</td><td>$sizeStr</td></tr>"
    }
)
</table>

<h3 class="tier-confirm">🟡 需确认（$($cleanupItems | Where-Object Tier -eq 'confirm' | Measure-Object | Select-Object -ExpandProperty Count) 项，共 $([math]::Round(($cleanupItems | Where-Object Tier -eq 'confirm' | Measure-Object Size -Sum).Sum/1MB,1)) MB）</h3>
<table><tr><th>类型</th><th>路径</th><th>大小</th></tr>
$(
    foreach ($item in ($cleanupItems | Where-Object Tier -eq 'confirm' | Sort-Object Size -Descending)) {
        $sizeStr = if ($item.Size -gt 1GB) { "$([math]::Round($item.Size/1GB,2)) GB" } else { "$([math]::Round($item.Size/1MB,1)) MB" }
        $typeLabel = if ($item.Type -eq 'large') { '大文件' } elseif ($item.Type -eq 'duplicate') { '精确重复' } else { '模糊重复' }
        "<tr><td>$typeLabel</td><td style='font-size:11px'>$($item.Path)</td><td>$sizeStr</td></tr>"
    }
)
</table>

<h3 class="tier-forbidden">🔴 禁碰（$($cleanupItems | Where-Object Tier -eq 'forbidden' | Measure-Object | Select-Object -ExpandProperty Count) 项）</h3>
<table><tr><th>类型</th><th>路径</th><th>大小</th></tr>
$(
    foreach ($item in ($cleanupItems | Where-Object Tier -eq 'forbidden' | Sort-Object Size -Descending | Select-Object -First 20)) {
        $sizeStr = if ($item.Size -gt 1GB) { "$([math]::Round($item.Size/1GB,2)) GB" } else { "$([math]::Round($item.Size/1MB,1)) MB" }
        $typeLabel = if ($item.Type -eq 'large') { '大文件' } elseif ($item.Type -eq 'duplicate') { '精确重复' } else { '模糊重复' }
        "<tr><td>$typeLabel</td><td style='font-size:11px'>$($item.Path)</td><td>$sizeStr</td></tr>"
    }
)
</table>

<div class="footer">
  <p>⚠️ 清理动作：展示清单 → 用户确认 → 回收站 API（绝不直接删除）</p>
  <p>报告由 Winskill v3.4.0 生成 | 单文件离线可开</p>
</div>
</div>
</body>
</html>
"@

Set-Content -Path $report -Value $html -Encoding utf8
Write-Host "`n✅ 体检完成！报告：$report"
Write-Host "   耗时：$elapsed 分钟 | 精确重复：$($exactDups.Count) 组 | 模糊重复：$($fuzzyDups.Count) 对"
```

### SimHash 辅助函数（在运行上述脚本前需先定义）

```powershell
# ===== SimHash 64 位指纹生成 =====
function Get-SimHash {
    param([string]$Text)
    
    # 分词：按非字母数字中文分割
    $tokens = $Text -split '[^a-z0-9\u4e00-\u9fff]+' | Where-Object { $_ }
    
    # 如果分词为空，用字符级 bigram
    if ($tokens.Count -eq 0) {
        $tokens = @()
        for ($i = 0; $i -lt $Text.Length - 1; $i++) {
            $tokens += $Text.Substring($i, 2)
        }
    }
    
    # 计算 64 位向量
    $vector = @(0) * 64
    foreach ($token in $tokens) {
        $hashBytes = [System.Security.Cryptography.SHA256]::Create().ComputeHash(
            [System.Text.Encoding]::UTF8.GetBytes($token)
        )
        for ($b = 0; $b -lt 8; $b++) {  # 取前 8 字节 = 64 位
            $byteVal = $hashBytes[$b]
            for ($bit = 0; $bit -lt 8; $bit++) {
                $idx = $b * 8 + $bit
                if ($byteVal -band (1 -shl $bit)) {
                    $vector[$idx]++
                } else {
                    $vector[$idx]--
                }
            }
        }
    }
    
    # 生成指纹
    $fingerprint = 0
    for ($i = 0; $i -lt 64; $i++) {
        if ($vector[$i] -gt 0) {
            $fingerprint = $fingerprint -bor (1 -shl $i)
        }
    }
    $fingerprint
}

# ===== SimHash 相似度（1 - 汉明距离/64） =====
function Get-SimHashSimilarity {
    param([long]$Hash1, [long]$Hash2)
    
    $xor = $Hash1 -bxor $Hash2
    $hamming = 0
    $x = [ulong]$xor
    while ($x -ne 0) {
        $hamming++
        $x = $x -band ($x - 1)  # 清除最低位的 1
    }
    return 1.0 - ($hamming / 64.0)
}

# ===== Treemap SVG 生成（简化矩形树图） =====
function Get-TreemapSvg {
    param($DirStats, [int]$Width = 800, [int]$Height = 400)
    
    $totalSize = ($DirStats | Measure-Object Size -Sum).Sum
    if ($totalSize -eq 0) { return "<p>无数据</p>" }
    
    $svg = "<svg width='$Width' height='$Height' viewBox='0 0 $Width $Height'>"
    
    # 颜色方案
    $colors = @('#1a73e8', '#34a853', '#fbbc04', '#ea4335', '#4285f4', '#0f9d58', '#f4b400', '#db4437', '#ab47bc', '#00acc1')
    
    # 简化的 treemap：水平条带布局
    $y = 0
    $i = 0
    foreach ($d in $DirStats) {
        $h = [math]::Max(20, ($d.Size / $totalSize) * $Height)
        if ($y + $h -gt $Height) { $h = $Height - $y }
        if ($h -le 0) { break }
        
        $color = $colors[$i % $colors.Count]
        $sizeStr = if ($d.Size -gt 1GB) { "$([math]::Round($d.Size/1GB,1))GB" } else { "$([math]::Round($d.Size/1MB,0))MB" }
        $label = "$($d.Dir) ($sizeStr)"
        
        $svg += "<rect x='0' y='$y' width='$Width' height='$h' fill='$color' stroke='#fff' stroke-width='1' rx='2'>"
        $svg += "<title>$label</title></rect>"
        
        if ($h -gt 16) {
            $svg += "<text x='8' y='$($y + 14)' fill='#fff' font-size='11' font-family='sans-serif'>$label</text>"
        }
        
        $y += $h
        $i++
        if ($y -ge $Height) { break }
    }
    
    $svg += "</svg>"
    return $svg
}
```

### 34.2 仅查看报告（不重新扫描）

```powershell
$report = "$env:USERPROFILE\.workbuddy\output\winskill\disk_health_report.html"
if (Test-Path $report) {
    Start-Process $report
} else {
    Write-Host "❌ 尚未生成报告，请先运行 34.1 体检"
}
```

### 34.3 清理动作（展示清单 → 确认 → 回收站）

```powershell
# 从报告中提取「可安全删」项，展示后确认清理
$outDir = "$env:USERPROFILE\.workbuddy\output\winskill"
# 实际清理需先运行体检生成报告，然后：
# 1. 展示清单（从 HTML 解析或从体检输出）
# 2. 用户确认
# 3. 用回收站 API 删除
$shell = New-Object -ComObject Shell.Application
# 示例：$shell.NameSpace(0).ParseName("文件路径").InvokeVerb("delete")
Write-Host "⚠️ 清理动作必须：展示清单 → 用户确认 → 回收站 API（绝不直接删除）"
```

### 报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `Access denied` | 权限不足 | 管理员身份运行 PowerShell |
| `文件正在使用` | 文件被占用 | 跳过，不影响整体报告 |
| `报告生成失败` | 磁盘空间不足 | 确保 output 目录有空间 |
| 扫描超时 | 文件过多 | 缩小扫描范围（如只扫 D:\） |

</details>

[↑ 返回顶部](#module-1)

---
