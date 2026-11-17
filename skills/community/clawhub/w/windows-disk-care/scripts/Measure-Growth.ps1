#requires -Version 7.2
[CmdletBinding()]
param(
    [string]$ReportDirectory = (Join-Path $env:LOCALAPPDATA 'WindowsDiskCare\reports'),
    [Alias('Path')][string[]]$WatchPath = @(),
    [string]$Repository,
    [string]$PolicyPath,
    [string]$CodexDirectory = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' })
)
$ErrorActionPreference = 'Stop'
if (-not ('DiskCareMeasure' -as [type])) { Add-Type -Path (Join-Path $PSScriptRoot 'DiskCareMeasure.cs') }
$policy = if ($PolicyPath) { Get-Content -LiteralPath $PolicyPath -Raw -Encoding utf8 | ConvertFrom-Json }
if ($policy) {
    if (-not $Repository) { $Repository = $policy.Repository }
    if (-not $PSBoundParameters.ContainsKey('ReportDirectory') -and $policy.ReportDirectory) { $ReportDirectory = $policy.ReportDirectory }
}
$historyPath = Join-Path $ReportDirectory 'growth-history.json'
$guard = [Threading.Mutex]::new($false, 'Local\CodexDiskGrowthMonitor')
try { $acquired = $guard.WaitOne(0) } catch [Threading.AbandonedMutexException] { $acquired = $true }
if (-not $acquired) { $guard.Dispose(); throw 'Another growth measurement is running' }

