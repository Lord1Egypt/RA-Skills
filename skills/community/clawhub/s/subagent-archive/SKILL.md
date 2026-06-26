---
name: subagent-archive
version: 3.2.0
updated: 2026-06-06
author: OpenClaw Community
original_developers: 丞相团队 (v3.0 - v3.1)
description: 安全归档/清理子会话的标准操作流程（跨平台 + workspace 可配置 + 原生清理 + dashboard 父会话分流 + 反向匹配索引清理 + 软删除 + OpenClaw 6.1 适配）
tags: [操作流程, 系统管理, 会话清理, 三层防御, OpenClaw 6.1, 跨平台]
compatibility:
  - OpenClaw 2026.5.26+ (基础功能)
  - OpenClaw 2026.6.1+ (--fix-missing, --active-key 增强)
  - PowerShell 5.1+ (Windows PowerShell)
  - PowerShell 7+ (PowerShell Core，跨平台 Win/macOS/Linux)
---

# 子会话安全归档技能 v3.2

## 🌐 OpenClaw 版本兼容矩阵

| 功能 | 5.26 | 6.1+ | v3.2 处理 |
|------|------|------|-----------|
| 会话 lock 释放修复 | ❌ | ✅ | 6.1+ 自动获益 |
| `--fix-missing` 反向匹配 | ❌ | ✅ | v3.2 优先调官方 + 自写补盲区 |
| `--active-key` 保护 | ❌ | ✅ | v3.2 透传 |
| `--fix-dm-scope` 修 DM | ✅ | ✅ | v3.2 透传 |
| `export-trajectory` 脱敏 | ❌ | ✅ | 与 v3.0 无关（语义化归档仍是 v3.0 独家）|

**核心设计原则**：v3.0+ 永远保留 dashboard 父会话归档、物理文件清理、软删除、归档到 memory/ 等 6.1 没提供的功能。v3.1+ 的升级是"集成"而不是"替换"。

**v3.1 → v3.2 升级要点**：
- 跨平台路径检测（Windows / macOS / Linux）
- 跨 PowerShell 版本支持（5.1 / 7+）
- 新增 `-WorkspaceDir` 参数（默认自动检测唯一 workspace，多 workspace 时引导用户显式指定）
- 中性化作者署名（原开发者 credit 保留在 README 致谢区）
- 完整保留 v3.1 全部功能

## 🌍 平台兼容矩阵（v3.2 新增）

| 平台 | PowerShell | 状态 |
|------|-----------|------|
| Windows | PowerShell 5.1 (Desktop) | ✅ 已测试 |
| Windows | PowerShell 7+ (Core) | ✅ 代码兼容（测试待办） |
| macOS | PowerShell 7+ (Core) | ✅ 代码兼容（测试待办） |
| Linux | PowerShell 7+ (Core) | ✅ 代码兼容（测试待办） |

> 路径检测逻辑：
> - PS 5.1 on Windows：`$env:USERPROFILE` → `~/.openclaw`
> - PS 7+ on Win/macOS/Linux：`$HOME` → `~/.openclaw`

## 功能说明

当需要清理/归档子会话时，必须按照本技能定义的标准流程执行，确保：
1. 内容被正确保存
2. 敏感信息不泄露
3. 原始文件被安全清理
4. **主会话永久保留**（`:main` 绝对不动）
5. **cron 任务永久保留**（`:cron:*` 活跃任务不动，只清过期）
6. **dashboard 父会话按 status 分流**（status=done 才归档，running/活跃永远不动）
7. **归档记录追加写入，不覆盖原有记录**
8. **OpenClaw 6.1 适配**：第 1 步优先调官方 `--fix-missing`，再用自写补盲区（双保险）
9. **跨平台支持（v3.2）**：自动检测 workspace 目录，跨 Win/macOS/Linux

## ⚠️ v3.2 相对 v3.1 的关键改进

