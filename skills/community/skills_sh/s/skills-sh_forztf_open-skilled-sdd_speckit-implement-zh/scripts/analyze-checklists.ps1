# 检查清单状态分析脚本
param(
    [Parameter(Mandatory=$true)]
    [string]$ChecklistsDir
)

function Get-ChecklistStatus {
    param(
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        return @{
            Name = Split-Path $Path -Leaf
            Total = 0
            Completed = 0
            Incomplete = 0
            Status = "NOT_FOUND"
        }
    }

    $content = Get-Content $Path -Raw
    $lines = $content -split "`n"

    $total = 0
    $completed = 0
    $incomplete = 0

    foreach ($line in $lines) {
        if ($line -match '^- \[([ Xx])\]') {
            $total++
            if ($matches[1] -eq 'X' -or $matches[1] -eq 'x') {
                $completed++
            } else {
                $incomplete++
            }
        }
    }

    $status = if ($incomplete -eq 0) { "PASS" } else { "FAIL" }

    return @{
        Name = Split-Path $Path -Leaf
        Total = $total
        Completed = $completed
        Incomplete = $incomplete
        Status = $status
    }
}

# 主逻辑
if (-not (Test-Path $ChecklistsDir)) {
    Write-Host "No checklists directory found."
    exit 0
}

$checklists = Get-ChildItem $ChecklistsDir -Filter "*.md"
$results = @()

foreach ($checklist in $checklists) {
    $status = Get-ChecklistStatus -Path $checklist.FullName
    $results += $status
}

# 生成状态表
Write-Host "| Checklist | Total | Completed | Incomplete | Status |"
Write-Host "|-----------|-------|-----------|------------|--------|"

foreach ($result in $results) {
    $statusSymbol = if ($result.Status -eq "PASS") { "✓ PASS" } else { "✗ FAIL" }
    Write-Host "| $($result.Name) | $($result.Total) | $($result.Completed) | $($result.Incomplete) | $statusSymbol |"
}

# 计算总体状态
$overallStatus = if ($results.Where({$_.Status -eq "FAIL"}).Count -eq 0) { "PASS" } else { "FAIL" }

Write-Host "`nOverall Status: $overallStatus"

if ($overallStatus -eq "FAIL") {
    Write-Host "`nSome checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
}

# 输出 JSON 格式（如果需要）
$results | ConvertTo-Json -Depth 10