# archive-sessions.ps1
# subagent-archive v3.2 执行脚本（通用化重构版）
# 适配：OpenClaw 2026.6.1+ / PowerShell 5.1+ / PowerShell 7+
# 平台：Windows / macOS / Linux
# 原开发者：丞相团队（v3.0 - v3.1）
# v3.2 重构：OpenClaw Community
# 日期：2026-06-06
#
# 适配：OpenClaw 6.1 新增 --fix-missing / --active-key / --fix-dm-scope
#
# 用法（PowerShell 命名参数，参数名以 - 开头）：
#   .\archive-sessions.ps1 -Agent myagent                          # dry-run（默认）
#   .\archive-sessions.ps1 -Agent myagent -Soft                    # 软删除模式
#   .\archive-sessions.ps1 -Agent myagent -Enforce                 # 硬删除模式
#   .\archive-sessions.ps1 -Agent myagent -Enforce -Json           # 硬删除 + JSON 输出
#   .\archive-sessions.ps1 -Agent myagent -Enforce -FixMissing     # 6.1+ 启用官方反向匹配（默认开启）
#   .\archive-sessions.ps1 -Agent myagent -NoFixMissing            # 6.1 降级到 v3.0 行为
#   .\archive-sessions.ps1 -Agent myagent -FixDmScope              # 6.1+ 修 DM scope
#   .\archive-sessions.ps1 -Agent myagent -ActiveKey "key1","key2" # 6.1+ 保护指定 key
#   .\archive-sessions.ps1 -Agent myagent -WorkspaceDir "C:\path\to\workspace-foo"  # 显式指定 workspace
#
# 注意：PowerShell 不支持 Unix 风格的 --agent=foo 或 --agent foo 语法
# 必须用 -Agent foo（空格分隔），且 -Agent 首字母大写以避免歧义
#
# 退出码：
#   0 = 无操作完成（dry-run 或没有可清理项）
#   1 = 实际清理完成
#   2 = 错误
#
# v3.2 相对 v3.1 关键变化：
#   1. 跨平台路径检测（Win/macOS/Linux + PS 5.1/7+）
#   2. 新增 -WorkspaceDir 参数（默认自动检测，失败时报错引导用户指定）
#   3. 中性化作者署名（原开发者 credit 保留在 README 致谢区）
#   4. 完整保留 v3.1 全部功能（--fix-missing、--active-key、--fix-dm-scope、零匹配守卫、追加写入、dashboard 分流、物理成组清理、软删除）

[CmdletBinding()]
param(
    [string]$Agent = "",
    [switch]$Soft,
    [switch]$Enforce,
    [switch]$DryRun = $true,  # 默认 dry-run
    [switch]$Json,
    # === v3.1 新增（OpenClaw 6.1 适配） ===
    [switch]$FixMissing = $true,   # 6.1+ 调官方 --fix-missing（默认开启）
    [switch]$NoFixMissing,         # 降级到 v3.0 行为（v3.1 兼容选项）
    [switch]$FixDmScope,           # 6.1+ 调官方 --fix-dm-scope
    [string[]]$ActiveKey = @(),   # 6.1+ 透传 --active-key
    # === v3.2 新增（通用化重构） ===
    [string]$WorkspaceDir = ""    # workspace 目录（默认自动检测，失败时需显式指定）
)

# ============================================================
# 0. 颜色输出辅助
# ============================================================

$Color = @{
    Green   = 'Green'
    Red     = 'Red'
    Yellow  = 'Yellow'
    Cyan    = 'Cyan'
    Gray    = 'DarkGray'
    Magenta = 'Magenta'
}

