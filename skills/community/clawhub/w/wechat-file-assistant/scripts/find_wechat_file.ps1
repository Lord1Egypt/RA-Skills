[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Query,
    [string[]]$Root,
    [switch]$Exact,
    [Nullable[datetime]]$Since,
    [Nullable[datetime]]$Before,
    [ValidateRange(1, 500)]
    [int]$MaxResults = 20,
    [string]$MetadataIndex,
    [switch]$OpenInExplorer,
    [switch]$DiscoverOnly
)

$ErrorActionPreference = 'Stop'

function Get-CanonicalPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    try {
        return [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
    } catch {
        return $Path.TrimEnd('\')
    }
}

function Add-CandidateRoot {
    param(
        [System.Collections.Generic.List[string]]$List,
        [string]$Path
    )
    if ([string]::IsNullOrWhiteSpace($Path)) { return }
    if (Test-Path -LiteralPath $Path -PathType Container) {
        $canonical = Get-CanonicalPath -Path $Path
        if (-not ($List | Where-Object { $_.Equals($canonical, [System.StringComparison]::OrdinalIgnoreCase) })) {
            $List.Add($canonical)
        }
    }
}

function Get-WeChatRoots {
    param([string[]]$ExplicitRoots)
    $roots = [System.Collections.Generic.List[string]]::new()
    foreach ($item in $ExplicitRoots) { Add-CandidateRoot -List $roots -Path $item }
    if ($ExplicitRoots.Count -gt 0) { return @($roots) }
    if ($env:WECHAT_FILE_ROOTS) {
        foreach ($item in ($env:WECHAT_FILE_ROOTS -split ';')) {
            Add-CandidateRoot -List $roots -Path $item
        }
    }
    $documents = [Environment]::GetFolderPath('MyDocuments')
    Add-CandidateRoot -List $roots -Path (Join-Path $documents 'WeChat Files')
    Add-CandidateRoot -List $roots -Path (Join-Path $documents 'xwechat_files')
    foreach ($drive in [System.IO.DriveInfo]::GetDrives()) {
        if (-not $drive.IsReady) { continue }
        $base = $drive.RootDirectory.FullName
        Add-CandidateRoot -List $roots -Path (Join-Path $base 'xwechat_files')
        Add-CandidateRoot -List $roots -Path (Join-Path $base 'WeChat Files')
        Add-CandidateRoot -List $roots -Path (Join-Path $base 'wechat\WeChat Files')
        Add-CandidateRoot -List $roots -Path (Join-Path $base 'weixin\WeChat Files')
    }
    return @($roots)
}

function Read-MetadataIndex {
    param([string]$IndexPath)
    $map = @{}
    if ([string]::IsNullOrWhiteSpace($IndexPath)) { return $map }
    if (-not (Test-Path -LiteralPath $IndexPath -PathType Leaf)) {
        throw "Metadata index not found: $IndexPath"
    }
    $extension = [System.IO.Path]::GetExtension($IndexPath).ToLowerInvariant()
    $records = @()
    if ($extension -eq '.csv') {
        $records = @(Import-Csv -LiteralPath $IndexPath)
    } elseif ($extension -eq '.jsonl' -or $extension -eq '.ndjson') {
        $records = @(Get-Content -LiteralPath $IndexPath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object { $_ | ConvertFrom-Json })
    } elseif ($extension -eq '.json') {
        $records = @((Get-Content -Raw -LiteralPath $IndexPath | ConvertFrom-Json))
    } else {
        throw 'MetadataIndex must be CSV, JSON, JSONL, or NDJSON.'
    }
    foreach ($record in $records) {
        if ($null -eq $record.path -or [string]::IsNullOrWhiteSpace([string]$record.path)) { continue }
        $key = (Get-CanonicalPath -Path ([string]$record.path)).ToLowerInvariant()
        $map[$key] = $record
    }
    return $map
}

function Get-AccountHint {
    param([string]$FilePath, [string]$SearchRoot)
    $relative = $FilePath.Substring($SearchRoot.Length).TrimStart('\')
    if ([string]::IsNullOrWhiteSpace($relative)) { return $null }
    $first = $relative.Split('\')[0]
    if ($first -match '^(wxid_|Q\d|[A-Za-z0-9_-]+_[A-Fa-f0-9]{4,})') { return $first }
    return $null
}

$attempted = [System.Collections.Generic.List[string]]::new()
$documents = [Environment]::GetFolderPath('MyDocuments')
$attempted.Add((Join-Path $documents 'WeChat Files'))
$attempted.Add((Join-Path $documents 'xwechat_files'))
foreach ($drive in [System.IO.DriveInfo]::GetDrives()) {
    if (-not $drive.IsReady) { continue }
    $base = $drive.RootDirectory.FullName
    $attempted.Add((Join-Path $base 'xwechat_files'))
    $attempted.Add((Join-Path $base 'wechat\WeChat Files'))
}

$roots = @(Get-WeChatRoots -ExplicitRoots $Root)
if ($DiscoverOnly) {
    [pscustomobject]@{
        status = if ($roots.Count -gt 0) { 'ok' } else { 'no_roots' }
        roots = $roots
        attempted = @($attempted | Select-Object -Unique)
    } | ConvertTo-Json -Depth 5
    exit 0
}
if ([string]::IsNullOrWhiteSpace($Query)) {
    throw 'Query is required unless -DiscoverOnly is used.'
}
if ($roots.Count -eq 0) {
    [pscustomobject]@{
        status = 'no_roots'
        query = $Query
        roots = @()
        attempted = @($attempted | Select-Object -Unique)
        results = @()
    } | ConvertTo-Json -Depth 5
    exit 0
}

$metadata = Read-MetadataIndex -IndexPath $MetadataIndex
$matches = [System.Collections.Generic.List[object]]::new()
foreach ($searchRoot in $roots) {
    Get-ChildItem -LiteralPath $searchRoot -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object {
            $nameMatches = if ($Exact) {
                $_.Name.Equals($Query, [System.StringComparison]::OrdinalIgnoreCase)
            } else {
                $_.Name.IndexOf($Query, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
            }
            $dateMatches = $true
            if ($Since.HasValue -and $_.LastWriteTime -lt $Since.Value) { $dateMatches = $false }
            if ($Before.HasValue -and $_.LastWriteTime -ge $Before.Value) { $dateMatches = $false }
            $nameMatches -and $dateMatches
        } |
        ForEach-Object {
            $canonical = Get-CanonicalPath -Path $_.FullName
            $key = $canonical.ToLowerInvariant()
            $record = if ($metadata.ContainsKey($key)) { $metadata[$key] } else { $null }
            $status = if ($null -ne $record) { 'verified_index_match' } else { 'unavailable' }
            $matches.Add([pscustomobject]@{
                name = $_.Name
                path = $canonical
                size_bytes = $_.Length
                last_write_time = $_.LastWriteTime.ToString('o')
                last_write_time_source = 'filesystem'
                account_hint = Get-AccountHint -FilePath $canonical -SearchRoot $searchRoot
                sender = if ($null -ne $record) { $record.sender } else { $null }
                sent_at = if ($null -ne $record) { $record.sent_at } else { $null }
                chat = if ($null -ne $record) { $record.chat } else { $null }
                metadata_status = $status
                metadata_source = if ($null -ne $record -and $record.source) { $record.source } elseif ($null -ne $record) { Get-CanonicalPath -Path $MetadataIndex } else { $null }
            })
        }
}

$ordered = @($matches | Sort-Object @{ Expression = 'last_write_time'; Descending = $true }, path | Select-Object -First $MaxResults)
$explorerOpened = $false
$explorerSelectedPath = $null
if ($OpenInExplorer -and $ordered.Count -gt 0) {
    $explorerSelectedPath = [string]$ordered[0].path
    Start-Process -FilePath 'explorer.exe' -ArgumentList ('/select,"{0}"' -f $explorerSelectedPath)
    $explorerOpened = $true
}
[pscustomobject]@{
    status = 'ok'
    query = $Query
    exact = [bool]$Exact
    roots = $roots
    match_count_returned = $ordered.Count
    truncated = $matches.Count -gt $ordered.Count
    explorer_opened = $explorerOpened
    explorer_selected_path = $explorerSelectedPath
    results = $ordered
} | ConvertTo-Json -Depth 6