| 改进点 | v3.1 行为 | v3.2 行为 |
|--------|---------|-----------|
| **跨平台路径** | 硬编码 Windows + 单一用户路径 | 自动检测用户主目录，支持 Win/macOS/Linux + PS 5.1/7+ |
| **workspace 检测** | 硬编码单一 workspace 路径 | 新增 `-WorkspaceDir` 参数；默认扫描 `~/.openclaw/workspace-*` 找带 `MEMORY.md` 的目录 |
| **多 workspace 处理** | 不支持 | 唯一命中自动选中；多重命中报错引导用户用 `-WorkspaceDir` 显式指定 |
| **作者署名** | 强绑定特定工作区和开发者 | "OpenClaw Community"（中性）；原开发者 credit 在 README 致谢区 |
| **示例 agent** | `-Agent <私有 agent>` | `-Agent myagent`（中性占位） |
| **v3.1 独有功能** | 全部保留 | dashboard 父会话归档、软删除、归档到 memory/、--fix-missing/--active-key/--fix-dm-scope 全部保留 |

## ⚠️ v3.1 相对 v3.0 的关键改进

| 改进点 | v3.0 行为 | v3.1 行为 |
|--------|---------|-----------|
| **OpenClaw 6.1 兼容** | 不识别 6.1 新参数 | 第 1 步自动加 `--fix-missing`，第 6 步集成官方反向匹配 |
| **orphan 检测覆盖** | 只看 `status` 字段，漏"无 status + 无 transcript"孤儿 | 6.1 官方 `--fix-missing` 一步清 + 自写补 status 缺失 |
| **active-key 保护** | 硬编码保护 `:main` / `:cron:` / `:dashboard:` | 支持 6.1 `--active-key <key>` 透传任意 key |
| **dm-scope 修复** | 不处理 DM scope | 6.1 `--fix-dm-scope` 透传 |
| **降级兼容** | 无 | `-NoFixMissing` 开关：6.1 不可用时降级到 v3.0 行为 |
| **v3.0 独有功能** | 全部保留 | dashboard 父会话归档、软删除、归档到 memory/ 全部保留 |

## ⚠️ v3.0 之前的关键改进（保留）

| 改进点 | v1.1.0 行为 | v3.0 行为 |
|--------|------------|-----------|
| **物理文件清理** | 只删 `.jsonl` 单一文件 | 按 `sessionId.*` 成组删除，覆盖 `.jsonl` / `.trajectory.jsonl` / `.trajectory-path.json` / `.jsonl.checkpoint.<id>.jsonl` / `.jsonl.reset.<ts>` / `.jsonl.deleted.<ts>` |
| **sessions.json 索引清理** | 用 `:main$` 粗暴过滤，可能误杀其他后缀 | **反向匹配**：只清理 `sessionFile` 已不存在的 key |
| **dashboard 父会话处理** | 没有特殊处理，依赖通用规则 | **status 分流**：status=done 父会话 + 空壳子会话 + 派生子会话可归档；status=running/活跃永远不动 |
| **保护 key** | 只保护 `:main` | 保护 `:main`、`:cron:*`（除过期）、`:dashboard:*`（除 done） |
| **模式支持** | 只有硬删除 | 支持 `dry-run`（默认）、`enforce`（真删）、`soft`（重命名为 `.deleted.<timestamp>`） |
| **追加写入铁律** | 写在第 3/4 步 | **仍为铁律**：第 3/4 步必须 `Add-Content`，禁止 `write/Set-Content` |
| **dashboard 父会话归档** | 不归档 | 归档到 `memory/dashboard-archives/YYYY-MM-DD-dashboard-<sessionId>.md` |

---

## ⚠️ 写入规则（铁律）

**第 3 步和第 4 步必须使用追加写入（`Add-Content`），禁止使用覆盖写入（`write/Set-Content`）！**

