$ErrorActionPreference = 'Stop'
$base = Join-Path ([IO.Path]::GetTempPath()) ('windows-disk-care-test-' + [Guid]::NewGuid().ToString('N'))
$root = Join-Path $base 'fixture'
New-Item -ItemType Directory -Path $root -Force | Out-Null
& git -C $root init -q
if ($LASTEXITCODE) { throw 'Fixture git init failed' }
Set-Content -LiteralPath (Join-Path $root '.gitignore') -Value '.local/'
Set-Content -LiteralPath (Join-Path $root 'source-sentinel.txt') -Value 'Preserve source'
$packages = Join-Path $root '.local\desktop-package'
$ages = [ordered]@{newest=1;second=2;old=3;pinned=11;linked=12;tracked=13;locked=14;unknown=15}
foreach ($name in $ages.Keys) {
    $p = Join-Path $packages "build-$name"
    $app = Join-Path $p 'ExampleApp-win32-x64'
    New-Item -ItemType Directory -Path (Join-Path $app 'resources') -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $app 'ExampleApp.exe') -Value 'Synthetic test file; not executable'
    if ($name -ne 'unknown') { Set-Content -LiteralPath (Join-Path $app 'resources\app.asar') -Value 'Synthetic test archive' }
    if ($name -eq 'pinned') { Set-Content -LiteralPath (Join-Path $p '.keep') -Value 'retain' }
    if ($name -eq 'old') { Set-Content -LiteralPath (Join-Path $p 'acceptance-evidence.txt') -Value 'Preserve outer acceptance evidence' }
    foreach ($entry in Get-ChildItem -LiteralPath $p -Recurse -Force) { $entry.LastWriteTimeUtc = [DateTime]::UtcNow.AddDays(-$ages[$name]) }
    (Get-Item -LiteralPath $p).LastWriteTimeUtc = [DateTime]::UtcNow.AddDays(-$ages[$name])
}
& git -C $root add -f -- '.local/desktop-package/build-tracked/ExampleApp-win32-x64/ExampleApp.exe'
if ($LASTEXITCODE) { throw 'Fixture track failed' }
$outside = Join-Path $root 'outside-sentinel'
New-Item -ItemType Directory -Path $outside | Out-Null
Set-Content -LiteralPath (Join-Path $outside 'preserve.txt') -Value 'Do not follow junctions'
New-Item -ItemType Junction -Path (Join-Path $packages 'build-linked\escape') -Target $outside | Out-Null
(Get-Item -LiteralPath (Join-Path $packages 'build-linked')).LastWriteTimeUtc = [DateTime]::UtcNow.AddDays(-12)
$policy = [ordered]@{
    Repository=$root;ReportDirectory=$base;KeepValidPackages=2;MinimumAgeDays=0
    ApplicationNames=@('ExampleApp');RustMinimumIdleHours=24;ShortcutRoots=@();ProtectedPaths=@();RustCaches=@();RustTargetDefinitions=@()
}
$policyFile = Join-Path $root 'test-policy.json'
$policy | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $policyFile -Encoding utf8
$lockFile = Join-Path $packages 'build-locked\ExampleApp-win32-x64\resources\app.asar'
$handle = [IO.File]::Open($lockFile,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::None)
try {
    & (Join-Path $PSScriptRoot 'Invoke-DiskCare.ps1') -PolicyPath $policyFile | Out-Null
    $previewFile = Get-ChildItem -LiteralPath $base -Filter '*-preview.json' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    & (Join-Path $PSScriptRoot 'Invoke-DiskCare.ps1') -PolicyPath $policyFile -Apply -ReviewedPreview $previewFile.FullName | Out-Null
} finally { $handle.Dispose() }
$reportFile = Get-ChildItem -LiteralPath $base -Filter '*-cleanup.json' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$report = Get-Content -LiteralPath $reportFile.FullName -Raw | ConvertFrom-Json
if (@($report.Results | Where-Object Status -eq 'deleted').Count -ne 1) { throw 'Expected exactly one disposable package to be deleted' }
if (Test-Path -LiteralPath (Join-Path $packages 'build-old\ExampleApp-win32-x64')) { throw 'Disposable old application payload was not removed' }
if (-not (Test-Path -LiteralPath (Join-Path $packages 'build-old\acceptance-evidence.txt'))) { throw 'Outer acceptance evidence was lost' }
foreach ($name in @('newest','second')) {
    $entry = $report.Results | Where-Object Path -eq (Join-Path $packages "build-$name")
    if ($entry.Reason -ne 'latest-valid-package') { throw "Latest two retention was not exercised: $name" }
}
$linked = $report.Results | Where-Object Path -eq (Join-Path $packages 'build-linked')
if ($linked.Reason -notmatch 'Linked descendant') { throw 'Junction boundary was not exercised' }
foreach ($name in @('newest','second','pinned','linked','tracked','locked','unknown')) {
    if (-not (Test-Path -LiteralPath (Join-Path $packages "build-$name"))) { throw "Protected test item lost: $name" }
}
foreach ($p in @((Join-Path $outside 'preserve.txt'),(Join-Path $root 'source-sentinel.txt'),(Join-Path $root '.git'))) {
    if (-not (Test-Path -LiteralPath $p)) { throw "Sentinel lost: $p" }
}
[pscustomobject]@{Passed=$true;Checks=11;Fixture=$root;Report=$reportFile.FullName;Description='Deletes reviewed old application payload; preserves outer evidence, latest two, pins, junction target, tracked file, open file, unknown package, source, and Git.'} | ConvertTo-Json -Compress