function Write-Color {
    param([string]$Message, [string]$Color = 'White')
    if ($Json) { return }
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success { param([string]$Msg) Write-Color "[OK] $Msg" $Color.Green }
function Write-Error2  { param([string]$Msg) Write-Color "[ERR] $Msg" $Color.Red }
function Write-Warn    { param([string]$Msg) Write-Color "[WARN] $Msg" $Color.Yellow }
function Write-Info    { param([string]$Msg) Write-Color "[INFO] $Msg" $Color.Cyan }
function Write-Skip    { param([string]$Msg) Write-Color "[SKIP] $Msg" $Color.Yellow }
function Write-Debug2  { param([string]$Msg) Write-Color "[DEBUG] $Msg" $Color.Gray }
function Write-Action  { param([string]$Msg) Write-Color "[ACT] $Msg" $Color.Magenta }

# ============================================================
# 1. 参数校验
# ============================================================

if ([string]::IsNullOrWhiteSpace($Agent)) {
    Write-Error2 "必须指定 -Agent <agentId>"
    exit 2
}

# 模式判定
$Mode = if ($Enforce) {
    "enforce"
} elseif ($Soft) {
    "soft"
} else {
    "dry-run"
}

# dry-run 是默认；soft 优先级高于 dry-run；enforce 优先级最高
if ($Enforce -and $Soft) {
    Write-Warn "-Enforce 和 -Soft 同时指定，-Enforce 优先"
    $Mode = "enforce"
}

# v3.1: 冲突检测（-FixMissing 和 -NoFixMissing 不能同时）
if ($FixMissing -and $NoFixMissing) {
    Write-Warn "-FixMissing 和 -NoFixMissing 同时指定，-NoFixMissing 优先（降级到 v3.0 行为）"
    $FixMissing = $false
}

Write-Info "============================================================"
Write-Info "subagent-archive v3.2 执行（通用化重构版，OpenClaw 6.1 适配）"
Write-Info "============================================================"
Write-Info "智能体: $Agent"
Write-Info "模式: $Mode"
Write-Info "OpenClaw 6.1 兼容: FixMissing=$FixMissing, NoFixMissing=$NoFixMissing, FixDmScope=$FixDmScope"
Write-Info "ActiveKey: $($ActiveKey -join ', ')"
Write-Info "时间: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Info ""

# ============================================================
# 2. 路径配置（v3.2 通用化：跨平台 + workspace 自动检测）
# ============================================================

# === v3.2 跨平台 OpenClaw 根目录检测 ===
# - PowerShell 5.1+ on Windows: $env:USERPROFILE
# - PowerShell 7+ on macOS / Linux: $HOME
# - 兼容处理：$IsWindows 仅 PS 6+ 存在，PS 5.1 必须用 $env:OS
$IsWindowsOS = ($env:OS -eq "Windows_NT")
if ($IsWindowsOS) {
    $OpenClawHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
} else {
    $OpenClawHome = $HOME
}
$OpenClawDir = Join-Path $OpenClawHome ".openclaw"
$SessionsDir = Join-Path $OpenClawDir (Join-Path "agents" (Join-Path $Agent "sessions"))

# === v3.2 workspace 目录检测（新增） ===
# 优先级：-WorkspaceDir 显式指定 > 自动扫描 $OpenClawDir\workspace-*
# 自动扫描规则：找带 MEMORY.md 的目录
# - 唯一命中：自动选中
# - 多重命中：报错，引导用户显式指定
# - 零命中：报错，引导用户显式指定
if ($WorkspaceDir -ne "") {
    if (-not (Test-Path $WorkspaceDir)) {
        Write-Error2 "WorkspaceDir 不存在: $WorkspaceDir"
        exit 2
    }
    Write-Info "workspace（显式指定）: $WorkspaceDir"
} else {
    $candidates = @()
    if (Test-Path $OpenClawDir) {
        $wsDirs = Get-ChildItem -Path $OpenClawDir -Directory -Filter "workspace-*" -ErrorAction SilentlyContinue
        foreach ($w in $wsDirs) {
            if (Test-Path (Join-Path $w.FullName "MEMORY.md")) {
                $candidates += $w.FullName
            }
        }
    }
    if ($candidates.Count -eq 0) {
        Write-Error2 "未找到 workspace 目录（扫描 $OpenClawDir\workspace-* 都没找到带 MEMORY.md 的目录）"
        Write-Error2 "请用 -WorkspaceDir <path> 显式指定。例如：-WorkspaceDir (Join-Path `$HOME 'path/to/workspace-foo')"
        exit 2
    } elseif ($candidates.Count -gt 1) {
        Write-Error2 "检测到多个 workspace:"
        foreach ($c in $candidates) {
            Write-Error2 "  - $c"
        }
        Write-Error2 "请用 -WorkspaceDir <path> 显式指定其中一个。"
        exit 2
    } else {
        $WorkspaceDir = $candidates[0]
        Write-Info "workspace（自动检测）: $WorkspaceDir"
    }
}

# 派生路径
$MemoryDir = Join-Path $WorkspaceDir "memory"
$DashboardArchiveDir = Join-Path $MemoryDir "dashboard-archives"
$DateStr = (Get-Date).ToString('yyyy-MM-dd')
$TimeStr = (Get-Date).ToString('yyyy-MM-dd HH:mm')
$LogFile = Join-Path $MemoryDir "$DateStr-subagent-archive-v3.md"

# 校验路径
if (-not (Test-Path $SessionsDir)) {
    Write-Error2 "会话目录不存在: $SessionsDir"
    exit 2
}

if (-not (Test-Path $MemoryDir)) {
    Write-Warn "memory 目录不存在: $MemoryDir，尝试创建"
    New-Item -Path $MemoryDir -ItemType Directory -Force | Out-Null
}

if (-not (Test-Path $DashboardArchiveDir)) {
    New-Item -Path $DashboardArchiveDir -ItemType Directory -Force | Out-Null
    Write-Success "创建 dashboard 归档目录: $DashboardArchiveDir"
}

# ============================================================
# 3. 第 1 步：调用 openclaw sessions cleanup（v3.1 集成 --fix-missing）
# ============================================================

Write-Info ""
Write-Info "========== 第 1 步：原生清理预演（v3.1 集成 6.1 --fix-missing） =========="

# === v3.1：动态构造原生清理命令 ===
$nativeArgs = @("sessions", "cleanup", "--agent", $Agent)

if ($Mode -ne "enforce") {
    $nativeArgs += "--dry-run"
} else {
    $nativeArgs += "--enforce"
}

# 6.1+ 透传 --fix-missing（默认开启，除非 -NoFixMissing）
if ($FixMissing -and -not $NoFixMissing) {
    $nativeArgs += "--fix-missing"
    Write-Info "[v3.1] 集成 6.1 --fix-missing（自动清理 orphan transcript）"
}

# 6.1+ 透传 --fix-dm-scope
if ($FixDmScope) {
    $nativeArgs += "--fix-dm-scope"
    Write-Info "[v3.1] 集成 6.1 --fix-dm-scope"
}

# 6.1+ 透传 --active-key（多次，一次一个值）
foreach ($key in $ActiveKey) {
    $nativeArgs += "--active-key"
    $nativeArgs += $key
    Write-Info "[v3.1] 透传 6.1 --active-key: $key"
}

Write-Info "执行命令: openclaw $($nativeArgs -join ' ')"

# 执行原生清理
$nativeOutput = & openclaw @nativeArgs 2>&1 | Out-String

if ($Mode -ne "enforce") {
    Write-Debug2 "原生清理输出（前 20 行）:"
    $nativeOutput -split "`n" | Select-Object -First 20 | ForEach-Object { Write-Debug2 $_ }
} else {
    Write-Info "原生清理 enforce 模式输出:"
    $nativeOutput -split "`n" | Select-Object -First 20 | ForEach-Object { Write-Debug2 $_ }
}

# 解析原生清理结果
$nativeRemoveCount = 0
if ($nativeOutput -match 'Would prune unreferenced artifacts:\s*(\d+)') {
    $nativeRemoveCount = [int]$Matches[1]
}

if ($Mode -eq "enforce") {
    Write-Info "原生清理（enforce）已执行"
} else {
    Write-Info "原生清理将处理: $nativeRemoveCount 个 unreferenced artifacts（仅预演）"
    if ($FixMissing -and -not $NoFixMissing) {
        Write-Info "[v3.1] 6.1 --fix-missing 将在 enforce 模式自动清 orphan transcript"
    }
}

# ============================================================
# 4. 第 2 步：扫描 sessions.json，识别目标会话
# ============================================================

Write-Info ""
Write-Info "========== 第 2 步：扫描 sessions.json 索引 =========="

$SessionsFile = Join-Path $SessionsDir "sessions.json"
if (-not (Test-Path $SessionsFile)) {
    Write-Error2 "sessions.json 不存在: $SessionsFile"
    exit 2
}

# 备份 sessions.json（如果 enforce 模式）
if ($Mode -eq "enforce") {
    $BackupFile = "$SessionsFile.backup-$DateStr-$((Get-Date).ToString('HHmmss'))"
    Copy-Item $SessionsFile $BackupFile -Force
    Write-Success "sessions.json 备份: $BackupFile"
}

$sessionsJson = Get-Content $SessionsFile -Raw | ConvertFrom-Json

$protectedKeys = @()
$candidateKeys = @()
$dashboardDoneParents = @()

foreach ($prop in $sessionsJson.PSObject.Properties) {
    $key = $prop.Name
    $value = $prop.Value

    # 主会话保护
    if ($key -match ':main$') {
        $protectedKeys += $key
        Write-Skip "主会话保护: $key"
        continue
    }

    # cron 任务保护
    if ($key -match ':cron:') {
        $protectedKeys += $key
        Write-Skip "cron 任务保护: $key"
        continue
    }

    # v3.1: ActiveKey 额外保护（6.1 --active-key 透传）
    if ($ActiveKey -and ($key -in $ActiveKey -or ($ActiveKey | Where-Object { $key -like $_ }))) {
        $protectedKeys += $key
        Write-Skip "ActiveKey 保护: $key"
        continue
    }

    # dashboard 父会话 status 分流
    if ($key -match ':dashboard:') {
        $status = $value.status
        if ($status -eq 'done') {
            $dashboardDoneParents += $key
            Write-Info "dashboard 父会话 (done) 加入候选: $key"
        } else {
            $protectedKeys += $key
            Write-Skip "dashboard 父会话非 done 状态 ($status) 跳过: $key"
        }
        continue
    }

    # direct 子会话（空壳 < 1KB 或孤立）
    $sessionFile = $value.sessionFile
    if ($sessionFile) {
        $fullPath = if ([System.IO.Path]::IsPathRooted($sessionFile)) {
            $sessionFile
        } else {
            Join-Path $SessionsDir $sessionFile
        }
        $fileExists = Test-Path $fullPath
        if (-not $fileExists) {
            $candidateKeys += $key
            Write-Info "会话文件不存在，加入候选: $key -> $sessionFile"
        } else {
            $fileInfo = Get-Item $fullPath
            if ($fileInfo.Length -lt 1024) {
                $candidateKeys += $key
                Write-Info "空壳会话 (< 1KB)，加入候选: $key ($($fileInfo.Length) bytes)"
            } else {
                Write-Debug2 "正常会话，跳过: $key ($($fileInfo.Length) bytes)"
            }
        }
    } else {
        # 孤儿 key（无 sessionFile）
        $candidateKeys += $key
        Write-Info "孤儿 key (无 sessionFile)，加入候选: $key"
    }
}

# 2.1 额外扫描：识别磁盘上未被 sessions.json 引用的孤儿 .jsonl 文件
Write-Debug2 "扫描磁盘上的 orphan 物理文件..."
$referencedFiles = @()
$referencedSessionIds = @()
foreach ($prop in $sessionsJson.PSObject.Properties) {
    $sf = $prop.Value.sessionFile
    if ($sf) {
        $referencedFiles += (Split-Path $sf -Leaf)
        $id = [System.IO.Path]::GetFileNameWithoutExtension($sf)
        $referencedSessionIds += $id
    }
}

function Get-BaseSessionId {
    param([string]$FileName)
    $base = $FileName -replace '\.jsonl$', ''
    $base = $base -replace '\.trajectory(\.jsonl)?$', ''
    $base = $base -replace '\.trajectory-path(\.json)?$', ''
    $base = $base -replace '\.jsonl\.checkpoint\..+$', ''
    $base = $base -replace '\.jsonl\.reset\..+$', ''
    $base = $base -replace '\.jsonl\.deleted\..+$', ''
    $base = $base -replace '\.deleted\..+$', ''
    return $base
}

$orphanPhysicalFiles = @()
Get-ChildItem -Path $SessionsDir -Filter "*.jsonl" -Force -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.Name -eq "sessions.json") { return }
    if ($_.Name -in $referencedFiles) { return }
    $baseId = Get-BaseSessionId $_.Name
    if ($baseId -in $referencedSessionIds) {
        Write-Debug2 "归属被引用会话，跳过: $($_.Name) (baseId=$baseId)"
        return
    }
    $orphanPhysicalFiles += $_
    Write-Info "未引用物理文件: $($_.Name) ($($_.Length) bytes, baseId=$baseId)"
}