**理由**：
- 覆盖写入会删除文件中之前已有的归档记录，导致历史归档信息丢失
- AGENTS.md 2026-04-26 铁律明确要求追加写入
- 同日多次执行 v3.2 脚本时，文件会持续累积，不会丢失历史

**例外**：
- 物理文件清理、sessions.json 重写：用 `Set-Content` 是允许的（必须用原子重写）
- 创建新文件：用 `New-Item`
- v3.1+ 第 6 步的"零匹配守卫"：零匹配时**不调用 Set-Content**（参考 ERR-20260606-001）

---

## 完整操作流程（6 步 + v3.1 双保险第 6 步）

### 第 0 步：路径配置（v3.2 新增章节）

**目标**：跨平台检测 OpenClaw 根目录、workspace 目录、memory 目录、dashboard 归档目录。

```powershell
# === 跨平台 OpenClaw 根目录检测 ===
$IsWindowsOS = ($env:OS -eq "Windows_NT")
if ($IsWindowsOS) {
    $OpenClawHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
} else {
    $OpenClawHome = $HOME
}
$OpenClawDir = Join-Path $OpenClawHome ".openclaw"
$SessionsDir = Join-Path $OpenClawDir "agents/$Agent/sessions"

# === workspace 目录检测（v3.2 新增） ===
# 优先级：-WorkspaceDir 显式指定 > 自动扫描 $OpenClawDir\workspace-*
# 自动扫描规则：找带 MEMORY.md 的目录
# - 唯一命中：自动选中
# - 多重命中：报错引导用户显式指定
# - 零命中：报错引导用户显式指定
if ($WorkspaceDir -ne "") {
    # 显式指定，直接用
} else {
    $candidates = @()
    $wsDirs = Get-ChildItem -Path $OpenClawDir -Directory -Filter "workspace-*"
    foreach ($w in $wsDirs) {
        if (Test-Path (Join-Path $w.FullName "MEMORY.md")) {
            $candidates += $w.FullName
        }
    }
    if ($candidates.Count -eq 0) { Write-Error "未找到 workspace 目录"; exit 2 }
    elseif ($candidates.Count -gt 1) { Write-Error "检测到多个 workspace"; exit 2 }
    else { $WorkspaceDir = $candidates[0] }
}

$MemoryDir = Join-Path $WorkspaceDir "memory"
$DashboardArchiveDir = Join-Path $MemoryDir "dashboard-archives"
```

**多 workspace 错误信息示例**：
```
[ERR] 检测到多个 workspace:
[ERR]   - /home/user/.openclaw/workspace-alpha
[ERR]   - /home/user/.openclaw/workspace-beta
[ERR] 请用 -WorkspaceDir <path> 显式指定其中一个。
```

---

### 第 1 步：内容提取与状态判定

**目标**：识别目标会话的类型（direct/cron/dashboard）和状态（running/done/idle）。

**v3.1+ 新增**：第 1 步**优先调 OpenClaw 6.1 官方 `--fix-missing`**（识别"transcript 文件不存在"的孤儿），第 1 步**还支持 `--active-key` / `--fix-dm-scope` 透传**。

```powershell
# 1.1 构造原生清理命令（v3.1 自动加 --fix-missing）
$nativeArgs = @("sessions", "cleanup", "--agent", $Agent, "--dry-run")
if ($FixMissing -and -not $NoFixMissing) { $nativeArgs += "--fix-missing" }
if ($FixDmScope) { $nativeArgs += "--fix-dm-scope" }
foreach ($key in $ActiveKey) { $nativeArgs += "--active-key"; $nativeArgs += $key }
$nativeOutput = & openclaw @nativeArgs 2>&1 | Out-String

# 1.2 列出所有会话，识别 dashboard 父会话
$allKeys = openclaw sessions --agent <agentId> --json | ConvertFrom-Json

# 1.3 对每个候选会话，读取状态（status 字段）
foreach ($entry in $allKeys) {
    $key = $entry.key
    $status = $entry.status  # running | done | idle | unknown
    $kind = $entry.kind      # direct | cron | dashboard | ...

    # dashboard 父会话的 status=done 才归档，status=running/idle 跳过
    if ($key -match ':dashboard:') {
        if ($status -ne 'done') {
            Write-Host "[跳过] $key - dashboard 父会话非 done 状态 ($status)" -ForegroundColor Yellow
            continue
        }
    }

    # cron 任务保护（除非已过期）
    if ($key -match ':cron:') {
        Write-Host "[跳过] $key - cron 任务受保护" -ForegroundColor Yellow
        continue
    }

    # 主会话保护
    if ($key -match ':main$') {
        Write-Host "[跳过] $key - 主会话受保护" -ForegroundColor Yellow
        continue
    }
}
```

