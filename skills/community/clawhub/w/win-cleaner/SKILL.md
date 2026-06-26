---
name: win-cleaner
description: Deep clean Windows C drive junk files to maximize free space. Analyzes disk usage, identifies safe-to-delete items, and cleans caches, temp files, logs, browser data, application caches, Windows Store, .NET, game, and video-conferencing caches while protecting user data and system stability. Use whenever the user asks to clean C drive, free up disk space, remove junk files, optimize Windows storage, or when C drive is full or running low.
---

# Windows C Drive Deep Cleaner

You are a disk cleanup specialist. This skill uses a **scan-first, pattern-match, clean-later** strategy that adapts to any Windows computer.

**Primary directive:** Maximize freed space while guaranteeing zero user data loss and zero system stability impact.

---

## Expected Yield Per Phase

Use this to prioritize if the user wants a quick clean vs. deep clean:

| Phase | Typical Yield | Time | Priority |
|-------|--------------|------|----------|
| 4a (Package managers) | 2-6 GB | 1-2 min | HIGH — always run |
| 4b (Windows junk) | 0.5-4 GB | 2-3 min | HIGH — always run |
| 4c (DISM) | 0.5-3 GB | 5-10 min | MEDIUM |
| 4d (VSS resize) | 0.5-2 GB | 1 min | MEDIUM |
| 4e (Windows Store / .NET) | 0.3-2 GB | 1-2 min | HIGH — always run |
| 5a (Pattern caches) | 0.5-3 GB | 2-5 min | HIGH — always run |
| 5b (Browser caches) | 0.3-2 GB | 1-2 min | HIGH — always run |
| 5c-e (IDE/Corrupted/GPU) | 0.1-2 GB | 1-3 min | MEDIUM |
| 5f-5n (App specific) | 0.5-5 GB | 2-5 min | HIGH — always run |
| 6 (User decisions) | 2-10 GB | varies | Depends on user |

If user asks for "quick clean": Phases 1 → 4a → 4b → 4e → 5a → 5b → 5f → 5g → 7. Skip DISM and VSS.
If user asks for "deep clean": All phases in order.

---

## Safety Guarantees

### What This Skill Will NEVER Do

- Delete any file from `C:\Windows\System32`, `C:\Windows\SysWOW64`, or `C:\Windows\WinSxS` (except via DISM which is safe)
- Delete any file from `C:\Windows\System32\DriverStore` (driver store)
- Delete `.exe`, `.dll`, `.sys`, `.msi`, `.msix` files anywhere on disk
- Delete any file from `C:\Program Files` or `C:\Program Files (x86)`
- Delete any file from user Documents, Pictures, Music, Videos unless it's a provably corrupted database dump
- Delete any registry keys or system configuration
- Delete Windows Store app packages (`WindowsApps`) — only clear their caches
- Run `format`, `cleanmgr /sageset`, or any tool that opens a GUI
- Execute destructive commands like `rm -rf C:\` or `del /f /s C:\*`
- Disable hiberfil.sys or pagefile.sys without explicit user confirmation

### Pattern Matching Safety Rules

When using regex to find cache folders, apply these constraints:

1. **Match whole directory name** only — use exact equality (`-eq`, `-contains`), never substring matching (`-match`, `-like`)
2. **Do NOT match** directory names that merely *contain* cache words (e.g., "MyCacheProject", "cache_manager", "template-parser")
3. **Skip** any directory that contains a `.git` subfolder, `package.json`, `Cargo.toml`, or `CMakeLists.txt` file (indicates a project, not cache)
4. **Skip** directories with a `Readme` or `README` file
5. **Only search within AppData and known dev-tool paths** — never search Documents, Desktop, or Downloads for pattern-based cleaning

### Pre-Flight Safety Checks

Before any deletion, verify:
- The target is not a reparse point or junction that points to a data drive (check via `Get-Item $path | Select-Object LinkType`)
- The folder was last modified more than 1 minute ago (not a running process's active temp)

---

## Phase 1: Disk Overview

Run these 3 commands in parallel:

```powershell
# 1a. Disk usage summary
Get-PSDrive C | ForEach-Object {
    $total = [math]::Round(($_.Used + $_.Free)/1GB, 2)
    $used  = [math]::Round($_.Used/1GB, 2)
    $free  = [math]::Round($_.Free/1GB, 2)
    $pct   = [math]::Round($_.Used/($_.Used+$_.Free)*100, 1)
    Write-Host "C: Total=${total}GB Used=${used}GB Free=${free}GB Usage=${pct}%"
    Write-Host "PHASE1_USED=$used"
}

# 1b. Top-level directory sizes (excluding reparse points)
Get-ChildItem C:\ -Directory -ErrorAction SilentlyContinue -Attributes !ReparsePoint | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
             Where-Object { !$_.PSIsContainer } |
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB,2)}
} | Sort-Object SizeGB -Descending | Format-Table -AutoSize

# 1c. User profile sizes
Get-ChildItem C:\Users -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
             Where-Object { !$_.PSIsContainer } |
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    [PSCustomObject]@{User=$_.Name; SizeGB=[math]::Round($size/1GB,2)}
} | Sort-Object SizeGB -Descending | Format-Table -AutoSize
```

---

## Phase 2: Comprehensive System Junk Scan

Run these in parallel (2-3 PowerShell calls):

### 2a. Windows System Temp & Log Locations

```powershell
$locations = @(
    [PSCustomObject]@{Name="Windows Temp";           Path="C:\Windows\Temp"},
    [PSCustomObject]@{Name="User Temp";              Path=$env:TEMP},
    [PSCustomObject]@{Name="Prefetch";               Path="C:\Windows\Prefetch"},
    [PSCustomObject]@{Name="Update Downloads";       Path="C:\Windows\SoftwareDistribution\Download"},
    [PSCustomObject]@{Name="Delivery Optimization";  Path="C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization"},
    [PSCustomObject]@{Name="Error Reports";          Path="C:\ProgramData\Microsoft\Windows\WER"},
    [PSCustomObject]@{Name="Panther Setup Logs";     Path="C:\Windows\Panther"},
    [PSCustomObject]@{Name="CBS Logs";               Path="C:\Windows\Logs\CBS"},
    [PSCustomObject]@{Name="DISM Logs";              Path="C:\Windows\Logs\DISM"},
    [PSCustomObject]@{Name="Windows Installer";      Path="C:\Windows\Installer"},
    [PSCustomObject]@{Name="ProgramData Pkg Cache";  Path="C:\ProgramData\Package Cache"},
    [PSCustomObject]@{Name="Thumbnail Cache";        Path="$env:LOCALAPPDATA\Microsoft\Windows\Explorer"},
    [PSCustomObject]@{Name="Font Cache";             Path="$env:LOCALAPPDATA\Microsoft\Windows\Fonts"},
    [PSCustomObject]@{Name="Teams Cache";            Path="$env:APPDATA\Microsoft\Teams"},
    [PSCustomObject]@{Name="Teams (new) Cache";      Path="$env:LOCALAPPDATA\Packages\MSTeams_8wekyb3d8bbwe\LocalCache"},
    [PSCustomObject]@{Name="Cortana Cache";          Path="$env:LOCALAPPDATA\Packages\Microsoft.Windows.Cortana_cw5n1h2txyewy\LocalState"},
    [PSCustomObject]@{Name="Windows Search Index";   Path="C:\ProgramData\Microsoft\Search\Data\Applications\Windows"},
    [PSCustomObject]@{Name="MRT Quarantine";         Path="C:\Windows\system32\MRT\Quarantine"},
    [PSCustomObject]@{Name="SCCM Cache";             Path="C:\Windows\ccmcache"}
)