Write-Info ""
Write-Info "汇总："
Write-Info "  - 受保护 key: $($protectedKeys.Count) 个"
Write-Info "  - dashboard done 父会话: $($dashboardDoneParents.Count) 个"
Write-Info "  - 其他候选会话: $($candidateKeys.Count) 个"
Write-Info "  - 磁盘孤儿物理文件: $($orphanPhysicalFiles.Count) 个"

# ============================================================
# 5. 第 3 步：dashboard 父会话归档（追加写入）
# ============================================================

Write-Info ""
Write-Info "========== 第 3 步：dashboard 父会话归档（追加写入） =========="

foreach ($parentKey in $dashboardDoneParents) {
    $sessionId = ($parentKey -split ':')[-1]

    $dashboardFile = Join-Path $DashboardArchiveDir "$DateStr-dashboard-$sessionId.md"

    if (Test-Path $dashboardFile) {
        Write-Skip "dashboard 归档已存在: $dashboardFile"
        continue
    }

    $parentValue = $sessionsJson.$parentKey
    $parentFile = $parentValue.sessionFile
    $parentSize = 0
    $parentCreatedAt = $parentValue.createdAt
    if ($parentFile) {
        $parentFullPath = if ([System.IO.Path]::IsPathRooted($parentFile)) {
            $parentFile
        } else {
            Join-Path $SessionsDir $parentFile
        }
        if (Test-Path $parentFullPath) {
            $parentSize = (Get-Item $parentFullPath).Length
        }
    }

    New-Item -Path $dashboardFile -ItemType File -Force | Out-Null
    Add-Content -Path $dashboardFile -Value @"
# Dashboard 父会话归档（v3.2）

**Session Key**: $parentKey
**Session ID**: $sessionId
**归档时间**: $TimeStr
**归档原因**: status=done，会话已结束
**归档模式**: $Mode
**OpenClaw 兼容**: 6.1+ 集成 --fix-missing
**归档版本**: subagent-archive v3.2

## 父会话元数据

- **父会话文件**: $parentFile
- **父会话文件大小**: $parentSize bytes ($(if ($parentSize -gt 0) { [math]::Round($parentSize / 1KB, 2) } else { 0 }) KB)
- **创建时间**: $parentCreatedAt
- **状态**: done
- **归档执行**: 自动归档（v3.2）

## 关键说明

- dashboard 父会话包含 control-ui 的状态展示
- status=done 表示任务已结束，可安全归档
- 物理文件清理由 archive-sessions.ps1 统一执行
"@
    Write-Success "dashboard 归档创建: $dashboardFile"
}