**dashboard 父会话识别规则**：
- key 以 `:dashboard:` 开头
- 父会话的 `status=done`（任务结束）
- 父会话的所有派生子会话（如有）也归档
- 子会话若是空壳（文件 < 1KB），也可归档

**v3.1+ `--fix-missing` 行为说明**：
- 6.1 官方 `--fix-missing` 会**绕过 age/count retention 限制**，直接清"transcript 文件不存在"的孤儿
- v3.0 第 6 步只检查 `status` 字段，漏掉了"无 status + 无 transcript"的孤儿——这正是 6.1 `--fix-missing` 补的
- v3.1+ 第 1 步先调官方，第 6 步再用自写逻辑补 status 缺失等其他异常（双保险）

**输出**：
- 待归档会话列表（带类型、状态、大小）
- 受保护的 key 列表（:main / :cron:* / 活跃 dashboard / `--active-key` 指定的 key）
- 6.1 官方清理报告（如果有 `--fix-missing`）

---

### 第 2 步：安全分析

对每个待归档会话做内容审查：
- 是否包含敏感信息（密码、密钥、个人隐私）→ 立刻停止，汇报操作员
- 是否有重要成果（大版本升级、关键交付）→ 完整提取关键内容
- 是否有错误教训（值得记录到 .learnings/ERRORS.md）→ 提取错误摘要

**输出**：安全分析结论（pass / hold / special）

---

### 第 3 步：结构化归档（追加写入）

在 `<workspace>/memory/YYYY-MM-DD-subagent-archive-v3.md` 中**追加**归档记录：

```powershell
$archiveFile = Join-Path $MemoryDir "$DateStr-subagent-archive-v3.md"

# 先检查文件是否存在，没有则创建
if (-not (Test-Path $archiveFile)) {
    New-Item -Path $archiveFile -ItemType File -Force | Out-Null
    Add-Content -Path $archiveFile -Value "# 子会话归档日志 (v3.2)`n"
}

# 检查是否已存在该 sessionId 的归档记录
$sessionId = '<具体 sessionId>'
$existing = Select-String -Path $archiveFile -Pattern $sessionId -SimpleMatch -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[跳过归档] $sessionId - 已存在归档记录" -ForegroundColor Yellow
} else {
    # 追加归档记录
    Add-Content -Path $archiveFile -Value @"

## ✅ 安全归档记录（$((Get-Date).ToString('yyyy-MM-dd HH:mm'))执行）

| 智能体 | 会话类型 | 归档文件 | 大小 | 归档时间戳 |
|--------|----------|----------|------|-----------|
| $agentId | $kind | $sessionId.jsonl | $size | $((Get-Date).ToString('yyyy-MM-dd HH:mm')) |

### 会话内容摘要
- **用途**：$purpose
- **创建时间**：$createdAt
- **最后活跃**：$lastActive
- **结果**：$result
"@
}
```

**dashboard 父会话特殊处理**：归档到 `<workspace>/memory/dashboard-archives/YYYY-MM-DD-dashboard-<sessionId>.md`：

```powershell
$dashboardDir = Join-Path $MemoryDir "dashboard-archives"
if (-not (Test-Path $dashboardDir)) {
    New-Item -Path $dashboardDir -ItemType Directory -Force | Out-Null
}
$dashboardFile = Join-Path $dashboardDir "$DateStr-dashboard-$sessionId.md"
if (-not (Test-Path $dashboardFile)) {
    New-Item -Path $dashboardFile -ItemType File -Force | Out-Null
    Add-Content -Path $dashboardFile -Value @"
# Dashboard 父会话归档

**Session ID**: $sessionId
**归档时间**: $((Get-Date).ToString('yyyy-MM-dd HH:mm'))
**归档原因**: status=done，会话已结束
"@
}
```

**关键点**：
- ✅ 使用 `Add-Content` 追加写入
- ❌ 禁止使用 `write/Set-Content` 覆盖
- ✅ 先检查是否已存在记录，避免重复

---

### 第 4 步：当日记录（追加写入）

将本次 v3.2 执行作为系统管理记录**追加**到日志文件：

```powershell
Add-Content -Path $archiveFile -Value @"