foreach ($loc in $locations) {
    if (Test-Path $loc.Path) {
        $size = (Get-ChildItem $loc.Path -Recurse -ErrorAction SilentlyContinue |
                 Where-Object { !$_.PSIsContainer } |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 1MB) {
            [PSCustomObject]@{Location=$loc.Name; SizeMB=[math]::Round($size/1MB,1)}
        }
    }
} | Sort-Object SizeMB -Descending | Format-Table -AutoSize
```

### 2b. Special Files & System State

```powershell
# Hibernation file
if (Test-Path C:\hiberfil.sys) {
    $h = Get-Item C:\hiberfil.sys -Force
    Write-Host "hiberfil.sys: $([math]::Round($h.Length/1GB,2)) GB"
    Write-Host "  → To disable: powercfg /h off  (frees RAM-size worth of space; disable only if you don't use Sleep/Hibernate)"
}
# Page file
if (Test-Path C:\pagefile.sys) {
    $p = Get-Item C:\pagefile.sys -Force
    Write-Host "pagefile.sys: $([math]::Round($p.Length/1GB,2)) GB (do NOT delete — required for system stability)"
}
# Swap file
if (Test-Path C:\swapfile.sys) {
    $s = Get-Item C:\swapfile.sys -Force
    Write-Host "swapfile.sys: $([math]::Round($s.Length/1GB,2)) GB"
}
# Windows.old
if (Test-Path C:\Windows.old) {
    $wo = (Get-ChildItem C:\Windows.old -Recurse -ErrorAction SilentlyContinue |
           Where-Object { !$_.PSIsContainer } |
           Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    Write-Host "Windows.old: $([math]::Round($wo/1GB,2)) GB  → Safe to remove via DISM /resetbase or Disk Cleanup"
}
# Memory dumps
Get-ChildItem C:\Windows\*.dmp -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "Crash dump: $($_.Name) = $([math]::Round($_.Length/1MB,1)) MB"
}
if (Test-Path C:\Windows\Memory.dmp) {
    $md = Get-Item C:\Windows\Memory.dmp
    Write-Host "Memory.dmp: $([math]::Round($md.Length/1GB,2)) GB"
}
# Live kernel dump
if (Test-Path C:\Windows\LiveKernelReports) {
    $lk = (Get-ChildItem C:\Windows\LiveKernelReports -Recurse -ErrorAction SilentlyContinue |
           Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($lk -gt 10MB) { Write-Host "LiveKernelReports: $([math]::Round($lk/1MB,1)) MB" }
}
# VSS / System Restore
vssadmin list shadowstorage 2>&1
# DISM component store analysis
dism /online /cleanup-image /analyzecomponentstore 2>&1 |
    Select-String -Pattern "recommend|Actual|claimed|cleanup" -SimpleMatch
```

### 2c. C:\ Root Orphan Detection

```powershell
# Find large non-system files at C:\ root
Get-ChildItem C:\ -File -ErrorAction SilentlyContinue | Where-Object {
    $_.Length -gt 50MB -and
    $_.Name -notin @('hiberfil.sys','pagefile.sys','swapfile.sys','DumpStack.log')
} | ForEach-Object {
    Write-Host "C:\$($_.Name): $([math]::Round($_.Length/1MB,1)) MB — suspicious large file at root"
}
# Check non-standard root directories
@("C:\tmp","C:\temp","C:\backup","C:\old","C:\dump") | ForEach-Object {
    if (Test-Path $_) {
        $size = (Get-ChildItem $_ -Recurse -ErrorAction SilentlyContinue |
                 Where-Object { !$_.PSIsContainer } |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 10MB) {
            Write-Host "$_ : $([math]::Round($size/1MB,1)) MB — non-standard root directory"
            Get-ChildItem $_ -Recurse -File -ErrorAction SilentlyContinue |
                Sort-Object Length -Descending | Select-Object -First 5 | ForEach-Object {
                Write-Host "  $($_.Name): $([math]::Round($_.Length/1MB,1)) MB"
            }
        }
    }
}
```

---

## Phase 3: Dynamic User Profile Discovery

### 3a. Deep AppData Scan — ALL three AppData roots (Local, Roaming, LocalLow)

LocalLow (`$env:USERPROFILE\AppData\LocalLow`) is often overlooked but can hold GPU driver caches, game saves, and app configs. It must be scanned.

```powershell
$appDataRoots = @{
    $env:LOCALAPPDATA                    = "Local"
    $env:APPDATA                         = "Roaming"
    "$env:USERPROFILE\AppData\LocalLow"  = "LocalLow"
}
foreach ($pair in $appDataRoots.GetEnumerator()) {
    $root = $pair.Key; $rootName = $pair.Value
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $appName = $_.Name; $appPath = $_.FullName
        Get-ChildItem $appPath -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
                     Where-Object { !$_.PSIsContainer } |
                     Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            if ($size -gt 50MB) {
                [PSCustomObject]@{Scope=$rootName; App=$appName; Subfolder=$_.Name; SizeMB=[math]::Round($size/1MB,1)}
            }
        }
        $fileSize = (Get-ChildItem $appPath -File -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($fileSize -gt 100MB) {
            [PSCustomObject]@{Scope=$rootName; App=$appName; Subfolder="(root files)"; SizeMB=[math]::Round($fileSize/1MB,1)}
        }
    } | Sort-Object SizeMB -Descending | Format-Table -AutoSize
}
```

### 3b. Profile Root — All Directories (hidden AND visible)

This catches SDK caches, portable app data, and abandoned project folders that sit directly in the user's home directory. Many cleanup tools miss this because they only look at AppData.

```powershell
# 3b-1: Measure ALL directories in user root (hidden + visible), report > 50MB
Get-ChildItem $env:USERPROFILE -Directory -ErrorAction SilentlyContinue -Force | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
             Where-Object { !$_.PSIsContainer } |
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($size -gt 50MB) {
        $isHidden = ($_.Attributes -band [System.IO.FileAttributes]::Hidden) -eq [System.IO.FileAttributes]::Hidden
        $category = if ($_.Name -match '^\.')       { "Dev/SDK" }
                    elseif ($_.Name -eq 'go')        { "Go ecosystem" }
                    elseif ($_.Name -match 'node_modules') { "Node.js" }
                    elseif ($isHidden)               { "Hidden" }
                    else                             { "Standard" }
        [PSCustomObject]@{Folder=$_.Name; SizeMB=[math]::Round($size/1MB,1); Hidden=$isHidden; Category=$category}
    }
} | Sort-Object SizeMB -Descending | Format-Table -AutoSize

# 3b-2: Identify known-cleanable SDK caches (safe to auto-clean later)
Write-Host "`n=== Identifiable SDK caches in user root ==="
$knownCaches = @{
    "$env:USERPROFILE\.openjfx\cache"        = "JavaFX cache"
    "$env:USERPROFILE\.cache"                = "XDG cache (Linux-tool cache on Windows)"
    "$env:USERPROFILE\go\pkg"                = "Go module cache"
    "$env:USERPROFILE\.go\pkg"               = "Go module cache (hidden)"
    "$env:USERPROFILE\.shiv"                 = "Python shiv tool cache"
    "$env:USERPROFILE\.cargo\registry\cache" = "Cargo registry cache"
    "$env:USERPROFILE\.gradle\caches"        = "Gradle cache"
    "$env:USERPROFILE\.m2\repository"        = "Maven repo cache"
    "$env:USERPROFILE\.nuget\packages"       = "NuGet global packages"
    "$env:USERPROFILE\.electron"             = "Electron download cache"
    "$env:USERPROFILE\.node_repl_history"    = "Node REPL history"
    "$env:USERPROFILE\.yarn\cache"           = "Yarn v1 cache"
    "$env:USERPROFILE\AppData\Local\Yarn\Cache" = "Yarn v2/Berry cache"
    "$env:USERPROFILE\.pnpm-store"           = "pnpm store"
}
foreach ($pair in $knownCaches.GetEnumerator()) {
    if (Test-Path $pair.Key) {
        $s = (Get-ChildItem $pair.Key -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 10MB) { Write-Host "$($pair.Value): $([math]::Round($s/1MB,1)) MB — $($pair.Key)" }
    }
}
```

### 3c. Documents Deep Scan

```powershell
Get-ChildItem "$env:USERPROFILE\Documents" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
             Where-Object { !$_.PSIsContainer } |
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($size -gt 100MB) {
        [PSCustomObject]@{Folder=$_.Name; SizeMB=[math]::Round($size/1MB,1)}
    }
} | Sort-Object SizeMB -Descending | Format-Table -AutoSize