# ============================================================
# 6. 第 4 步：结构化归档日志（追加写入）
# ============================================================

Write-Info ""
Write-Info "========== 第 4 步：当日归档日志（追加写入） =========="

if (-not (Test-Path $LogFile)) {
    New-Item -Path $LogFile -ItemType File -Force | Out-Null
    Add-Content -Path $LogFile -Value "# 子会话归档日志 (subagent-archive v3.2)"
    Add-Content -Path $LogFile -Value ""
    Add-Content -Path $LogFile -Value "**创建时间**: $TimeStr  **维护**: 自动归档  **版本**: v3.2 (OpenClaw 6.1 适配 + 通用化重构)"
    Add-Content -Path $LogFile -Value ""
}

Add-Content -Path $LogFile -Value ""
Add-Content -Path $LogFile -Value "---"
Add-Content -Path $LogFile -Value ""
Add-Content -Path $LogFile -Value "## 📋 系统管理操作（v3.2）"
Add-Content -Path $LogFile -Value ""
Add-Content -Path $LogFile -Value "### 归档执行"
Add-Content -Path $LogFile -Value "- **时间**: $TimeStr"
Add-Content -Path $LogFile -Value "- **模式**: $Mode"
Add-Content -Path $LogFile -Value "- **目标智能体**: $Agent"
Add-Content -Path $LogFile -Value "- **workspace**: $WorkspaceDir"
Add-Content -Path $LogFile -Value "- **受保护 key 数**: $($protectedKeys.Count)"
Add-Content -Path $LogFile -Value "- **dashboard done 父会话数**: $($dashboardDoneParents.Count)"
Add-Content -Path $LogFile -Value "- **其他候选会话数**: $($candidateKeys.Count)"
Add-Content -Path $LogFile -Value "- **OpenClaw 6.1 兼容**: FixMissing=$FixMissing, FixDmScope=$FixDmScope, ActiveKey=$($ActiveKey -join ',')"
Add-Content -Path $LogFile -Value ""