## 📋 系统管理操作（v3.2）

### 归档执行
- **时间**：$((Get-Date).ToString('yyyy-MM-dd HH:mm'))
- **模式**：$mode (dry-run / enforce / soft)
- **目标智能体**：$agentId
- **workspace**：$WorkspaceDir
- **归档会话数**：$archivedCount
- **释放空间**：$freedMB MB
- **受保护 key**：$protectedKeys
- **OpenClaw 6.1 兼容**：FixMissing=$FixMissing, FixDmScope=$FixDmScope, ActiveKey=$($ActiveKey -join ',')
- **操作**：v3.2 安全归档完成
"@
```

**关键点**：
- ✅ 使用 `Add-Content` 追加写入
- ❌ 禁止使用 `write/Set-Content` 覆盖

---

### 第 5 步：物理文件清理（v3.0 关键改进，v3.1+/v3.2 保留）

**⚠️ v3.0 核心改进**（v3.2 完整保留）：按 `sessionId.*` 成组删除，覆盖所有变体文件：

```powershell
# v3.2: SessionsDir 已经从 path 配置阶段计算好
$sessionsDir = $SessionsDir
$sessionId = '<具体 sessionId>'

# 找出该 sessionId 的所有变体文件
# 覆盖：.jsonl, .trajectory.jsonl, .trajectory-path.json,
#       .jsonl.checkpoint.<id>.jsonl, .jsonl.reset.<ts>, .jsonl.deleted.<ts>
$patterns = @(
    "$sessionId.jsonl",
    "$sessionId.trajectory.jsonl",
    "$sessionId.trajectory-path.json",
    "$sessionId.jsonl.checkpoint.*.jsonl",
    "$sessionId.jsonl.reset.*",
    "$sessionId.jsonl.deleted.*"
)

$totalFreed = 0
foreach ($pattern in $patterns) {
    $files = Get-ChildItem -Path $sessionsDir -Filter $pattern -Force -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $size = $file.Length
        if ($mode -eq 'soft') {
            # 软删除：重命名为 .deleted.<timestamp>
            $newName = "$($file.FullName).deleted.$((Get-Date).ToString('yyyy-MM-ddTHH-mm-ss.fffZ'))"
            Rename-Item -Path $file.FullName -NewName (Split-Path $newName -Leaf)
            Write-Host "[soft-rename] $($file.Name) -> $(Split-Path $newName -Leaf)" -ForegroundColor DarkYellow
        } else {
            # 硬删除
            Remove-Item $file.FullName -Force
            Write-Host "[hard-delete] $($file.Name) ($size bytes)" -ForegroundColor Green
        }
        $totalFreed += $size
    }
}

