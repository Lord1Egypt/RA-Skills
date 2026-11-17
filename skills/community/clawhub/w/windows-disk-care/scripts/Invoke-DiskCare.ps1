#requires -Version 7.2
param(
    [switch]$Apply,
    [Parameter(Mandatory)][string]$PolicyPath,
    [string]$ReviewedPreview
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$policyBytes = [IO.File]::ReadAllBytes((Get-Item -LiteralPath $PolicyPath).FullName)
$policy = [Text.Encoding]::UTF8.GetString($policyBytes).TrimStart([char]0xFEFF) | ConvertFrom-Json
$policyHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($policyBytes))
$scriptHash = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash
if (-not $policy.Repository -or -not [IO.Path]::IsPathFullyQualified($policy.Repository) -or $policy.Repository -notmatch '^[A-Za-z]:\\') {
    throw 'Set Repository to the absolute local path of the approved Git checkout.'
}
foreach ($appName in $policy.ApplicationNames) {
    if ($appName -isnot [string] -or $appName -notmatch '^[\p{L}\p{N}](?:[\p{L}\p{N} ._-]{0,78}[\p{L}\p{N}_-])?$') { throw 'ApplicationNames must contain exact executable base names.' }
}
if ([int]$policy.KeepValidPackages -lt 1 -or [double]$policy.MinimumAgeDays -lt 0 -or [double]$policy.RustMinimumIdleHours -lt 0) {
    throw 'Keep at least one valid package and use non-negative retention periods.'
}
$reportDirectory = if ($policy.ReportDirectory) { [string]$policy.ReportDirectory } else { Join-Path $env:LOCALAPPDATA 'WindowsDiskCare\reports' }
if (-not [IO.Path]::IsPathFullyQualified($reportDirectory)) { throw 'ReportDirectory must be absolute.' }
$review = $null
if ($Apply) {
    if (-not $ReviewedPreview) { throw 'Apply requires a reviewed preview from this run.' }
    $review = Get-Content -LiteralPath $ReviewedPreview -Raw | ConvertFrom-Json
    if ($review.Applied -or $review.PolicyHash -ne $policyHash -or $review.ScriptHash -ne $scriptHash -or
        [DateTimeOffset]::Parse($review.FinishedAt).UtcDateTime -lt [DateTime]::UtcNow.AddMinutes(-30)) {
        throw 'Preview is stale or does not match the current policy/script.'
    }
}
if (-not ('DiskCareLeafInfo' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.ComponentModel;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
public class DiskCareLeafInfo {
    [StructLayout(LayoutKind.Sequential)] struct FT { public uint Low, High; }
    [StructLayout(LayoutKind.Sequential)] struct Info {
        public uint Attributes; public FT Creation, Access, Write;
        public uint Volume, High, Low, Links, IndexHigh, IndexLow;
    }
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool GetFileInformationByHandle(SafeFileHandle h, out Info info);
    public string Path {get;set;} public string Id {get;set;}
    public long Bytes {get;set;} public long WriteTicks {get;set;} public uint Links {get;set;}
    public static DiskCareLeafInfo Read(string path) {
        using (var f = File.Open(path, FileMode.Open, FileAccess.Read, FileShare.None)) {
            Info i; if (!GetFileInformationByHandle(f.SafeFileHandle, out i))
                throw new Win32Exception(Marshal.GetLastWin32Error());
            if ((i.Attributes & 0x400) != 0) throw new IOException("Reparse leaf");
            return new DiskCareLeafInfo {Path=System.IO.Path.GetFullPath(path),
                Id=i.Volume.ToString("X8")+":"+i.IndexHigh.ToString("X8")+i.IndexLow.ToString("X8"),
                Bytes=((long)i.High<<32)|i.Low, Links=i.Links,
                WriteTicks=DateTime.FromFileTimeUtc(((long)i.Write.High<<32)|i.Write.Low).Ticks};
        }
    }
}
'@
}
$mutex = [Threading.Mutex]::new($false, 'Local\CodexWindowsDiskCare')
if (-not $mutex.WaitOne(0)) { throw 'Another disk-care run is active.' }

function Full([string]$Path) { [IO.Path]::GetFullPath($Path).TrimEnd('\') }
function IsUnder([string]$Path, [string]$Root) {
    (Full $Path).StartsWith((Full $Root) + '\', [StringComparison]::OrdinalIgnoreCase)
}
function Assert-NoLinkAncestors([string]$Path) {
    $current = Get-Item -LiteralPath $Path -Force
    while ($null -ne $current) {
        if ($current.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point: $($current.FullName)" }
        $current = if ($current -is [IO.DirectoryInfo]) { $current.Parent } else { $current.Directory }
    }
}
function TreeFacts([string]$Path) {
    Assert-NoLinkAncestors $Path
    $files = [Collections.Generic.List[object]]::new()
    $dirs = [Collections.Generic.List[object]]::new()
    $pending = [Collections.Generic.Stack[string]]::new()
    $pending.Push($Path)
    [long]$bytes = 0
    $latest = (Get-Item -LiteralPath $Path -Force).LastWriteTimeUtc
    while ($pending.Count) {
        $dir = $pending.Pop()
        foreach ($entry in Get-ChildItem -LiteralPath $dir -Force -ErrorAction Stop) {
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked descendant: $($entry.FullName)" }
            if ($entry.Name -match '^(\.git|\.env|\.keep|\.retain|KEEP(?:\.txt)?|DO_NOT_DELETE|PINNED|\.pin)$|保留|待验收|\.sqlite(?:3)?(?:-wal|-shm)?$|\.db$|\.(pem|pfx|key)$') { throw "Protected content or marker: $($entry.FullName)" }
            if ($entry.LastWriteTimeUtc -gt $latest) { $latest = $entry.LastWriteTimeUtc }
            if ($entry.PSIsContainer) { $dirs.Add($entry); $pending.Push($entry.FullName) }
            else { $files.Add($entry); $bytes += $entry.Length }
        }
    }
    [pscustomobject]@{Bytes=$bytes;Latest=$latest;Files=$files;Directories=$dirs}
}
function FreeSpace {
    foreach ($drive in [IO.DriveInfo]::GetDrives()) {
        if ($drive.DriveType -eq 'Fixed' -and $drive.IsReady) { [pscustomobject]@{Drive=$drive.Name.Substring(0,1);FreeBytes=$drive.AvailableFreeSpace} }
    }
}
function PackageApplications([string]$Path) {
    foreach ($name in $policy.ApplicationNames) {
        $candidate = Join-Path $Path ($name + '-win32-x64')
        if (Test-Path -LiteralPath $candidate -PathType Container) { Get-Item -LiteralPath $candidate -Force }
    }
}
function ValidPackage([string]$Path) {
    $payloads = @(PackageApplications $Path)
    if ($payloads.Count -ne 1) { return $false }
    $app = $payloads[0]
    $exe = $app.Name.Substring(0,$app.Name.Length - '-win32-x64'.Length) + '.exe'
    return ((Test-Path -LiteralPath (Join-Path $app.FullName 'resources\app.asar') -PathType Leaf) -and
            (Test-Path -LiteralPath (Join-Path $app.FullName $exe) -PathType Leaf))
}
function Fingerprint($Rows) {
    $json = ConvertTo-Json -InputObject @($Rows | Sort-Object Path) -Depth 4 -Compress
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes([string]$json)))
}
function Assert-NoCompiler {
    $busy = @(Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object Name -match '^(cargo|rustc|rustdoc|cl|link|msbuild|cmake)(\.exe)?$')
    if ($busy.Count) { throw "Compiler active: $($busy[0].Name)" }
}
function Read-DockerMetadata([string[]]$Arguments) {
    $si = [Diagnostics.ProcessStartInfo]::new()
    $si.FileName = 'docker'; $si.UseShellExecute = $false; $si.CreateNoWindow = $true
    $si.RedirectStandardOutput = $true; $si.RedirectStandardError = $true
    foreach ($a in $Arguments) { $si.ArgumentList.Add($a) }
    $p = [Diagnostics.Process]::new(); $p.StartInfo = $si
    try {
        [void]$p.Start()
        $outputTask = $p.StandardOutput.ReadToEndAsync()
        $errorTask = $p.StandardError.ReadToEndAsync()
        if (-not $p.WaitForExit(30000)) { throw 'Docker reference inspection timed out; preserve cache' }
        if ($p.ExitCode -ne 0) { throw 'Docker reference inspection failed; preserve cache' }
        $outputTask.GetAwaiter().GetResult()
    } finally { $p.Dispose() }
}
function Assert-RustNotMounted([string]$Path) {
    $backend = @(Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object Name -eq 'com.docker.backend.exe')
    if (-not $backend.Count) { return }
    $ids = @((Read-DockerMetadata @('ps','-aq')) -split '\r?\n' | Where-Object { $_ })
    if (-not $ids.Count) { return }
    $raw = Read-DockerMetadata (@('inspect','--format','{{json .Mounts}}') + $ids)
    $lines = @($raw -split '\r?\n' | Where-Object { $_ })
    if ($lines.Count -ne $ids.Count) { throw 'Incomplete Docker mount inspection' }
    foreach ($line in $lines) {
        foreach ($mount in @($line | ConvertFrom-Json)) {
            if ($mount.Type -ne 'bind') { continue }
            $q = [string]$mount.Source
            if ($q -match '^/(run/desktop/mnt/host|host_mnt|mnt)/([a-z])(?:/(.*))?$') {
                $q = $Matches[2].ToUpper() + ':\' + $Matches[3].Replace('/','\')
            }
            if ($q -notmatch '^[A-Za-z]:') { continue }
            if ((Full $q) -eq (Full $Path) -or (IsUnder $Path $q) -or (IsUnder $q $Path)) {
                throw "Docker bind mount intersects cache: $q"
            }
        }
    }
}

try {
    $started = Get-Date
    $before = @(FreeSpace)
    $results = [Collections.Generic.List[object]]::new()
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    $services = @(Get-CimInstance Win32_Service -ErrorAction Stop | Where-Object PathName | Select-Object -ExpandProperty PathName)
    $tasks = @(Get-ScheduledTask -ErrorAction Stop | ForEach-Object { $_.Actions | ForEach-Object { $action=$_; foreach($name in @('Execute','Arguments','WorkingDirectory')) { $property=$action.PSObject.Properties[$name]; if($null -ne $property) { $property.Value } } } } | Where-Object { $_ })
    $references = [Collections.Generic.List[object]]::new()
    $shell = New-Object -ComObject WScript.Shell
    $systemShortcutRoots = @('DesktopDirectory','CommonDesktopDirectory','StartMenu','CommonStartMenu') | ForEach-Object { [Environment]::GetFolderPath($_) } | Where-Object { $_ }
    foreach ($shortcutRoot in @(($systemShortcutRoots + @($policy.ShortcutRoots)) | Sort-Object -Unique)) {
        if (Test-Path -LiteralPath $shortcutRoot) {
            foreach ($lnk in Get-ChildItem -LiteralPath $shortcutRoot -Filter '*.lnk' -Recurse -Force -ErrorAction Stop) {
                $sc = $shell.CreateShortcut($lnk.FullName)
                $references.Add([pscustomobject]@{Source=$lnk.FullName;Text=($sc.TargetPath+' '+$sc.Arguments+' '+$sc.WorkingDirectory)})
            }
        }
    }
    foreach ($s in $services) { $references.Add([pscustomobject]@{Source='Windows service';Text=$s}) }
    foreach ($t in $tasks) { $references.Add([pscustomobject]@{Source='Scheduled task';Text=$t}) }

    Assert-NoLinkAncestors $policy.Repository
    $repoTop = & git -C $policy.Repository rev-parse --show-toplevel
    if ($LASTEXITCODE -ne 0 -or (Full $repoTop) -ne (Full $policy.Repository)) { throw 'Repository must name the checkout root.' }
    $worktrees = @(& git -c core.quotepath=false -C $policy.Repository worktree list --porcelain)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inventory registered worktrees.' }
    $roots = @($worktrees | Where-Object { $_.StartsWith('worktree ') } | ForEach-Object { Full $_.Substring(9) })
    $common = Full (& git -C $policy.Repository rev-parse --path-format=absolute --git-common-dir)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot determine repository identity.' }
    $candidates = [Collections.Generic.List[object]]::new()
    foreach ($root in $roots) {
        if (-not (Test-Path -LiteralPath $root -PathType Container)) { continue }
        Assert-NoLinkAncestors $root
        $identity = Full (& git -C $root rev-parse --path-format=absolute --git-common-dir)
        if ($LASTEXITCODE -ne 0 -or $identity -ne $common) { throw "Unexpected repository at $root" }
        # Source and immediate local launch scripts are read only for path references.
        $scriptFiles = [Collections.Generic.List[object]]::new()
        foreach ($dir in @($root,(Join-Path $root '.local'),(Join-Path $root 'scripts'))) {
            if (Test-Path -LiteralPath $dir) {
                foreach ($f in Get-ChildItem -LiteralPath $dir -File -Force -ErrorAction Stop | Where-Object Extension -in '.ps1','.cmd','.bat','.vbs','.js','.mjs','.ts','.json') {
                    if ($f.Length -lt 2MB -and $f.Name -notmatch 'account|credential|secret|token|auth|password') { $scriptFiles.Add($f) }
                }
            }
        }
        foreach ($f in $scriptFiles) { $references.Add([pscustomobject]@{Source=$f.FullName;Text=(Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop)}) }
        $packageParent = Join-Path $root '.local\desktop-package'
        if (@($policy.ApplicationNames).Count -gt 0 -and (Test-Path -LiteralPath $packageParent)) {
            Assert-NoLinkAncestors $packageParent
            $packages = @(Get-ChildItem -LiteralPath $packageParent -Directory -Force | Where-Object Name -match '^build-[a-zA-Z0-9]+$' | Sort-Object LastWriteTimeUtc -Descending)
            $valid = @($packages | Where-Object { ValidPackage $_.FullName })
            $retained = @($valid | Select-Object -First $policy.KeepValidPackages | Select-Object -ExpandProperty FullName)
            foreach ($p in $packages) {
                $reason = if ($p.FullName -in $retained) { 'latest-valid-package' } elseif ($valid.Count -lt $policy.KeepValidPackages) { 'insufficient-valid-replacements' } elseif (-not (ValidPackage $p.FullName)) { 'unconfirmed-package' } else { '' }
                $candidates.Add([pscustomobject]@{Path=$p.FullName;Root=$root;Kind='desktop-package';InitialSkip=$reason;GitCheck=$true})
            }
        }
    }
    foreach ($cache in $policy.RustCaches) {
        $cachePath = Full $cache
        if (-not (Test-Path -LiteralPath $cachePath -PathType Container)) { continue }
        $owners = @($roots | Where-Object { IsUnder $cachePath $_ } | Sort-Object Length -Descending)
        if (-not $owners.Count) { throw "Cache outside approved repository worktrees: $cachePath" }
        if ($cachePath -notmatch '\\.local\\upstream-build\\target-windows\\(?:debug|release)\\(?:incremental|deps|build)$') { throw "Unexpected cache layout: $cachePath" }
        $candidates.Add([pscustomobject]@{Path=$cachePath;Root=$owners[0];Kind='rust-cache';InitialSkip='';GitCheck=$true})
    }
    if ($policy.PSObject.Properties['RustTargetDefinitions']) {
        foreach ($definition in $policy.RustTargetDefinitions) {
            foreach ($location in @($definition.TargetRoot,$definition.SourceManifest)) {
                if (-not [IO.Path]::IsPathFullyQualified($location) -or $location -notmatch '^[A-Za-z]:\\') { throw 'Rust definitions require absolute local paths.' }
            }
            $targetRoot = Full $definition.TargetRoot
            if ((Full ([IO.Path]::GetPathRoot($targetRoot))) -eq $targetRoot) { throw 'A drive root cannot be a Cargo target.' }
            if (-not (Test-Path -LiteralPath $targetRoot -PathType Container)) { continue }
            Assert-NoLinkAncestors $targetRoot
            Assert-NoLinkAncestors $definition.SourceManifest
            if (-not (Test-Path -LiteralPath (Join-Path $targetRoot 'CACHEDIR.TAG') -PathType Leaf) -or
                -not (Test-Path -LiteralPath $definition.SourceManifest -PathType Leaf) -or
                (Split-Path $definition.SourceManifest -Leaf) -ne 'Cargo.toml') { throw "Unverified Rust target: $targetRoot" }
            foreach ($profile in $definition.Profiles) {
                if ($profile -notin @('debug','release','x86_64-pc-windows-msvc/release')) { throw 'Unexpected Rust profile' }
                foreach ($name in @('incremental','deps','build')) {
                    $p = Join-Path $targetRoot "$profile\$name"
                    if (Test-Path -LiteralPath $p -PathType Container) {
                        $candidates.Add([pscustomobject]@{Path=$p;Root=$targetRoot;Kind='rust-cache';InitialSkip='';GitCheck=$false})
                    }
                }
            }
        }
    }

    # Search nested launch scripts for package keys; immediate JSON/config references above remain protected.
    # rg does not follow reparse directories by default. Exclude bundled code, credentials and session bodies.
    $packageCandidates = @($candidates | Where-Object { $_.Kind -eq 'desktop-package' -and -not $_.InitialSkip })
    if ($packageCandidates.Count) {
        $referenceRoots = @($packageCandidates.Root | Select-Object -Unique)
        $rgArguments = @('-l','-F','--hidden','--no-ignore','--max-filesize','2M')
        foreach ($extension in @('ps1','cmd','bat','vbs','js','mjs','ts','py')) { $rgArguments += @('-g',("*."+$extension)) }
        foreach ($directory in @('.git','node_modules','desktop-package','desktop-installer','target','target-windows','sessions','archived_sessions')) {
            $rgArguments += @('-g',("!**/"+$directory+"/**"))
        }
        foreach ($word in @('credential','secret','token','password')) { $rgArguments += @('--iglob',("!**/*"+$word+"*")) }
        foreach ($key in @($packageCandidates | ForEach-Object { Split-Path $_.Path -Leaf } | Select-Object -Unique)) {
            $rgArguments += @('-e',$key)
        }
        $rgArguments += @('--') + $referenceRoots
        $referenceHits = @(& rg @rgArguments)
        if ($LASTEXITCODE -gt 1) { throw 'Nested launch reference scan incomplete; no deletion performed.' }
        foreach ($file in $referenceHits) {
            Assert-NoLinkAncestors $file
            $references.Add([pscustomobject]@{Source=$file;Text=(Get-Content -LiteralPath $file -Raw -ErrorAction Stop)})
        }
    }

    foreach ($candidate in $candidates) {
        $item = [ordered]@{Path=$candidate.Path;Kind=$candidate.Kind;Status='skipped';Reason=$candidate.InitialSkip;LogicalBytes=0;FileCount=0;DeletePath=$null;ManifestHash=$null;SelectedFiles=@();PreservedFiles=@();DeletedFiles=@()}
        try {
            if ($candidate.InitialSkip) { $results.Add([pscustomobject]$item); continue }
            $path = Full $candidate.Path
            if (-not (IsUnder $path $candidate.Root)) { throw 'Path outside worktree boundary' }
            if ($candidate.Kind -eq 'desktop-package' -and (Split-Path $path -Parent) -ne (Join-Path $candidate.Root '.local\desktop-package')) { throw 'Invalid package parent' }
            foreach ($pin in $policy.ProtectedPaths) {
                if ($path -eq (Full $pin) -or (IsUnder $path $pin) -or (IsUnder $pin $path)) { throw "Explicitly protected: $pin" }
            }
            $ancestor = $path
            while ($ancestor -and (IsUnder $ancestor $candidate.Root)) {
                foreach ($marker in @('.keep','.retain','KEEP','KEEP.txt','DO_NOT_DELETE','.pin','PINNED')) {
                    if (Test-Path -LiteralPath (Join-Path $ancestor $marker)) { throw "Retention marker: $ancestor\$marker" }
                }
                $ancestor = Split-Path $ancestor -Parent
            }
            $relative = [IO.Path]::GetRelativePath($candidate.Root,$path).Replace('\','/')
            $gitRoot = if ($candidate.GitCheck) { $candidate.Root } else {
                $parent = [IO.DirectoryInfo]::new($path)
                while ($null -ne $parent) {
                    if (Test-Path -LiteralPath (Join-Path $parent.FullName '.git')) { $parent.FullName; break }
                    $parent = $parent.Parent
                }
            }
            if ($gitRoot) {
                $gitRelative = [IO.Path]::GetRelativePath($gitRoot,$path).Replace('\','/')
                $tracked = @(& git -C $gitRoot ls-files -- $gitRelative)
                if ($LASTEXITCODE -ne 0 -or $tracked.Count) { throw 'Tracked files or Git inspection failed' }
                & git -C $gitRoot check-ignore -q -- $gitRelative
                if ($LASTEXITCODE -ne 0) { throw 'Candidate is not ignored generated output' }
            }
            $live = @(Get-CimInstance Win32_Process -ErrorAction Stop)
            foreach ($proc in $live) {
                if ($proc.ProcessId -eq $PID) { continue }
                $text = [string]$proc.ExecutablePath + ' ' + [string]$proc.CommandLine
                $normal = $text.Replace('/','\').Replace('\\','\')
                if ($normal.IndexOf($path,[StringComparison]::OrdinalIgnoreCase) -ge 0) { throw "Referenced by active process $($proc.ProcessId)" }
                if ($candidate.Kind -eq 'rust-cache' -and $proc.Name -match '^(cargo|rustc|rustdoc|cl|link|msbuild|cmake)(\.exe)?$') { throw "Compiler active: $($proc.Name)" }
                # A process referring only to a worktree is not evidence that every old package is in use.
                if ($candidate.Kind -eq 'desktop-package' -and
                    $normal.IndexOf($candidate.Root,[StringComparison]::OrdinalIgnoreCase) -ge 0 -and
                    $normal -match '(package-desktop|electron-builder|electron-packager|make-installer|build-desktop)') {
                    throw "Packaging process active in worktree: $($proc.ProcessId)"
                }
            }
            foreach ($reference in $references) {
                $text = ([string]$reference.Text).Replace('/','\').Replace('\\','\')
                $relativeWin = $relative.Replace('/','\')
                $packageKeyMatch = $candidate.Kind -eq 'desktop-package' -and $text.IndexOf((Split-Path $path -Leaf),[StringComparison]::OrdinalIgnoreCase) -ge 0
                if ($packageKeyMatch -or $text.IndexOf($path,[StringComparison]::OrdinalIgnoreCase) -ge 0 -or $text.IndexOf($relativeWin,[StringComparison]::OrdinalIgnoreCase) -ge 0) { throw "Launch/reference match: $($reference.Source)" }
            }
            if ($candidate.Kind -eq 'rust-cache') { Assert-RustNotMounted $path }
            $deletePath = $path
            if ($candidate.Kind -eq 'desktop-package') {
                # Inspect markers throughout the build, but retain outer manifests, hashes, logs and evidence.
                $null = TreeFacts $path
                $apps = @(PackageApplications $path)
                if ($apps.Count -ne 1) { throw 'Ambiguous package application directory' }
                $deletePath = Full $apps[0].FullName
                if (-not (IsUnder $deletePath $path) -or (Split-Path $deletePath -Parent) -ne $path) { throw 'Invalid application boundary' }
            }
            $facts = TreeFacts $deletePath
            $item.LogicalBytes = $facts.Bytes
            $item.FileCount = $facts.Files.Count
            if ($candidate.Kind -eq 'desktop-package') {
                if ([double]$policy.MinimumAgeDays -gt 0 -and $facts.Latest -gt [DateTime]::UtcNow.AddDays(-[double]$policy.MinimumAgeDays)) { throw 'Package still inside configured retention age' }
            } else {
                $idleHours = if ($policy.PSObject.Properties['RustMinimumIdleHours']) { [double]$policy.RustMinimumIdleHours } else { 168 }
                if ($facts.Latest -gt [DateTime]::UtcNow.AddHours(-$idleHours)) { throw "Rust cache written within $idleHours hours" }
            }
            $snapshots = @($facts.Files | ForEach-Object { [DiskCareLeafInfo]::Read($_.FullName) })
            $item.ManifestHash = Fingerprint $snapshots
            $item.DeletePath = $deletePath
            if ($candidate.Kind -eq 'rust-cache') {
                # Delete only known compiled leaf formats, retaining shared links, source, manifests and evidence.
                $extensions = @('.rlib','.rmeta','.pdb','.d','.obj','.o','.lib','.a','.so','.dll','.exe','.exp','.ilk','.bin')
                $item.SelectedFiles = @($snapshots | Where-Object { $_.Links -eq 1 -and [IO.Path]::GetExtension($_.Path) -in $extensions })
                $item.PreservedFiles = @($snapshots | Where-Object { $_.Links -ne 1 -or [IO.Path]::GetExtension($_.Path) -notin $extensions } | Select-Object -ExpandProperty Path)
                if (-not $item.SelectedFiles.Count) { throw 'No disposable single-link compiled leaves' }
            } else {
                $item.SelectedFiles = $snapshots
            }
            if ($Apply) {
                $approved = @($review.Results | Where-Object { $_.Path -eq $path -and $_.Status -eq 'eligible' })
                if ($approved.Count -ne 1 -or $approved[0].ManifestHash -ne $item.ManifestHash -or $approved[0].DeletePath -ne $deletePath) {
                    throw 'Candidate absent from reviewed preview or file identities changed'
                }
            }
            $item.Status = 'eligible'
            $item.Reason = 'validated-generated-output'
            if ($Apply) {
                Assert-NoLinkAncestors $path
                Assert-NoLinkAncestors $deletePath
                if ($candidate.Kind -eq 'desktop-package') {
                    Write-Output "Removing reviewed application payload; preserving outer build evidence: $deletePath"
                    Remove-Item -LiteralPath $deletePath -Recurse -Force -ErrorAction Stop
                    if (Test-Path -LiteralPath $deletePath) { throw 'Application remains after removal' }
                    $item.DeletedFiles = @($snapshots.Path)
                } else {
                    Assert-NoCompiler
                    $deleted = [Collections.Generic.List[string]]::new()
                    foreach ($f in $item.SelectedFiles) {
                        if ($deleted.Count % 200 -eq 0) { Assert-NoCompiler }
                        $leaf = Full $f.Path
                        if (-not (IsUnder $leaf $path)) { throw 'Leaf escaped approved cache boundary' }
                        Assert-NoLinkAncestors $leaf
                        $fresh = [DiskCareLeafInfo]::Read($leaf)
                        if ($fresh.Id -ne $f.Id -or $fresh.Bytes -ne $f.Bytes -or $fresh.WriteTicks -ne $f.WriteTicks -or $fresh.Links -ne 1) { throw "Changed Rust leaf: $leaf" }
                        Remove-Item -LiteralPath $leaf -ErrorAction Stop
                        $deleted.Add($leaf)
                        $item.DeletedFiles = $deleted.ToArray()
                    }
                }
                $item.Status = 'deleted'
            }
        } catch {
            $item.Reason = $_.Exception.Message
            if ($Apply -and $item.Status -eq 'eligible') { $item.Status = 'failed-or-partial' } else { $item.Status = 'skipped' }
        }
        $results.Add([pscustomobject]$item)
    }
    $after = @(FreeSpace)
    $report = [ordered]@{
        SchemaVersion=2;StartedAt=$started.ToString('o');FinishedAt=(Get-Date).ToString('o');Applied=[bool]$Apply
        PolicyHash=$policyHash;ScriptHash=$scriptHash;ReviewedPreview=$ReviewedPreview
        Before=$before;After=$after
        DriveDeltas=@($after | ForEach-Object { $d=$_; $old=$before | Where-Object Drive -eq $d.Drive; [pscustomobject]@{Drive=$d.Drive;AvailableBytesChange=$d.FreeBytes-$old.FreeBytes} })
        Results=$results.ToArray();Note='LogicalBytes are estimates, not freed space. Actual drive deltas also include concurrent activity.'
    }
    [void][IO.Directory]::CreateDirectory($reportDirectory)
    $name = (Get-Date -Format 'yyyyMMdd-HHmmssfff') + '-' + [Guid]::NewGuid().ToString('N') + $(if($Apply){'-cleanup.json'}else{'-preview.json'})
    $reportFile = Join-Path $reportDirectory $name
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportFile -Encoding utf8
    [pscustomobject]@{Report=$reportFile;Applied=[bool]$Apply;Counts=@($results | Group-Object Status | Select-Object Name,Count);DriveDeltas=$report.DriveDeltas;Results=$results.ToArray()} | ConvertTo-Json -Depth 7 -Compress
} finally {
    $mutex.ReleaseMutex()
    $mutex.Dispose()
}
