# 技能进化（知行环）— 初始化 .wiki 目录结构（Windows PowerShell 原生版）
#
# 用法:
#   powershell -ExecutionPolicy Bypass -File wiki_init.ps1
#   powershell -ExecutionPolicy Bypass -File wiki_init.ps1 -Root "D:\proj"
#
# 说明: 本文件必须以 UTF-8 with BOM 保存，否则 Windows PowerShell 5.1
#       会按系统 ANSI（中文环境为 GBK）解析脚本，导致中文模板乱码。
#       有 Python 的环境建议优先使用 wiki_init.py。

param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$wiki = Join-Path $Root ".wiki"

if (Test-Path -LiteralPath $wiki) {
    Write-Host "[技能进化] .wiki 目录已存在: $wiki"
    exit 0
}

# 创建目录
foreach ($d in @("raw", "knowledge", "skills", "meta")) {
    New-Item -ItemType Directory -Path (Join-Path $wiki $d) -Force | Out-Null
}

# UTF8Encoding($false) = 无 BOM，与 wiki_init.sh / wiki_init.py 产出保持一致
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$patterns = @"
# Wiki Knowledge — 模式库

> 本文件由 Wiki Maintainer 维护，记录从执行轨迹中提炼的失败模式与成功策略。
> 只增不减，永不重置。

## 失败模式

（暂无记录）

## 成功策略

（暂无记录）
"@

$evolution = @"
# 技能演化日志

> 记录每次 Wiki 维护和技能变更的历史。

（暂无记录）
"@

$impact = @"
# 提案影响追踪

> 记录每个技能提案的验证结果。

（暂无记录）
"@

$today = Get-Date -Format "yyyy-MM-dd"
$config = @"
# Wiki 配置

- **创建日期**：$today
- **维护周期**：每 3-5 个任务后执行一次 Wiki Maintainer
- **进化周期**：每 5-10 个任务后执行一次 Skill Proposer
- **轨迹格式**：精简模式（每条 ≤10 行）
"@

$files = @{
    "knowledge\patterns.md"       = $patterns
    "knowledge\evolution_log.md"  = $evolution
    "knowledge\impact_tracker.md" = $impact
    "meta\config.md"              = $config
}

foreach ($key in $files.Keys) {
    $path = Join-Path $wiki $key
    [System.IO.File]::WriteAllText($path, $files[$key], $utf8NoBom)
}

Write-Host "[技能进化] 初始化完成: $wiki"
Write-Host "   raw/        - 执行轨迹（按日期追加）"
Write-Host "   knowledge/  - 持久化知识（patterns + evolution_log + impact_tracker）"
Write-Host "   skills/     - 可复用技能（可回滚）"
Write-Host "   meta/       - Wiki 配置"
exit 0