Write-Host "[总计] 释放 $($totalFreed / 1MB) MB" -ForegroundColor Cyan
```

**警告**：
- ❌ 不要只删 `<id>.jsonl`，会漏掉 `.trajectory.jsonl` 等
- ✅ 必须按 `sessionId.*` 通配符成组清理

---

### 第 6 步：清理 sessions.json 索引（v3.1+ 升级：双保险）

**⚠️ v3.1+ 核心升级**：在 v3.0 反向匹配基础上，**优先调 OpenClaw 6.1 官方 `--fix-missing`**，再用自写逻辑补盲区（双保险）：

```powershell
$sessionsFile = Join-Path $SessionsDir "sessions.json"

# === v3.1+ 第 6.1 步：优先调官方 --fix-missing（6.1+） ===
# 官方会识别所有"transcript 文件不存在"的孤儿，绕过 age/count retention 限制
if ($FixMissing -and -not $NoFixMissing) {
    if ($Mode -eq "enforce") {
        $fixArgs = @("sessions", "cleanup", "--agent", $Agent, "--enforce", "--fix-missing")
        if ($FixDmScope) { $fixArgs += "--fix-dm-scope" }
        foreach ($key in $ActiveKey) { $fixArgs += "--active-key"; $fixArgs += $key }
        Write-Action "执行官方 --fix-missing 清理..."
        & openclaw @fixArgs 2>&1 | Out-String | Write-Info
    } else {
        Write-Info "[dry-run] 6.1 --fix-missing 将被调用（实际未执行）"
    }
} else {
    Write-Warn "跳过官方 --fix-missing（FixMissing=$FixMissing, NoFixMissing=$NoFixMissing）"
}

# === v3.1+ 第 6.2 步：自写逻辑补盲区（仅当 6.1 漏掉时） ===
# 6.1 官方只清"transcript 不存在"的孤儿，漏掉"status 缺失但文件存在"等异常
$json = Get-Content $sessionsFile -Raw | ConvertFrom-Json

$staleKeys = @()
foreach ($prop in $json.PSObject.Properties.Copy) {
    $entry = $prop.Value
    $keyName = $prop.Name

    # 跳过受保护 key
    if ($keyName -in $protectedKeys) { continue }
    if ($keyName -match ':main$') { continue }
    if ($keyName -match ':cron:') { continue }
    if ($keyName -match ':dashboard:' -and $entry.status -ne 'done') { continue }

    # 检测"status 字段缺失但文件存在"的异常（v3.0 漏的类型）
    if (-not $entry.status -and $entry.sessionFile -and (Test-Path $entry.sessionFile)) {
        Write-Warn "异常条目：$keyName 缺 status 字段（v3.0 盲区，v3.1+/v3.2 检测但不自动清）"
        # 不加入 $staleKeys，留给操作员决定
    }

    # 检测孤儿条目（v3.0 已有逻辑，官方 --fix-missing 已经在第 1 步清过）
    if ($entry.sessionFile -and -not (Test-Path $entry.sessionFile)) {
        $staleKeys += $keyName
        Write-Action "发现 orphan key: $keyName"
    }
}

