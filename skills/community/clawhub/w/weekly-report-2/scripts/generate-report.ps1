# generate-report.ps1 - Weekly report generator (Git-based)
# Usage:
#   powershell -ExecutionPolicy Bypass -File generate-report.ps1 -Repo . -Days 7 -Output weekly-report.md
param(
    [string]$Repo = ".",
    [int]$Days = 7,
    [string]$Author = "",
    [string]$Output = "weekly-report.md"
)

$ErrorActionPreference = "Stop"

# --- Resolve repo path ---
$repoPath = (Resolve-Path -LiteralPath $Repo).Path
Push-Location $repoPath
try {
    git rev-parse --is-inside-work-tree 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Not a Git repository: $repoPath"
    }

    $sinceDate = (Get-Date).AddDays(-$Days)
    $since = $sinceDate.ToString("yyyy-MM-dd 00:00:00")
    $until = (Get-Date).ToString("yyyy-MM-dd 23:59:59")

    # --- Collect commits ---
    $authorFilter = if ($Author) { " --author=`"$Author`"" } else { "" }
    $raw = git log "--since=$since" "--until=$until" --pretty=format:"%h||%ad||%an||%s" --date=short $authorFilter
    $commits = @($raw) | Where-Object { $_ -match "^\w+\|\|" }

    if ($commits.Count -eq 0) {
        Write-Host "No commits found in the last $Days day(s)."
        Pop-Location
        exit 0
    }

    # --- Collect changed files (exclude merges) ---
    $files = git log "--since=$since" "--until=$until" --no-merges --name-only --pretty=format:"" $authorFilter |
        Where-Object { $_.Trim() -ne "" } | Sort-Object -Unique

    # --- Aggregate stats ---
    $authors = $commits | ForEach-Object {
        ($_ -split "\|\|")[2]
    } | Sort-Object -Unique

    # --- Build commit table rows ---
    $rows = foreach ($c in $commits) {
        $parts = $c -split "\|\|"
        $hash = $parts[0].Substring(0, [Math]::Min(7, $parts[0].Length))
        $date = $parts[1]
        $who  = $parts[2]
        $msg  = $parts[3]
        "| $hash | $date | $who | $msg |"
    }

    $rangeStart = $sinceDate.ToString("yyyy-MM-dd")
    $rangeEnd   = (Get-Date).ToString("yyyy-MM-dd")
    $commitCount = $commits.Count
    $fileCount   = @($files).Count
    $authorCount = @($authors).Count

    # --- Write report ---
    $report = @"
# Weekly Report

**Report period**: $rangeStart ~ $rangeEnd
**Commits**: $commitCount | **Files changed**: $fileCount | **Contributors**: $authorCount

## Accomplished
- (Draft this section from commit summaries)

## In Progress
- (To be filled)

## Issues & Risks
- None

## Next Week Plan
- (To be filled)

## Commit Details
| Hash | Date | Author | Message |
|------|------|--------|---------|
$($rows -join "`n")
"@

    Set-Content -LiteralPath $Output -Value $report -Encoding UTF8
    Write-Host "Report written to $Output ($commitCount commits, $fileCount files)."
}
finally {
    Pop-Location
}