Add-Content -Path $LogFile -Value "### 受保护 key 列表"
foreach ($k in $protectedKeys) {
    Add-Content -Path $LogFile -Value "- $k"
}
Add-Content -Path $LogFile -Value ""

if ($dashboardDoneParents.Count -gt 0) {
    Add-Content -Path $LogFile -Value "### Dashboard 父会话归档"
    foreach ($parentKey in $dashboardDoneParents) {
        $sessionId = ($parentKey -split ':')[-1]
        Add-Content -Path $LogFile -Value "| $parentKey | $DateStr-dashboard-$sessionId.md | done |"
    }
    Add-Content -Path $LogFile -Value ""
}

Write-Success "日志已追加: $LogFile"

# ============================================================
# 7. 第 5 步：物理文件清理（v3.0 关键改进，v3.1/v3.2 保留）
# ============================================================

Write-Info ""
Write-Info "========== 第 5 步：物理文件清理 =========="

$totalFreed = 0
$cleanedCount = 0
$allTargets = @($dashboardDoneParents + $candidateKeys)

# 7.1 先处理孤儿物理文件（最直接）
foreach ($orphan in $orphanPhysicalFiles) {
    $size = $orphan.Length
    if ($Mode -eq "enforce") {
        Remove-Item $orphan.FullName -Force -ErrorAction SilentlyContinue
        Write-Success "硬删除孤儿文件: $($orphan.Name) ($size bytes)"
    } elseif ($Mode -eq "soft") {
        $timestamp = (Get-Date).ToString('yyyy-MM-ddTHH-mm-ss.fffZ')
        $newName = "$($orphan.BaseName).deleted.$timestamp$($orphan.Extension)"
        Rename-Item -Path $orphan.FullName -NewName $newName -ErrorAction SilentlyContinue
        Write-Warn "软删除孤儿文件: $($orphan.Name) -> $newName"
    } else {
        Write-Action "[dry-run] 将删除孤儿: $($orphan.Name) ($size bytes)"
    }
    $totalFreed += $size
    $cleanedCount++
}