# === v3.1+ 第 6.3 步：零匹配守卫（v3.0 修复的 bug，不能重蹈覆辙） ===
if ($Mode -eq "enforce") {
    if ($staleKeys.Count -gt 0) {
        # 强制备份
        $backupPath = "$sessionsFile.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $sessionsFile $backupPath
        Write-Success "已备份: $backupPath"

        # 删除 stale keys
        foreach ($key in $staleKeys) {
            $json.PSObject.Properties.Remove($key)
        }

        # 重写
        $json | ConvertTo-Json -Depth 20 | Set-Content $sessionsFile -NoNewline -Encoding UTF8
        Write-Success "已清理 $($staleKeys.Count) 个 stale key"
    } else {
        Write-Info "无需重写 sessions.json（无 stale key）"
    }
} else {
    Write-Warn "[dry-run] 将清理 $($staleKeys.Count) 个 stale key（未执行）"
    foreach ($k in $staleKeys) {
        Write-Action "  - $k"
    }
}
```

**v3.2 vs v3.0 第 6 步关键差异**：
- ❌ **v3.0 只调自写逻辑**（看 status 字段，漏无 status 孤儿）
- ✅ **v3.1+ 优先调官方 `--fix-missing`**（6.1 一步补上"transcript 不存在"孤儿）
- ✅ **v3.1+ 自写补 status 缺失异常**（6.1 漏的盲区）
- ✅ **v3.1+ 强制零匹配守卫**（err-20260606-001 不能重蹈）

**v3.1+ 第 6 步设计原则**：
- 集成优先：6.1 提供的能力优先用官方
- 互补保留：6.1 不提供的（如软删除、归档、status 检测）继续用自写
- 零匹配守卫：永远不无条件 Set-Content（防止 sessions.json 被清空）

**验证清理结果**：
```powershell
openclaw sessions --agent $agentId
# 应该显示: Sessions listed: N（:main + 活跃 cron + 活跃 dashboard 仍保留）
```

---

## ⚠️ 重要约束（v3.2 完整保留）

1. **禁止删除主会话**：`:main` 绝对不能动
2. **禁止删除活跃 cron 任务**：`:cron:*` 中正在运行的受保护
3. **禁止删除活跃 dashboard**：`:dashboard:*` 中 status≠done 的受保护
4. **sessions.json 清理用反向匹配**：永远不要用 `:main$` 这种粗暴过滤
5. **物理清理按 sessionId.* 成组**：覆盖 .jsonl + .trajectory.jsonl + .trajectory-path.json + .jsonl.checkpoint.* + .jsonl.reset.* + .jsonl.deleted.*
6. **先保存后删除**：第 1-4 步完成后才能执行第 5 步
7. **追加写入铁律**：第 3/4 步必须 `Add-Content`
8. **dashboard 父会话额外归档**：归档到 `<workspace>/memory/dashboard-archives/` 独立目录
9. **默认 dry-run**：必须显式传 `-Enforce` 才真删
10. **支持 soft 模式**：用 `.deleted.<timestamp>` 后缀代替 `Remove-Item`
11. **6.1 兼容**：6.1+ 默认调 `--fix-missing` / `--active-key` / `--fix-dm-scope`；低版本自动降级（用 `-NoFixMissing`）
12. **零匹配守卫**：第 6 步零匹配时**不重写** sessions.json（参考 ERR-20260606-001）
13. **v3.2 新增：跨平台路径**：自动检测 `~/.openclaw`（Win/macOS/Linux）
14. **v3.2 新增：workspace 可配置**：默认自动检测唯一 workspace；多 workspace 报错引导用 `-WorkspaceDir`
15. **v3.2 新增：示例中性化**：示例统一用 `-Agent myagent`，避免绑定特定私有 agent

## 适用场景

- 子任务完成后清理临时会话
- 下属智能体子会话闲置需要归档
- 系统维护时清理 dashboard 已结束的父会话
- 磁盘空间不足时批量清理
- 配合 OpenClaw 原生 `sessions cleanup` 做补强
- **v3.1+ 新增**：OpenClaw 6.1 升级后做能力集成（替代纯 v3.0 自写逻辑）
- **v3.2 新增**：跨平台工作流统一（Win 开发机 + macOS 工作站 + Linux 服务器）

## 禁止行为

- ❌ 直接删除文件（跳过归档流程）
- ❌ 删除主会话文件或 sessions.json 中的 `:main` 条目
- ❌ 只删 `.jsonl` 不删 `.trajectory.jsonl`（数据残留）
- ❌ 用 `$key -notmatch ':main$'` 过滤 sessions.json（粗暴，可能误杀）
- ❌ 第 3/4 步使用覆盖写入（覆盖原有记录）
- ❌ 在 `--dry-run` 模式下执行物理删除
- ❌ 把 dashboard status=running 的父会话也归档
- ❌ 用本技能清掉 `:cron:*` 活跃任务
- ❌ **v3.1+ 新增**：第 6 步零匹配时仍 Set-Content（参考 ERR-20260606-001）
- ❌ **v3.1+ 新增**：跳过第 1 步的官方 `--fix-missing` 调用（除非用 `-NoFixMissing` 显式降级）
- ❌ **v3.2 新增**：在主会话（agent:YOURAGENT:main）里跑 enforce 模式
- ❌ **v3.2 新增**：用 Unix 风格参数 `--agent=foo`（必须用 PowerShell 原生 `-Agent foo`）

## 完整检查清单（v3.2）

- [ ] **第 0 步（v3.2 新增）**：路径检测（OpenClaw 根 + workspace + memory + dashboard-archives）
- [ ] **第 0 步（v3.2 新增）**：多 workspace 时用 `-WorkspaceDir` 显式指定
- [ ] **第 1 步**：识别会话类型（direct/cron/dashboard）和 status
- [ ] **第 1 步**：受保护 key 列表已建立（:main / :cron:* / 活跃 :dashboard:*）
- [ ] **第 1 步（v3.1+ 新增）**：默认调官方 `--fix-missing`（6.1+ 自动）
- [ ] **第 1 步（v3.1+ 新增）**：`--active-key` 透传（如指定）
- [ ] **第 2 步**：安全分析（敏感信息/重要成果/错误教训）
- [ ] **第 3 步**：结构化归档（**追加写入 `Add-Content`** 到 `<workspace>/memory/YYYY-MM-DD-subagent-archive-v3.md`）
- [ ] **第 3 步（dashboard）**：额外追加到 `<workspace>/memory/dashboard-archives/YYYY-MM-DD-dashboard-<sessionId>.md`
- [ ] **第 4 步**：当日记录（**追加写入 `Add-Content`**）
- [ ] **第 5 步**：物理文件清理（按 `sessionId.*` 成组，覆盖 6 种变体）
- [ ] **第 5 步**：使用 `dry-run` / `soft` / `enforce` 中合适的模式
- [ ] **第 6 步**：清理 sessions.json（**双保险**：官方 `--fix-missing` + 自写反向匹配）
- [ ] **第 6 步**：保留 :main / :cron:* / 活跃 :dashboard:*
- [ ] **第 6 步（v3.1+ 新增）**：零匹配守卫——零匹配时**不重写** sessions.json
- [ ] **验证**：`openclaw sessions --agent $agentId` 显示正确的会话数

## 关联工具

- **执行脚本**：`scripts/archive-sessions.ps1`（v3.2 实现，跨平台 + workspace 可配置）
- **OpenClaw 原生**：`openclaw sessions cleanup --enforce --fix-missing`（v3.1+ 集成）
- **OpenClaw 6.1 新参数**：`--fix-missing` / `--active-key` / `--fix-dm-scope`
- **OpenClaw 维护**：`openclaw config get session.maintenance`（v3.1+ 配合 enforce 模式）

## 版本历史

- **v3.2.0** (2026-06-06) — 通用化重构：跨平台路径检测（Win/macOS/Linux + PS 5.1/7+）、`-WorkspaceDir` 参数（自动检测 + 显式覆盖）、中性化作者署名；完整保留 v3.1 全部功能
- **v3.1.0** (2026-06-06) — OpenClaw 6.1 适配：集成 `--fix-missing` / `--active-key` / `--fix-dm-scope`；第 6 步改为"官方 + 自写"双保险；新增 `-NoFixMissing` 降级开关
- **v3.0.0** (2026-06-06) — 物理文件成组清理 + 反向匹配索引清理 + dashboard 父会话分流 + 软删除模式
- **v1.1.0** (2026-04-26) — 基础 6 步流程 + 追加写入铁律
- **v1.0.0** (2026-04-?) — 初版（v1.1.0 之前的实现）