# Large individual files in Documents
Get-ChildItem "$env:USERPROFILE\Documents" -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 100MB } | Sort-Object Length -Descending |
    Select-Object -First 20 | ForEach-Object {
    Write-Host "$($_.Directory.Name)\$($_.Name): $([math]::Round($_.Length/1MB,1)) MB"
}
```

### 3d. Desktop & Downloads Scan

```powershell
# Desktop
Write-Host "=== Desktop ==="
$desktopSize = (Get-ChildItem "$env:USERPROFILE\Desktop" -Recurse -ErrorAction SilentlyContinue |
                Where-Object { !$_.PSIsContainer } |
                Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host "Total: $([math]::Round($desktopSize/1GB,2)) GB"
Get-ChildItem "$env:USERPROFILE\Desktop" -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 20MB } | Sort-Object Length -Descending |
    Select-Object -First 15 | ForEach-Object {
    Write-Host "  $($_.Name): $([math]::Round($_.Length/1MB,1)) MB"
}

# Downloads (report only, never auto-clean)
Write-Host "`n=== Downloads ==="
$dlSize = (Get-ChildItem "$env:USERPROFILE\Downloads" -Recurse -ErrorAction SilentlyContinue |
           Where-Object { !$_.PSIsContainer } |
           Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host "Total: $([math]::Round($dlSize/1GB,2)) GB (NOT auto-cleaned — user decision only)"
# Report old installer files as candidates
Get-ChildItem "$env:USERPROFILE\Downloads" -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 100MB -and $_.Extension -in @('.exe','.msi','.iso','.zip','.7z','.rar') } |
    Sort-Object Length -Descending | Select-Object -First 10 | ForEach-Object {
    Write-Host "  Large installer/archive: $($_.Name) ($([math]::Round($_.Length/1MB,1)) MB)"
}
```

### 3e. Environment-Specific Detection

```powershell
# Docker
$dockerData    = "$env:USERPROFILE\.docker"
$dockerDesktop = "$env:LOCALAPPDATA\Docker"
if ((Test-Path $dockerData) -or (Test-Path $dockerDesktop)) {
    Write-Host "Docker detected. Disk usage:"
    docker system df 2>$null
}

# WSL
wsl --list --verbose 2>$null
if (Test-Path "$env:LOCALAPPDATA\Packages") {
    $wslDirs = Get-ChildItem "$env:LOCALAPPDATA\Packages" -Directory -ErrorAction SilentlyContinue |
               Where-Object { $_.Name -match "Canonical|WSL|Debian|Ubuntu|kali" }
    foreach ($d in $wslDirs) {
        $size = (Get-ChildItem $d.FullName -Recurse -ErrorAction SilentlyContinue |
                 Where-Object { !$_.PSIsContainer } |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 100MB) {
            Write-Host "WSL distro $($d.Name): $([math]::Round($size/1GB,2)) GB"
        }
    }
}