foreach ($key in $allTargets) {
    $sessionId = ($key -split ':')[-1]

    $patterns = @(
        "$sessionId.jsonl",
        "$sessionId.trajectory.jsonl",
        "$sessionId.trajectory-path.json",
        "$sessionId.jsonl.checkpoint.*.jsonl",
        "$sessionId.jsonl.reset.*",
        "$sessionId.jsonl.deleted.*"
    )

    foreach ($pattern in $patterns) {
        $files = Get-ChildItem -Path $SessionsDir -Filter $pattern -Force -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            $size = $file.Length
            if ($Mode -eq "enforce") {
                Remove-Item $file.FullName -Force -ErrorAction SilentlyContinue
                Write-Success "硬删除: $($file.Name) ($size bytes)"
            } elseif ($Mode -eq "soft") {
                $timestamp = (Get-Date).ToString('yyyy-MM-ddTHH-mm-ss.fffZ')
                $newName = "$($file.BaseName).deleted.$timestamp$($file.Extension)"
                Rename-Item -Path $file.FullName -NewName $newName -ErrorAction SilentlyContinue
                Write-Warn "软删除: $($file.Name) -> $newName"
            } else {
                Write-Action "[dry-run] 将删除: $($file.Name) ($size bytes)"
            }
            $totalFreed += $size
            $cleanedCount++
        }
    }
}