try {
    $started = [DateTimeOffset]::Now
    $history = if ([IO.File]::Exists($historyPath)) {
        Get-Content -LiteralPath $historyPath -Raw | ConvertFrom-Json -AsHashtable
    } else { @{SchemaVersion=1; Samples=@()} }
    if ($history.SchemaVersion -ne 1 -or -not $history.Contains('Samples')) { throw 'Unrecognized growth history' }
    $last = if ($history.Samples.Count) { $history.Samples[-1] } else { $null }
    $paths = [ordered]@{}
    $issues = [Collections.Generic.List[string]]::new()
    function Add-Path([string]$folder, [string]$kind) {
        $paths[[IO.Path]::GetFullPath($folder)] = $kind
    }
    function Direct-Children([string]$folder) {
        try {
            $item = Get-Item -Force -LiteralPath $folder
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked root' }
            Get-ChildItem -LiteralPath $folder -Directory -Force |
                Where-Object { -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) }
        } catch { $issues.Add("$folder / $($_.Exception.GetType().Name)") }
    }

    $userCodex = $CodexDirectory
    $codexItem = Get-Item -LiteralPath $userCodex -Force -ErrorAction SilentlyContinue
    if ($codexItem -and -not ($codexItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        foreach ($folder in @('sessions','archived_sessions')) { Add-Path (Join-Path $userCodex $folder) 'SessionFiles' }
        foreach ($dbRoot in @($userCodex,(Join-Path $userCodex 'sqlite'))) {
            $dbItem = Get-Item -LiteralPath $dbRoot -Force -ErrorAction SilentlyContinue
            if ($dbItem -and -not ($dbItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                try {
                    foreach ($db in Get-ChildItem -LiteralPath $dbRoot -Filter '*.sqlite*' -File -Force -ErrorAction Stop) { Add-Path $db.FullName 'DatabaseFile' }
                } catch { $issues.Add("$dbRoot / $($_.Exception.GetType().Name)") }
            }
        }
        $worktreeDir = Join-Path $userCodex 'worktrees'
        if ([IO.Directory]::Exists($worktreeDir)) { foreach ($folder in Direct-Children $worktreeDir) { Add-Path $folder.FullName 'Worktree' } }
    }
    try { foreach ($page in Get-CimInstance Win32_PageFileUsage -ErrorAction Stop) { Add-Path $page.Name 'PagingFile' } }
    catch { $issues.Add('Paging file discovery unavailable') }
    foreach ($rel in @('Docker\wsl\disk\docker_data.vhdx','Docker\wsl\data\ext4.vhdx')) {
        $vhd = Join-Path $env:LOCALAPPDATA $rel
        if ([IO.File]::Exists($vhd)) { Add-Path $vhd 'DockerDiskFile' }
    }
    if ($Repository) {
        try {
            $registered = @(& git -c core.quotepath=false -C $Repository worktree list --porcelain 2>$null)
            if ($LASTEXITCODE -ne 0) { throw 'Git worktree listing failed' }
            foreach ($line in $registered) {
                if (-not $line.StartsWith('worktree ')) { continue }
                $root = [IO.Path]::GetFullPath($line.Substring(9))
                foreach ($child in @('.local\desktop-package','target','node_modules')) {
                    $candidate = Join-Path $root $child
                    if ([IO.Directory]::Exists($candidate)) { Add-Path $candidate 'ProjectOutput' }
                }
            }
        } catch { $issues.Add('Git worktree discovery unavailable') }
    }
    if ($policy) { foreach ($definition in $policy.RustTargetDefinitions) { Add-Path $definition.TargetRoot 'CargoTarget' } }
    foreach ($path in $WatchPath) {
        if (-not [IO.Path]::IsPathFullyQualified($path)) { throw 'WatchPath requires absolute paths.' }
        Add-Path $path 'UserWatch'
    }
    if ($last) {
        foreach ($past in $last.Rows) {
            if ($past.Status -ne 'missing' -and -not $paths.Contains($past.Path)) { Add-Path $past.Path $past.Kind }
        }
    }
    $previousRows = @{}
    if ($last) { foreach ($row in $last.Rows) { $previousRows[$row.Path] = $row } }
    $rows = @(foreach ($path in $paths.Keys | Sort-Object) {
        $size = $null; $errors = 0; $links = 0; $status = 'ok'
        try {
            $ancestor = [IO.Directory]::GetParent($path)
            while ($null -ne $ancestor) {
                if ($ancestor.Exists -and ($ancestor.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                    throw [IO.IOException]::new('Linked ancestor')
                }
                $ancestor = $ancestor.Parent
            }
            $metadata = Get-Item -LiteralPath $path -Force -ErrorAction Stop
            if ($metadata.Attributes -band [IO.FileAttributes]::ReparsePoint) { $status = 'reparse' }
            elseif ($metadata.PSIsContainer) {
                $scanner = [DiskCareMeasure]::new()
                $scanner.Minimum = [long]::MaxValue
                $size = $scanner.Scan($path).Bytes
                $errors = $scanner.ErrorCount
                $links = $scanner.LinkCount
                if ($errors) { $status = 'partial' }
            } else { $size = [long]$metadata.Length }
        } catch [System.Management.Automation.ItemNotFoundException] { $size = 0L; $status = 'missing' }
          catch { $status = 'unavailable'; $errors++ }
        $prev = $previousRows[$path]
        $delta = $null
        if ($prev -and $prev.Status -in @('ok','missing') -and $status -in @('ok','missing')) { $delta = $size - $prev.LogicalBytes }
        $firstSeen = [bool]($last -and -not $prev -and $status -eq 'ok')
        [ordered]@{Path=$path;Kind=$paths[$path];Status=$status;LogicalBytes=$size;DeltaLogicalBytes=$delta;FirstSeen=$firstSeen;Errors=$errors;SkippedLinks=$links}
    })
    $drives = @(foreach ($disk in [IO.DriveInfo]::GetDrives()) {
        if ($disk.DriveType -ne 'Fixed' -or -not $disk.IsReady) { continue }
        $letter = $disk.Name.Substring(0,1)
        $prior = if ($last) { $last.Drives | Where-Object Drive -eq $letter }
        $free = $disk.AvailableFreeSpace
        [ordered]@{Drive=$letter;FreeBytes=$free;TotalBytes=$disk.TotalSize;FreeDelta=if ($prior) { $free - $prior.FreeBytes } else { $null }}
    })
    $sample = [ordered]@{StartedAt=$started.ToString('o');FinishedAt=[DateTimeOffset]::Now.ToString('o');Drives=$drives;Rows=$rows;DiscoveryIssues=@($issues)}
    $samples = @($history.Samples | Select-Object -Last 31) + @($sample)
    [void][IO.Directory]::CreateDirectory($ReportDirectory)
    $tmp = Join-Path $ReportDirectory ('growth-history-'+[Guid]::NewGuid().ToString('N')+'.tmp')
    try {
        $doc = [ordered]@{SchemaVersion=1;Samples=$samples}
        [IO.File]::WriteAllText($tmp,($doc | ConvertTo-Json -Depth 8 -Compress),[Text.UTF8Encoding]::new($false))
        [IO.File]::Move($tmp,$historyPath,$true)
    } finally { if ([IO.File]::Exists($tmp)) { [IO.File]::Delete($tmp) } }
    $changes = @($rows | Where-Object { $_.FirstSeen -or ($null -ne $_.DeltaLogicalBytes -and [Math]::Abs($_.DeltaLogicalBytes) -ge 64MB) } |
        Sort-Object { if ($_.FirstSeen) { $_.LogicalBytes } else { [Math]::Abs($_.DeltaLogicalBytes) } } -Descending | Select-Object -First 12)
    [ordered]@{Report=$historyPath;Samples=$samples.Count;Measured=$rows.Count;PreviousAt=if ($last){$last.FinishedAt};Drives=$drives;Changes=$changes;DiscoveryIssues=@($issues);Incomplete=@($rows|Where-Object { $_.Status -notin @('ok','missing') }).Count} | ConvertTo-Json -Depth 6 -Compress
} finally { $guard.ReleaseMutex(); $guard.Dispose() }