# OneDrive
$oneDrive = "$env:USERPROFILE\OneDrive"
if (Test-Path $oneDrive) {
    $odSize = (Get-ChildItem $oneDrive -Recurse -ErrorAction SilentlyContinue |
               Where-Object { !$_.PSIsContainer } |
               Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    Write-Host "OneDrive local: $([math]::Round($odSize/1GB,2)) GB (cloud-synced files — NEVER auto-delete)"
}

# Steam
foreach ($steamPath in @("C:\Program Files (x86)\Steam", "$env:LOCALAPPDATA\Steam")) {
    if (Test-Path "$steamPath\steamapps") {
        $steamSize = (Get-ChildItem "$steamPath\steamapps" -Recurse -ErrorAction SilentlyContinue |
                      Where-Object { !$_.PSIsContainer } |
                      Measure-Object -Property Length -Sum).Sum
        Write-Host "Steam games ($steamPath): $([math]::Round($steamSize/1GB,2)) GB"
    }
}

# Adobe Creative Cloud cache
$adobeCC = "$env:LOCALAPPDATA\Adobe\CoreSync"
if (Test-Path $adobeCC) {
    $aSize = (Get-ChildItem $adobeCC -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($aSize -gt 100MB) { Write-Host "Adobe CoreSync: $([math]::Round($aSize/1MB,1)) MB" }
}

# Zoom
$zoomAppData = "$env:APPDATA\Zoom"
if (Test-Path $zoomAppData) {
    $zSize = (Get-ChildItem $zoomAppData -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($zSize -gt 50MB) { Write-Host "Zoom AppData: $([math]::Round($zSize/1MB,1)) MB" }
}
```

### 3f. Additional User Root Scan

```powershell
# Yarn / pnpm / bun
foreach ($toolCache in @(
    @{Path="$env:LOCALAPPDATA\Yarn\Cache"; Name="Yarn"},
    @{Path="$env:USERPROFILE\.pnpm-store"; Name="pnpm"},
    @{Path="$env:LOCALAPPDATA\pnpm\store"; Name="pnpm (local)"},
    @{Path="$env:USERPROFILE\.bun\install\cache"; Name="Bun"}
)) {
    if (Test-Path $toolCache.Path) {
        $s = (Get-ChildItem $toolCache.Path -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 50MB) { Write-Host "$($toolCache.Name) cache: $([math]::Round($s/1MB,1)) MB — $($toolCache.Path)" }
    }
}

# node_modules directly in user root (not inside a project)
Get-ChildItem $env:USERPROFILE -Directory -ErrorAction SilentlyContinue -Depth 1 |
    Where-Object { $_.Name -eq 'node_modules' -and $_.FullName -notlike '*\AppData\*' } |
    ForEach-Object {
        $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 50MB) { Write-Host "node_modules (non-project): $($_.FullName) ($([math]::Round($s/1MB,1)) MB)" }
    }

# Large .log, .tmp, .dump files directly in user root
Get-ChildItem $env:USERPROFILE -File -ErrorAction SilentlyContinue | Where-Object {
    $_.Length -gt 50MB -and $_.Extension -in @('.log','.tmp','.temp','.dump','.dmp','.etl')
} | ForEach-Object {
    Write-Host "Large junk file in user root: $($_.Name) ($([math]::Round($_.Length/1MB,1)) MB)"
}

# Versioned IDE directories
foreach ($ideDir in @(
    "$env:USERPROFILE\.vscode",
    "$env:USERPROFILE\.trae-cn",
    "$env:USERPROFILE\.cursor",
    "$env:USERPROFILE\.windsurf"
)) {
    if (-not (Test-Path $ideDir)) { continue }
    $ideSize = (Get-ChildItem $ideDir -Recurse -ErrorAction SilentlyContinue |
                Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($ideSize -gt 100MB) { Write-Host "IDE data $ideDir : $([math]::Round($ideSize/1MB,1)) MB" }
}
```

---

## Phase 4: Universal Safe Cleanup (Auto-Execute)

### 4a. Package Manager Caches

```powershell
$freed4a = 0

# pip
if (Get-Command pip -ErrorAction SilentlyContinue) { pip cache purge 2>&1 }
foreach ($p in @("$env:LOCALAPPDATA\pip\cache","$env:LOCALAPPDATA\pip\http","$env:LOCALAPPDATA\pip\selfcheck")) {
    if (Test-Path $p) {
        $s = (Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        $freed4a += $s
        Write-Host "pip $(Split-Path $p -Leaf): $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force $p -ErrorAction SilentlyContinue
    }
}

# uv
if (Get-Command uv -ErrorAction SilentlyContinue) { uv cache clean 2>&1 }
$uvCache = "$env:LOCALAPPDATA\uv\cache"
if (Test-Path $uvCache) {
    $s = (Get-ChildItem $uvCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    $freed4a += $s
    Write-Host "uv cache: $([math]::Round($s/1MB,1)) MB"
    Remove-Item -Recurse -Force $uvCache -ErrorAction SilentlyContinue
}

# npm
if (Get-Command npm -ErrorAction SilentlyContinue) { npm cache clean --force 2>&1 }

# Yarn v1
$yarnCache = "$env:LOCALAPPDATA\Yarn\Cache"
if (Test-Path $yarnCache) {
    $s = (Get-ChildItem $yarnCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 50MB) {
        $freed4a += $s
        Write-Host "Yarn cache: $([math]::Round($s/1MB,1)) MB"
        if (Get-Command yarn -ErrorAction SilentlyContinue) { yarn cache clean 2>&1 }
        else { Remove-Item -Recurse -Force $yarnCache -ErrorAction SilentlyContinue }
    }
}

# pnpm
$pnpmStore = "$env:LOCALAPPDATA\pnpm\store"
if (Test-Path $pnpmStore) {
    $s = (Get-ChildItem $pnpmStore -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 50MB) {
        $freed4a += $s
        Write-Host "pnpm store: $([math]::Round($s/1MB,1)) MB"
        if (Get-Command pnpm -ErrorAction SilentlyContinue) { pnpm store prune 2>&1 }
        else { Remove-Item -Recurse -Force $pnpmStore -ErrorAction SilentlyContinue }
    }
}

# NuGet
foreach ($p in @(
    "$env:LOCALAPPDATA\NuGet\Cache",
    "$env:LOCALAPPDATA\NuGet\plugins-cache",
    "$env:LOCALAPPDATA\NuGet\http-cache",
    "$env:LOCALAPPDATA\NuGet\v3-cache",
    "$env:LOCALAPPDATA\NuGet\scratch"
)) {
    if (Test-Path $p) {
        $s = (Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        $freed4a += $s
        Remove-Item -Recurse -Force $p -ErrorAction SilentlyContinue
    }
}
# NuGet global packages (report, don't auto-clean)
$nugetGlobal = "$env:USERPROFILE\.nuget\packages"
if (Test-Path $nugetGlobal) {
    $s = (Get-ChildItem $nugetGlobal -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 1GB) { Write-Host "NOTE: NuGet global packages: $([math]::Round($s/1GB,1)) GB (keeping — can run 'dotnet nuget locals all --clear' to purge)" }
}

# Maven — report only (redownload is very slow)
if (Test-Path "$env:USERPROFILE\.m2\repository") {
    $m2Size = (Get-ChildItem "$env:USERPROFILE\.m2\repository" -Recurse -ErrorAction SilentlyContinue |
               Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($m2Size -gt 1GB) { Write-Host "NOTE: .m2 Maven cache: $([math]::Round($m2Size/1GB,1)) GB (keeping — re-downloadable but very large)" }
}

# Gradle — clean jars and transforms only, NOT entire caches folder
if (Test-Path "$env:USERPROFILE\.gradle\caches") {
    foreach ($sub in @('jars-9','jars-8','jars-7','transforms-3','transforms-2','transforms-1','build-cache-1')) {
        $subPath = "$env:USERPROFILE\.gradle\caches\$sub"
        if (Test-Path $subPath) {
            $gs = (Get-ChildItem $subPath -Recurse -ErrorAction SilentlyContinue |
                   Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
            if ($gs -gt 100MB) {
                $freed4a += $gs
                Write-Host "Gradle $sub: $([math]::Round($gs/1MB,1)) MB"
                Remove-Item -Recurse -Force $subPath -ErrorAction SilentlyContinue
            }
        }
    }
}

# Bun
$bunCache = "$env:USERPROFILE\.bun\install\cache"
if (Test-Path $bunCache) {
    $s = (Get-ChildItem $bunCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 50MB) {
        $freed4a += $s
        Write-Host "Bun cache: $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force $bunCache -ErrorAction SilentlyContinue
    }
}

Write-Host "PHASE4A_FREED=$([math]::Round($freed4a/1MB,1))"
```

### 4b. Windows System Junk

```powershell
$freed = 0

# Temp directories
foreach ($tmpDir in @("$env:TEMP","C:\Windows\Temp")) {
    if (Test-Path $tmpDir) {
        $before = (Get-ChildItem $tmpDir -Recurse -ErrorAction SilentlyContinue |
                   Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        Get-ChildItem $tmpDir -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue 2>$null
        $after = (Get-ChildItem $tmpDir -Recurse -ErrorAction SilentlyContinue |
                  Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        $diff = $before - $after; $freed += $diff
        Write-Host "$tmpDir : $([math]::Round($diff/1MB,1)) MB"
    }
}

# Prefetch
$pfBefore = (Get-ChildItem C:\Windows\Prefetch\*.pf -ErrorAction SilentlyContinue |
             Measure-Object -Property Length -Sum).Sum
Get-ChildItem C:\Windows\Prefetch\*.pf -ErrorAction SilentlyContinue |
    Remove-Item -Force -ErrorAction SilentlyContinue
$freed += $pfBefore
Write-Host "Prefetch: $([math]::Round($pfBefore/1MB,1)) MB"

# Thumbnail cache
$thumbBefore = (Get-ChildItem "$env:LOCALAPPDATA\Microsoft\Windows\Explorer" -Filter "thumbcache_*" -ErrorAction SilentlyContinue |
                Measure-Object -Property Length -Sum).Sum
Get-ChildItem "$env:LOCALAPPDATA\Microsoft\Windows\Explorer" -Filter "thumbcache_*" -ErrorAction SilentlyContinue |
    Remove-Item -Force -ErrorAction SilentlyContinue
$freed += $thumbBefore

# Font cache (only temp font cache, not system fonts)
$fontDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
if (Test-Path $fontDir) {
    $fontBefore = (Get-ChildItem $fontDir -Recurse -ErrorAction SilentlyContinue |
                   Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Get-ChildItem $fontDir -Recurse -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $freed += $fontBefore
    Write-Host "Font cache: $([math]::Round($fontBefore/1MB,1)) MB"
}

# DNS cache (in-memory, zero disk impact, but good hygiene)
ipconfig /flushdns 2>$null

# Recycle Bin
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
Write-Host "Recycle Bin emptied"

# Windows Panther setup logs
if (Test-Path C:\Windows\Panther\monitor) {
    $pmSize = (Get-ChildItem C:\Windows\Panther\monitor -Recurse -ErrorAction SilentlyContinue |
               Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Get-ChildItem C:\Windows\Panther\monitor -Recurse -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $freed += $pmSize
    Write-Host "Panther monitor logs: $([math]::Round($pmSize/1MB,1)) MB"
}
Get-ChildItem C:\Windows\Panther -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -match '\.(log|etl|txt)$' } | ForEach-Object {
    $freed += $_.Length; Remove-Item $_.FullName -Force
}

# Delivery Optimization
$doDir = "C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization"
if (Test-Path $doDir) {
    $doSize = (Get-ChildItem $doDir -Recurse -ErrorAction SilentlyContinue |
               Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Get-ChildItem $doDir -Recurse -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $freed += $doSize
    Write-Host "Delivery Optimization: $([math]::Round($doSize/1MB,1)) MB"
}

# Windows Update download cache
$wuDir = "C:\Windows\SoftwareDistribution\Download"
if (Test-Path $wuDir) {
    $wuS = (Get-ChildItem $wuDir -Recurse -ErrorAction SilentlyContinue |
            Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Get-ChildItem $wuDir -Recurse -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $freed += $wuS
    Write-Host "Windows Update cache: $([math]::Round($wuS/1MB,1)) MB"
}

# Old CBS persist logs (keep current CBS.log)
Get-ChildItem C:\Windows\Logs\CBS -Filter "CbsPersist_*.log" -ErrorAction SilentlyContinue | ForEach-Object {
    $freed += $_.Length; Remove-Item $_ -Force
}

# DISM logs > 10MB
Get-ChildItem C:\Windows\Logs\DISM -Filter "dism*.log" -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 10MB } | ForEach-Object {
    $freed += $_.Length; Remove-Item $_ -Force
}

# Windows Error Reporting
$werDir = "C:\ProgramData\Microsoft\Windows\WER"
if (Test-Path $werDir) {
    $werS = (Get-ChildItem $werDir -Recurse -ErrorAction SilentlyContinue |
             Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($werS -gt 10MB) {
        Get-ChildItem $werDir -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        $freed += $werS
        Write-Host "WER: $([math]::Round($werS/1MB,1)) MB"
    }
}

# Live Kernel Reports
$lkDir = "C:\Windows\LiveKernelReports"
if (Test-Path $lkDir) {
    $lkSize = (Get-ChildItem $lkDir -Recurse -ErrorAction SilentlyContinue |
               Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($lkSize -gt 10MB) {
        Get-ChildItem $lkDir -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        $freed += $lkSize
        Write-Host "LiveKernelReports: $([math]::Round($lkSize/1MB,1)) MB"
    }
}

# Memory crash dumps in C:\Windows
foreach ($dumpFile in (Get-ChildItem C:\Windows\*.dmp -ErrorAction SilentlyContinue)) {
    $freed += $dumpFile.Length
    Write-Host "Crash dump removed: $($dumpFile.Name) ($([math]::Round($dumpFile.Length/1MB,1)) MB)"
    Remove-Item $dumpFile.FullName -Force
}
$memDump = "C:\Windows\Memory.dmp"
if (Test-Path $memDump) {
    $md = Get-Item $memDump
    $freed += $md.Length
    Write-Host "Memory.dmp removed: $([math]::Round($md.Length/1GB,2)) GB"
    Remove-Item $memDump -Force
}

# SCCM/ConfigMgr cache (enterprise environments)
$sccmCache = "C:\Windows\ccmcache"
if (Test-Path $sccmCache) {
    $sccmS = (Get-ChildItem $sccmCache -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($sccmS -gt 100MB) {
        Write-Host "SCCM cache: $([math]::Round($sccmS/1MB,1)) MB"
        Get-ChildItem $sccmCache -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
        $freed += $sccmS
    }
}

Write-Host "`nPhase 4b total: $([math]::Round($freed/1MB,1)) MB"
Write-Host "PHASE4B_FREED=$([math]::Round($freed/1MB,1))"
```

### 4c. DISM Component Cleanup (long timeout: 600s)

```powershell
Write-Host "DISM basic cleanup..."
dism /online /cleanup-image /startcomponentcleanup
Write-Host "DISM deep cleanup (/resetbase) — removes ALL superseded components."
Write-Host "WARNING: After /resetbase, you cannot uninstall Windows updates. This is generally fine."
dism /online /cleanup-image /startcomponentcleanup /resetbase
```

### 4d. System Restore / VSS Slim Down

```powershell
Write-Host "Resizing VSS to 1GB max..."
vssadmin resize shadowstorage /for=C: /on=C: /maxsize=1GB
vssadmin list shadowstorage
```

### 4e. Windows Store App Cache & .NET Native Image Cache

```powershell
$freed4e = 0

# Windows Store downloaded package cache
$storeCache = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe\LocalCache"
if (Test-Path $storeCache) {
    $s = (Get-ChildItem $storeCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 50MB) {
        Get-ChildItem $storeCache -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        $freed4e += $s
        Write-Host "Windows Store local cache: $([math]::Round($s/1MB,1)) MB"
    }
}

# wsappx / WinRT download cache
$wsDownload = "C:\Windows\SoftwareDistribution\DataStore"
if (Test-Path $wsDownload) {
    $s = (Get-ChildItem $wsDownload -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 100MB) {
        Write-Host "SoftwareDistribution DataStore: $([math]::Round($s/1MB,1)) MB (stopping wuauserv first)"
        Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
        Get-ChildItem "$wsDownload\Logs" -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Start-Service wuauserv -ErrorAction SilentlyContinue
    }
}

# .NET Native Image Cache (ngen) — stale
$ngenDir = "C:\Windows\assembly\NativeImages_v4.0.30319_64"
if (Test-Path $ngenDir) {
    $ngenSize = (Get-ChildItem $ngenDir -Recurse -ErrorAction SilentlyContinue |
                 Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Host ".NET native image cache (64-bit): $([math]::Round($ngenSize/1MB,1)) MB  (Windows manages this, skipping auto-clean)"
}

# Microsoft Edge WebView2 runtime cache
foreach ($wv2 in @(
    "$env:LOCALAPPDATA\Microsoft\EdgeWebView\Cache",
    "$env:LOCALAPPDATA\Microsoft\EdgeWebView\Code Cache"
)) {
    if (Test-Path $wv2) {
        $s = (Get-ChildItem $wv2 -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 20MB) {
            $freed4e += $s
            Write-Host "EdgeWebView2 cache: $([math]::Round($s/1MB,1)) MB"
            Remove-Item -Recurse -Force $wv2 -ErrorAction SilentlyContinue
        }
    }
}

# Microsoft Update Health Tools cache
$muhtCache = "C:\ProgramData\Microsoft\Windows\UpdateHealthTools"
if (Test-Path $muhtCache) {
    $s = (Get-ChildItem $muhtCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 50MB) {
        $freed4e += $s
        Write-Host "UpdateHealthTools: $([math]::Round($s/1MB,1)) MB"
        Get-ChildItem $muhtCache -File -Filter "*.log" -ErrorAction SilentlyContinue |
            Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

# Windows Temp from system accounts
foreach ($sysTemp in @(
    "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Temp",
    "C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Temp"
)) {
    if (Test-Path $sysTemp) {
        $s = (Get-ChildItem $sysTemp -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 10MB) {
            $freed4e += $s
            Write-Host "Service account temp ($sysTemp): $([math]::Round($s/1MB,1)) MB"
            Get-ChildItem $sysTemp -Recurse -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue 2>$null
        }
    }
}

Write-Host "PHASE4E_FREED=$([math]::Round($freed4e/1MB,1))"
```

### 4f. Optional: Disable Hibernation (ask user first)

**⚠️ Do NOT run this automatically.** Only proceed if user confirms they don't use Sleep/Hibernate.

```powershell
# Check hiberfil.sys size first
if (Test-Path C:\hiberfil.sys) {
    $h = Get-Item C:\hiberfil.sys -Force
    Write-Host "hiberfil.sys is $([math]::Round($h.Length/1GB,2)) GB."
    Write-Host "To disable hibernation and reclaim this space, run: powercfg /h off"
    Write-Host "To re-enable: powercfg /h on"
    Write-Host "Note: Disabling hibernation removes the Fast Startup feature on shutdown."
}
# Only run after user confirms:
# powercfg /h off
```

---

## Phase 5: Pattern-Based Application Cache Cleanup

### Safety Constraints

1. **Search only within AppData and dev-tool paths** — never Documents, Desktop, Downloads
2. **Match whole directory name** via `-contains`, never substring matching
3. **Skip** directories containing `.git`, `package.json`, `Cargo.toml`, `CMakeLists.txt`, or `README`
4. **Recurse deep enough** to catch nested caches — use `-Depth 8` from AppData roots

### 5a. Exact-Match Cache Pattern Cleaning

```powershell
$safePatterns = @(
    'Cache', 'cache', 'CACHE',
    'Temp', 'temp', 'TEMP',
    'Log', 'Logs', 'log', 'logs',
    'Code Cache',
    'GPUCache',
    'DawnCache',
    'ShaderCache',
    'GrShaderCache',
    'Crashpad',
    'CrashDumps',
    'Crash Reports',
    'thumbnails', 'Thumbnails',
    'preview', 'Preview',
    '__pycache__'
)

$searchRoots = @($env:LOCALAPPDATA, $env:APPDATA, "$env:USERPROFILE\AppData\LocalLow", "$env:USERPROFILE\.vscode")
$totalFreed = 0

foreach ($root in $searchRoots) {
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem $root -Recurse -Directory -ErrorAction SilentlyContinue -Depth 8 |
        Where-Object { $safePatterns -contains $_.Name } |
        ForEach-Object {
            $isProject = (Test-Path "$($_.FullName)\.git") -or
                         (Test-Path "$($_.FullName)\package.json") -or
                         (Test-Path "$($_.FullName)\Cargo.toml") -or
                         (Test-Path "$($_.FullName)\CMakeLists.txt") -or
                         (Test-Path "$($_.FullName)\README") -or
                         (Test-Path "$($_.FullName)\README.md")
            if ($isProject) { return }
            $item = Get-Item $_.FullName -ErrorAction SilentlyContinue
            if ($item.LinkType) { return }
            $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
                     Where-Object { !$_.PSIsContainer } |
                     Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            if ($size -gt 1MB) {
                Write-Host "Cache: $($_.FullName) ($([math]::Round($size/1MB,1)) MB)"
                $totalFreed += $size
                Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue
            }
        }
}
Write-Host "`nPhase 5a total: $([math]::Round($totalFreed/1MB,1)) MB"
Write-Host "PHASE5A_FREED=$([math]::Round($totalFreed/1MB,1))"
```

### 5b. GPU Shader Caches

```powershell
$gpuFreed = 0
foreach ($gpuPath in @(
    "$env:LOCALAPPDATA\NVIDIA\DXCache",
    "$env:LOCALAPPDATA\NVIDIA\GLCache",
    "$env:LOCALAPPDATA\AMD\DxCache",
    "$env:LOCALAPPDATA\AMD\GLCache",
    "$env:LOCALAPPDATA\AMD\VkCache",
    "$env:PROGRAMDATA\NVIDIA Corporation\NV_Cache",
    "$env:LOCALAPPDATA\Intel\ShaderCache",
    "$env:LOCALAPPDATA\D3DSCache"
)) {
    if (Test-Path $gpuPath) {
        $gs = (Get-ChildItem $gpuPath -Recurse -ErrorAction SilentlyContinue |
               Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($gs -gt 5MB) {
            Write-Host "GPU cache $gpuPath : $([math]::Round($gs/1MB,1)) MB"
            $gpuFreed += $gs
            Get-ChildItem $gpuPath -Recurse -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}
Write-Host "GPU shader caches: $([math]::Round($gpuFreed/1MB,1)) MB"
```

### 5c. Browser Cache Deep Clean (Chromium + Firefox)

```powershell
$browserFreed = 0

# Chromium-based browsers (auto-discover)
$browserDataDirs = @()
foreach ($vendor in @('Google','Microsoft','BraveSoftware','Opera Software','Vivaldi')) {
    $vendorPath = "$env:LOCALAPPDATA\$vendor"
    if (Test-Path $vendorPath) {
        Get-ChildItem $vendorPath -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $userData = "$($_.FullName)\User Data"
            if (Test-Path $userData) { $browserDataDirs += $userData }
        }
    }
}
# Also check for Arc browser
if (Test-Path "$env:LOCALAPPDATA\Packages\TheBrowserCompany.Arc_*") {
    Get-ChildItem "$env:LOCALAPPDATA\Packages\TheBrowserCompany.Arc_*\LocalState\StorableSidebar" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "Arc browser detected — cache cleaned via pattern matching in Phase 5a"
    }
}

foreach ($userData in $browserDataDirs) {
    Write-Host "Chromium browser: $userData"
    Get-ChildItem $userData -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        foreach ($cacheName in @('Cache','Code Cache','Service Worker','GPUCache',
                                  'DawnCache','ShaderCache','GrShaderCache','Crashpad','CacheStorage')) {
            $cp = "$($_.FullName)\$cacheName"
            if (Test-Path $cp) {
                $s = (Get-ChildItem $cp -Recurse -ErrorAction SilentlyContinue |
                      Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
                $browserFreed += $s
                Remove-Item -Recurse -Force $cp -ErrorAction SilentlyContinue
            }
        }
    }
}

# Firefox
$ffProfiles = "$env:APPDATA\Mozilla\Firefox\Profiles"
if (Test-Path $ffProfiles) {
    Get-ChildItem $ffProfiles -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        foreach ($ffCache in @('cache2','startupCache','OfflineCache','safebrowsing','thumbnails')) {
            $ffPath = "$($_.FullName)\$ffCache"
            if (Test-Path $ffPath) {
                $s = (Get-ChildItem $ffPath -Recurse -ErrorAction SilentlyContinue |
                      Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
                if ($s -gt 1MB) {
                    $browserFreed += $s
                    Write-Host "Firefox $ffCache : $([math]::Round($s/1MB,1)) MB"
                    Remove-Item -Recurse -Force $ffPath -ErrorAction SilentlyContinue
                }
            }
        }
        # Firefox storage (flag but don't auto-clean)
        $ffStorage = "$($_.FullName)\storage\default"
        if (Test-Path $ffStorage) {
            $s = (Get-ChildItem $ffStorage -Recurse -ErrorAction SilentlyContinue |
                  Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
            if ($s -gt 50MB) {
                Write-Host "Firefox storage/default: $([math]::Round($s/1MB,1)) MB (may contain extension data — skipping)"
            }
        }
    }
}

Write-Host "Browser caches: $([math]::Round($browserFreed/1MB,1)) MB"
Write-Host "PHASE5C_FREED=$([math]::Round($browserFreed/1MB,1))"
```

### 5d. JetBrains IDE Cache Cleanup

```powershell
$jbLocal = "$env:LOCALAPPDATA\JetBrains"
if (Test-Path $jbLocal) {
    Get-ChildItem $jbLocal -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $cacheDir = "$($_.FullName)\caches"
        if (Test-Path $cacheDir) {
            $s = (Get-ChildItem $cacheDir -Recurse -ErrorAction SilentlyContinue |
                  Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
            Write-Host "JetBrains $($_.Name) caches: $([math]::Round($s/1MB,1)) MB"
            Remove-Item -Recurse -Force $cacheDir -ErrorAction SilentlyContinue
        }
        # Clean only old version directories (not the most recent one)
        $versionDirs = Get-ChildItem $_.FullName -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^\d+\.\d+' } |
            Sort-Object Name -Descending
        if ($versionDirs.Count -gt 1) {
            $versionDirs | Select-Object -Skip 1 | ForEach-Object {
                $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
                      Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
                Write-Host "JetBrains old version $($_.Name): $([math]::Round($s/1MB,1)) MB"
                Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue
            }
        }
    }
}
```

### 5e. VS Code / VS Code Insiders Cache

```powershell
foreach ($vsc in @('Code','Code - Insiders','Code - Exploration')) {
    $vscRoot = "$env:APPDATA\$vsc"
    if (-not (Test-Path $vscRoot)) { continue }
    foreach ($sub in @('Cache','CachedData','Code Cache','GPUCache','Crashpad',
                        'DawnCache','ShaderCache','GrShaderCache')) {
        $cp = "$vscRoot\$sub"
        if (Test-Path $cp) {
            $s = (Get-ChildItem $cp -Recurse -ErrorAction SilentlyContinue |
                  Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
            Write-Host "$vsc $sub: $([math]::Round($s/1MB,1)) MB"
            Remove-Item -Recurse -Force $cp -ErrorAction SilentlyContinue
        }
    }
    $wsStorage = "$vscRoot\User\workspaceStorage"
    if (Test-Path $wsStorage) {
        $wsSize = (Get-ChildItem $wsStorage -Recurse -ErrorAction SilentlyContinue |
                   Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($wsSize -gt 200MB) {
            Write-Host "$vsc workspaceStorage: $([math]::Round($wsSize/1MB,1)) MB"
            Remove-Item -Recurse -Force $wsStorage -ErrorAction SilentlyContinue
        }
    }
}
```

### 5f. Microsoft Teams Cache (Classic + New)

```powershell
$teamsFreed = 0

# Teams Classic
$teamsClassic = "$env:APPDATA\Microsoft\Teams"
if (Test-Path $teamsClassic) {
    foreach ($sub in @('Cache','Code Cache','GPUCache','blob_storage','databases',
                        'Local Storage','tmp','logs','crash reports')) {
        $p = "$teamsClassic\$sub"
        if (Test-Path $p) {
            $s = (Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue |
                  Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
            if ($s -gt 5MB) {
                $teamsFreed += $s
                Write-Host "Teams Classic $sub: $([math]::Round($s/1MB,1)) MB"
                Remove-Item -Recurse -Force $p -ErrorAction SilentlyContinue
            }
        }
    }
}

# Teams (new) — MSIX/Store version
$teamsNew = "$env:LOCALAPPDATA\Packages\MSTeams_8wekyb3d8bbwe\LocalCache"
if (Test-Path $teamsNew) {
    $s = (Get-ChildItem $teamsNew -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 20MB) {
        $teamsFreed += $s
        Write-Host "Teams (new) LocalCache: $([math]::Round($s/1MB,1)) MB"
        Get-ChildItem $teamsNew -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Teams caches: $([math]::Round($teamsFreed/1MB,1)) MB"
Write-Host "PHASE5F_FREED=$([math]::Round($teamsFreed/1MB,1))"
```

### 5g. Adobe, Zoom & Video Conferencing Caches

```powershell
$appFreed = 0

# Adobe products cache
foreach ($adobePath in @(
    "$env:LOCALAPPDATA\Adobe\Color\Themes",
    "$env:APPDATA\Adobe\Common\Media Cache Files",
    "$env:APPDATA\Adobe\Common\Media Cache",
    "$env:LOCALAPPDATA\Adobe\Photoshop",
    "$env:LOCALAPPDATA\Adobe\After Effects",
    "$env:LOCALAPPDATA\Adobe\Premiere Pro"
)) {
    if (Test-Path $adobePath) {
        $s = (Get-ChildItem $adobePath -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 50MB) {
            Write-Host "Adobe $(Split-Path $adobePath -Leaf): $([math]::Round($s/1MB,1)) MB"
            # Only clean cache subdirectories, not the entire folder
            Get-ChildItem $adobePath -Directory -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -in @('Cache','cache','Temp','temp','Media Cache Files','Media Cache') } |
                ForEach-Object {
                    $cs = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
                           Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
                    $appFreed += $cs
                    Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue
                }
        }
    }
}

# Zoom
foreach ($zoomPath in @(
    "$env:APPDATA\Zoom\data",
    "$env:APPDATA\Zoom\logs",
    "$env:LOCALAPPDATA\Zoom\Logs"
)) {
    if (Test-Path $zoomPath) {
        $s = (Get-ChildItem $zoomPath -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 20MB) {
            $appFreed += $s
            Write-Host "Zoom $(Split-Path $zoomPath -Leaf): $([math]::Round($s/1MB,1)) MB"
            Get-ChildItem $zoomPath -File -Filter "*.log" -ErrorAction SilentlyContinue |
                Remove-Item -Force -ErrorAction SilentlyContinue
            Get-ChildItem $zoomPath -File -Filter "*.tmp" -ErrorAction SilentlyContinue |
                Remove-Item -Force -ErrorAction SilentlyContinue
        }
    }
}

# Webex
$webexCache = "$env:LOCALAPPDATA\Cisco\Unified Communications\Jabber\CSF\Cache"
if (Test-Path $webexCache) {
    $s = (Get-ChildItem $webexCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 20MB) {
        $appFreed += $s
        Write-Host "Webex cache: $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force $webexCache -ErrorAction SilentlyContinue
    }
}

Write-Host "App caches (Adobe/Zoom/video): $([math]::Round($appFreed/1MB,1)) MB"
Write-Host "PHASE5G_FREED=$([math]::Round($appFreed/1MB,1))"
```

### 5h. Corrupted Database Files (Universal)

```powershell
# SQLite files with I/O error markers
Get-ChildItem $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue -Depth 6 |
    Where-Object { $_.Name -match 'SQLITE_IOERR|SQLITE_CORRUPT|_IOERR\d{10,}' } |
    ForEach-Object {
        Write-Host "Corrupted DB: $($_.FullName) ($([math]::Round($_.Length/1MB,1)) MB)"
        Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
    }

# Orphaned WAL/SHM journal files (parent DB no longer exists)
Get-ChildItem $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue -Depth 6 |
    Where-Object {
        $ext = $_.Extension
        ($ext -eq '.db-wal' -or $ext -eq '.db-shm' -or $ext -eq '.db-journal') -and
        (-not (Test-Path ($_.FullName -replace '-(wal|shm|journal)$', '')))
    } | ForEach-Object {
        Write-Host "Orphaned journal: $($_.FullName) ($([math]::Round($_.Length/1MB,1)) MB)"
        Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
    }
```

### 5i. Desktop Orphaned Junk Files

```powershell
$desktop = "$env:USERPROFILE\Desktop"
$junkPatterns = @('update.mar','update.mar.*','cached-microdescs','cached-certs',
                   '*.tmp','*.temp','~$*.docx','~$*.xlsx','~$*.pptx')
foreach ($pattern in $junkPatterns) {
    Get-ChildItem $desktop -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.Length -gt 10MB -or $_.Extension -match '\.(tmp|temp|mar)$') {
            Write-Host "Desktop junk: $($_.Name) ($([math]::Round($_.Length/1MB,1)) MB)"
            Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
        }
    }
}
```

### 5j. C:\ Root Orphan Cleanup (Debug Logs)

```powershell
foreach ($rootTmp in @("C:\tmp","C:\temp")) {
    if (Test-Path $rootTmp) {
        Get-ChildItem $rootTmp -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            $ext = $_.Extension.ToLower()
            if ($ext -in @('.log','.tmp','.temp','.dump','.etl','.txt') -and $_.Length -gt 10MB) {
                $firstLine = Get-Content $_.FullName -TotalCount 1 -ErrorAction SilentlyContinue
                if ($firstLine -match 'TLS secrets|# TLS|SSLKEYLOGFILE|DEBUG|TRACE|PresharedKey|Generated by') {
                    Write-Host "Debug log: $($_.FullName) ($([math]::Round($_.Length/1MB,1)) MB)"
                    Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
                }
            }
        }
    }
}
```

### 5k. SDK & Tool Caches in User Root

```powershell
# JavaFX SDK cache
$jfxCache = "$env:USERPROFILE\.openjfx\cache"
if (Test-Path $jfxCache) {
    $s = (Get-ChildItem $jfxCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Host ".openjfx cache: $([math]::Round($s/1MB,1)) MB"
    Remove-Item -Recurse -Force $jfxCache -ErrorAction SilentlyContinue
}

# XDG .cache directory (Git Bash, MSYS2, Cygwin)
$xdgCache = "$env:USERPROFILE\.cache"
if (Test-Path $xdgCache) {
    $s = (Get-ChildItem $xdgCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 5MB) {
        Write-Host ".cache (XDG): $([math]::Round($s/1MB,1)) MB"
        Get-ChildItem $xdgCache -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Go module cache
$goModCache = "$env:USERPROFILE\go\pkg\mod"
if (-not (Test-Path $goModCache)) { $goModCache = "$env:USERPROFILE\.go\pkg\mod" }
if (Test-Path $goModCache) {
    $s = (Get-ChildItem $goModCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Host "Go module cache: $([math]::Round($s/1MB,1)) MB"
    if (Get-Command go -ErrorAction SilentlyContinue) { go clean -modcache 2>&1 }
    else { Remove-Item -Recurse -Force $goModCache -ErrorAction SilentlyContinue }
}

# Python shiv
$shivCache = "$env:USERPROFILE\.shiv"
if (Test-Path $shivCache) {
    $s = (Get-ChildItem $shivCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Host ".shiv cache: $([math]::Round($s/1MB,1)) MB"
    Remove-Item -Recurse -Force $shivCache -ErrorAction SilentlyContinue
}

# Cargo registry cache (Rust) — only cache dir, not src
$cargoRegCache = "$env:USERPROFILE\.cargo\registry\cache"
if (Test-Path $cargoRegCache) {
    $s = (Get-ChildItem $cargoRegCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Host "Cargo registry cache: $([math]::Round($s/1MB,1)) MB"
    Remove-Item -Recurse -Force $cargoRegCache -ErrorAction SilentlyContinue
}

# Electron download cache
$electronCache = "$env:USERPROFILE\.electron"
if (Test-Path $electronCache) {
    $s = (Get-ChildItem $electronCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 20MB) {
        Write-Host "Electron download cache: $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force $electronCache -ErrorAction SilentlyContinue
    }
}
```

### 5l. Squirrel Installer & Old Electron App Versions (Safe Version)

Squirrel-based apps (Teams, Slack, Discord, WhatsApp Desktop, etc.) leave `app-x.x.x` versioned directories after auto-updates. Only the **highest** version directory is kept.

```powershell
foreach ($electronApp in @('Discord','Slack','Microsoft Teams','Spotify','GitHubDesktop','WhatsApp')) {
    $appDir = "$env:LOCALAPPDATA\$electronApp"
    if (-not (Test-Path $appDir)) { continue }
    
    # Find all version directories
    $versionDirs = Get-ChildItem $appDir -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^app-\d+\.\d+\.\d+' -and $_.Name -notmatch '-full$' } |
        Sort-Object { [version]($_.Name -replace '^app-','') } -Descending

    if ($versionDirs.Count -le 1) { continue }

    # Keep only the newest version; delete the rest
    $versionDirs | Select-Object -Skip 1 | ForEach-Object {
        $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 30MB) {
            Write-Host "Electron old version $electronApp\$($_.Name): $([math]::Round($s/1MB,1)) MB"
            Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue
        }
    }
}

# Clean -full suffix stale dirs (download staging, always safe)
Get-ChildItem "$env:LOCALAPPDATA" -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '-full$' } | ForEach-Object {
        $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue |
              Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 50MB) {
            Write-Host "Squirrel stale staging: $($_.Name) ($([math]::Round($s/1MB,1)) MB)"
            Remove-Item -Recurse -Force $_.FullName -ErrorAction SilentlyContinue
        }
    }
```

### 5m. INetCache & Legacy Browser Data

```powershell
# INetCache (IE / legacy Edge)
$inetCache = "$env:LOCALAPPDATA\Microsoft\Windows\INetCache"
if (Test-Path $inetCache) {
    $s = (Get-ChildItem $inetCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 5MB) {
        Write-Host "INetCache: $([math]::Round($s/1MB,1)) MB"
        Get-ChildItem $inetCache -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}
foreach ($ieDir in @(
    "$env:LOCALAPPDATA\Microsoft\Windows\INetCookies",
    "$env:LOCALAPPDATA\Microsoft\Windows\History"
)) {
    if (Test-Path $ieDir) {
        Get-ChildItem $ieDir -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue 2>$null
    }
}

# Flash cache (deprecated but may still exist)
$flashCache = "$env:APPDATA\Macromedia\Flash Player"
if (Test-Path $flashCache) {
    $s = (Get-ChildItem $flashCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 5MB) {
        Write-Host "Flash Player cache: $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force $flashCache -ErrorAction SilentlyContinue
    }
}
```

### 5n. Game Platform Caches (Steam / Epic / Xbox)

```powershell
$gameFreed = 0

# Steam shader and download cache (NOT game files)
$steamLocal = "$env:LOCALAPPDATA\Steam"
if (Test-Path "$steamLocal\htmlcache") {
    $s = (Get-ChildItem "$steamLocal\htmlcache" -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 20MB) {
        $gameFreed += $s
        Write-Host "Steam htmlcache: $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force "$steamLocal\htmlcache" -ErrorAction SilentlyContinue
    }
}

# Epic Games Launcher cache
$epicCache = "$env:LOCALAPPDATA\EpicGamesLauncher\Saved\webcache"
if (Test-Path $epicCache) {
    $s = (Get-ChildItem $epicCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 20MB) {
        $gameFreed += $s
        Write-Host "Epic Launcher webcache: $([math]::Round($s/1MB,1)) MB"
        Remove-Item -Recurse -Force $epicCache -ErrorAction SilentlyContinue
    }
}

# Xbox / GamePass (UWP) cache
$xboxCache = "$env:LOCALAPPDATA\Packages\Microsoft.GamingApp_8wekyb3d8bbwe\LocalCache"
if (Test-Path $xboxCache) {
    $s = (Get-ChildItem $xboxCache -Recurse -ErrorAction SilentlyContinue |
          Where-Object { !$_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 20MB) {
        $gameFreed += $s
        Write-Host "Xbox app cache: $([math]::Round($s/1MB,1)) MB"
        Get-ChildItem $xboxCache -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Game platform caches: $([math]::Round($gameFreed/1MB,1)) MB"
Write-Host "PHASE5N_FREED=$([math]::Round($gameFreed/1MB,1))"
```

---

## Phase 6: User Decision Items

After Phases 4-5, remaining large items are **user data, not cache**. Categorize and present:

### Auto-Classification Rules

For each remaining folder > 200MB from Phase 3:

| Path Pattern | Category | Recommendation |
|-------------|----------|----------------|
| Contains `\Msg\`, `\messages\`, `\chat\` | **Chat data** | User's chat history — ask |
| Contains `BackupFiles`, `\Backup\`, `_backup` | **Old backups** | Redundant — suggest deletion |
| `.rustup\toolchains` | **SDK toolchains** | Reinstallable — suggest keeping only active one |
| `.cargo`, `.gradle`, `.m2`, `.nuget` | **Build cache** | Re-downloadable — suggest cleaning |
| `\Projects\`, `\Workspace\`, `\repos\` | **Dev projects** | NEVER suggest deletion |
| `\Recordings\`, `\Meetings\` | **Recordings** | May be important — ask |
| `VirtualBox`, `VMware`, `Docker`, `WSL` | **VM/Container** | Large — ask |
| `BurpSuite`, `Wireshark`, `fiddler`, `ZAP` | **Security tools** | User projects — NEVER delete |
| `.android\avd` | **Android emulators** | Re-downloadable but large — ask |
| `.apple`, `MobileSync`, `Apple Computer` | **Apple backups** | May be important — ask |
| `Squirrel`, `app-`, `-full` | **Old installers** | Stale versions — suggest deletion |
| `node_modules` (not inside a project) | **Abandoned deps** | Can be regenerated — suggest deletion |
| `go/pkg`, `.go/pkg` | **Go module cache** | Re-downloadable — suggest cleaning |
| `.cache`, `.shiv`, `.openjfx` | **SDK/tool cache** | Safe to delete |
| `IntelGraphicsProfiles`, `Intel` in LocalLow | **GPU driver cache** | Safe to delete |
| `hiberfil.sys` (if still present) | **Hibernation file** | Ask user if they use Hibernate/Sleep |
| Downloads folder items > 500MB | **Large downloads** | Show top 10, ask user |
| Unknown (can't classify) | **Unknown** | Err on caution — NEVER delete |

### Presentation Format

```
### Items for Your Decision (X.XX GB total)

| # | Path | Size | Category | Risk | Note |
|---|------|------|----------|------|------|
| 1 | <path> | X.XX GB | <category> | Low | <suggestion> |
```

Ask: "Enter numbers to clean (e.g., 1,3,5), or 'all' / 'none'."

**Special prompts to ask:**
- If hiberfil.sys > 2 GB: "Do you use Sleep or Hibernate? If not, I can disable hibernation to reclaim [X] GB."
- If Downloads > 2 GB: "Your Downloads folder contains [X] GB including [top files]. Would you like to review them?"
- If Docker detected: "Docker is using [X] GB. Run `docker system prune -f` to remove unused images/containers?"

---

## Phase 7: Final Report

```powershell
Write-Host "========================================"
Write-Host "       FINAL DISK CLEANUP REPORT"
Write-Host "========================================"
Get-PSDrive C | ForEach-Object {
    $total = [math]::Round(($_.Used + $_.Free)/1GB, 2)
    $used  = [math]::Round($_.Used/1GB, 2)
    $free  = [math]::Round($_.Free/1GB, 2)
    $pct   = [math]::Round($_.Used/($_.Used+$_.Free)*100, 1)
    Write-Host "Total: $total GB | Used: $used GB ($pct%) | Free: $free GB"
}
Write-Host "========================================"
```

After the PowerShell output, manually compile a summary table from the `PHASE*_FREED` markers:

```
Cleanup Summary:
  4a  Package managers:         X.XX GB
  4b  Windows junk:             X.XX GB
  4c  DISM:                     completed
  4d  VSS resize:               completed
  4e  Windows Store / .NET:     X.XX GB
  5a  Pattern caches:           X.XX GB
  5b  GPU shader caches:        X.XX GB
  5c  Browser caches:           X.XX GB
  5d  JetBrains caches:         X.XX GB
  5e  VS Code caches:           X.XX GB
  5f  Teams caches:             X.XX GB
  5g  Adobe / Zoom caches:      X.XX GB
  5h  Corrupted DB files:       X.XX GB
  5i  Desktop junk:             X.XX GB
  5j  Root orphans:             X.XX GB
  5k  SDK / tool caches:        X.XX GB
  5l  Electron old versions:    X.XX GB
  5m  Legacy browser data:      X.XX GB
  5n  Game platform caches:     X.XX GB
  6   User-approved items:      X.XX GB
  ─────────────────────────────────────
  TOTAL FREED:                  X.XX GB
```

Also list remaining large directories with explanations for why they were kept.

---

## Execution Rules

1. **Scan always before cleaning** — Phase 1-3 complete before Phase 4
2. **Parallelize independent scans** — Phase 1a/1b/1c together; Phase 2a/2b/2c together; Phase 3a/3b/3c/3d/3e together
3. **Phase 4 sequential**: 4a → 4b → 4c → 4d → 4e (dependencies between steps)
4. **Phase 5 parallel**: 5a and 5b can run together; 5c-5n can be batched
5. **Use `-ErrorAction SilentlyContinue`** everywhere — locked files are skipped
6. **DISM timeout: 600s**; everything else: default 120s
7. **NEVER DELETE**: System32, SysWOW64, WinSxS (manual), DriverStore, Program Files, Program Files (x86)
8. **NEVER DELETE**: `.exe`, `.dll`, `.sys`, `.msi`, `.msix` files
9. **NEVER DELETE**: OneDrive synced files, user Documents/Pictures/Music/Videos
10. **NEVER disable** hiberfil.sys or pagefile.sys without explicit user confirmation
11. **Use `!$_.PSIsContainer`** (PowerShell 5.1 compatible)
12. **Use `-contains`** for exact name matching; never `-match` with partial patterns
13. **If any command produces unexpected errors, stop and investigate** — do not proceed with cleanup in that area
14. **After Phase 4c (DISM), continue even if DISM produces warnings** — DISM often reports non-critical warnings
15. **Electron version deletion** — always sort versions and keep the highest; never delete all versions
16. **Record freed numbers** as you go — the final Phase 7 report needs per-phase contributions