$freedMB = [math]::Round($totalFreed / 1MB, 2)
Write-Info ""
Write-Info "物理文件汇总："
Write-Info "  - 处理文件数: $cleanedCount"
Write-Info "  - 释放空间: $freedMB MB ($totalFreed bytes)"

# ============================================================
# 8. 第 6 步：清理 sessions.json 索引（v3.1 升级：双保险 + 零匹配守卫）
# ============================================================

Write-Info ""
Write-Info "========== 第 6 步：清理 sessions.json 索引（v3.1 双保险） =========="

# 重新读取（因为可能改变了）
$sessionsJson = Get-Content $SessionsFile -Raw | ConvertFrom-Json

$staleKeys = @()
$abnormalKeys = @()  # v3.1 新增：status 缺失等异常（仅记录，不自动清）

foreach ($prop in $sessionsJson.PSObject.Properties.Copy) {
    $entry = $prop.Value
    $keyName = $prop.Name

    # 跳过受保护 key
    if ($keyName -in $protectedKeys) { continue }
    if ($keyName -match ':main$') { continue }
    if ($keyName -match ':cron:') { continue }
    if ($keyName -match ':dashboard:' -and $entry.status -ne 'done') { continue }

    # v3.1 新增：检测"status 字段缺失但文件存在"的异常
    # 这是 v3.0 的盲区——v3.0 只看 status 字段，漏掉"无 status + 有 transcript"的异常
    if (-not $entry.status -and $entry.sessionFile -and (Test-Path $entry.sessionFile)) {
        $abnormalKeys += $keyName
        Write-Warn "异常条目：$keyName 缺 status 字段（v3.0 盲区，v3.1/v3.2 检测但不自动清）"
        # 不加入 $staleKeys，留给主公决定
    }

    # 检测孤儿条目（v3.0 已有逻辑，官方 --fix-missing 已经在第 1 步清过）
    if ($entry.sessionFile -and -not (Test-Path $entry.sessionFile)) {
        $staleKeys += $keyName
        Write-Action "发现 orphan key: $keyName"
    }
}

Write-Info ""
Write-Info "v3.2 第 6 步结果："
Write-Info "  - stale/orphan key: $($staleKeys.Count) 个"
Write-Info "  - abnormal key (status 缺失): $($abnormalKeys.Count) 个（仅记录，不自动清）"

