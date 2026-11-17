param(
    [string[]]$Roots = @([IO.DriveInfo]::GetDrives() | Where-Object { $_.DriveType -eq 'Fixed' -and $_.IsReady } | ForEach-Object Name),
    [string]$OutputDirectory = (Join-Path $env:LOCALAPPDATA 'WindowsDiskCare\reports'),
    [int]$MinimumMiB = 256
)
$ErrorActionPreference = 'Stop'
if (-not ('DiskCareMeasure' -as [type])) {
    Add-Type -Path (Join-Path $PSScriptRoot 'DiskCareMeasure.cs')
}
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
foreach ($root in $Roots) {
    $scan = [DiskCareMeasure]::new()
    $scan.Minimum = [long]$MinimumMiB * 1MB
    $drive = [System.IO.DriveInfo]::new([System.IO.Path]::GetPathRoot([System.IO.Path]::GetFullPath($root)))
    $before = $drive.AvailableFreeSpace
    Write-Output "Scanning $root (metadata only; links skipped)"
    $total = $scan.Scan($root)
    $report = [ordered]@{
        SchemaVersion = 1
        Root = $root
        CapturedAt = (Get-Date).ToString('o')
        FreeBytes = $before
        TotalBytes = $drive.TotalSize
        LogicalBytes = $total.Bytes
        Files = $total.Files
        Note = 'Logical file sizes can double-count hard links and parent/child rows. Do not add nested rows or use these as freed disk space. Reparse points are skipped. Inaccessible paths are incomplete.'
        ErrorCount = $scan.ErrorCount
        Errors = @($scan.Errors)
        LinkCount = $scan.LinkCount
        Links = @($scan.Links)
        Directories = @($scan.Directories | Sort-Object Bytes -Descending)
        LargeFiles = @($scan.LargeFiles | Sort-Object Bytes -Descending)
    }
    $label = $root.TrimEnd('\').Replace(':','').Replace('\','_')
    $file = Join-Path $OutputDirectory "$stamp-$label.json"
    $report | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $file -Encoding utf8
    [pscustomobject]@{Report=$file;FreeGiB=[math]::Round($before/1GB,2);LogicalGiB=[math]::Round($total.Bytes/1GB,2);Files=$total.Files;Errors=$scan.ErrorCount;SkippedLinks=$scan.LinkCount} | ConvertTo-Json -Compress
    $scan.Directories | Sort-Object Bytes -Descending | Select-Object -First 55 Path,@{n='GiB';e={[math]::Round($_.Bytes/1GB,2)}} | ConvertTo-Json -Compress
}