# === v3.1 零匹配守卫（v3.0 修复的 bug，不能重蹈覆辙，v3.2 保留） ===
if ($Mode -eq "enforce") {
    if ($staleKeys.Count -gt 0) {
        # 强制备份
        $backupPath = "$SessionsFile.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-v32step6"
        Copy-Item $SessionsFile $backupPath
        Write-Success "已备份: $backupPath"

        # 删除 stale keys
        foreach ($key in $staleKeys) {
            $sessionsJson.PSObject.Properties.Remove($key) | Out-Null
        }

        # 重写
        $sessionsJson | ConvertTo-Json -Depth 20 | Set-Content $SessionsFile -NoNewline -Encoding UTF8
        Write-Success "已清理 $($staleKeys.Count) 个 stale key"
    } else {
        # v3.0/3.1/3.2 零匹配守卫：零匹配时**不重写** sessions.json
        Write-Info "无需重写 sessions.json（无 stale key，零匹配守卫生效）"
    }
} else {
    Write-Warn "[dry-run] 将清理 $($staleKeys.Count) 个 stale key（未执行）"
    foreach ($k in $staleKeys) {
        Write-Action "  - $k"
    }
}

# 记录 abnormal key 到日志
if ($abnormalKeys.Count -gt 0) {
    Add-Content -Path $LogFile -Value "### 异常条目（status 缺失，v3.0 盲区，v3.1/v3.2 检测）"
    foreach ($k in $abnormalKeys) {
        Add-Content -Path $LogFile -Value "- $k"
    }
    Add-Content -Path $LogFile -Value ""
}

# ============================================================
# 9. 最终汇总报告
# ============================================================

Write-Info ""
Write-Info "============================================================"
Write-Info "v3.2 执行汇总"
Write-Info "============================================================"

if ($Json) {
    $result = @{
        mode = $Mode
        agent = $Agent
        version = "v3.2"
        workspace = $WorkspaceDir
        openclawCompatibility = @{
            fixMissing = $FixMissing
            noFixMissing = $NoFixMissing
            fixDmScope = $FixDmScope
            activeKey = $ActiveKey
        }
        protectedKeys = $protectedKeys.Count
        dashboardParents = $dashboardDoneParents.Count
        candidates = $candidateKeys.Count
        filesCleaned = $cleanedCount
        freedMB = $freedMB
        staleKeys = $staleKeys.Count
        abnormalKeys = $abnormalKeys.Count
        logFile = $LogFile
    }
    $result | ConvertTo-Json -Depth 5
} else {
    Write-Info "智能体: $Agent"
    Write-Info "模式: $Mode"
    Write-Info "版本: v3.2 (OpenClaw 6.1 适配 + 通用化重构)"
    Write-Info "workspace: $WorkspaceDir"
    Write-Info "受保护 key: $($protectedKeys.Count)"
    Write-Info "Dashboard done 父会话: $($dashboardDoneParents.Count)"
    Write-Info "其他候选会话: $($candidateKeys.Count)"
    Write-Info "处理文件数: $cleanedCount"
    Write-Info "释放空间: $freedMB MB"
    Write-Info "Stale key: $($staleKeys.Count)"
    Write-Info "Abnormal key: $($abnormalKeys.Count) (仅记录，不自动清)"
    Write-Info "日志文件: $LogFile"
    Write-Info ""
}

# 追加汇总到日志
Add-Content -Path $LogFile -Value "### 执行汇总"
Add-Content -Path $LogFile -Value "- **版本**: v3.2 (OpenClaw 6.1 适配 + 通用化重构)"
Add-Content -Path $LogFile -Value "- **处理文件数**: $cleanedCount"
Add-Content -Path $LogFile -Value "- **释放空间**: $freedMB MB"
Add-Content -Path $LogFile -Value "- **Stale key 数**: $($staleKeys.Count)"
Add-Content -Path $LogFile -Value "- **Abnormal key 数**: $($abnormalKeys.Count)"
Add-Content -Path $LogFile -Value "- **结果**: v3.2 归档完成"
Add-Content -Path $LogFile -Value ""

# 退出码
if ($Mode -eq "enforce" -and ($cleanedCount -gt 0 -or $staleKeys.Count -gt 0)) {
    exit 1  # 实际清理完成
} else {
    exit 0  # 无操作完成（dry-run 或没东西可清）
}
