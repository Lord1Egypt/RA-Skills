# scan_all.ps1 — Windows on-demand detection of installed statistical software
# Output JSON: {"R":{"installed":true,"path":"...","version":"..."},...}
# Detection uses registry uninstall entries + a small set of well-known install
# paths + command resolution.
#
# SCOPE / PRIVACY (SDI-1/SDI-4):
#   * This script detects installed statistical software and reports install
#     paths + versions (privacy-sensitive local inventory).
#   * REVEALING paths/versions requires EXPLICIT opt-in for ANY detection —
#     broad host-wide OR a narrow single -Target probe:
#       STATSOFT_AUTO_WRITE=1 (non-interactive) or STATSOFT_CONFIRM=1 + a TTY y/N.
#   * WITHOUT opt-in the script still runs but emits ONLY a boolean
#     installed/not-installed result (paths and versions are hidden).
#   * Detection resolves locations from registry / well-known paths / command
#     lookup and does NOT execute third-party binaries to obtain versions.

param(
    [string]$Target = ""
)

$ErrorActionPreference = "SilentlyContinue"

$script:isZH = [System.Globalization.CultureInfo]::CurrentUICulture.Name.StartsWith("zh")
function Write-Lang {
    param([string]$CN, [string]$EN)
    if ($script:isZH) { Write-Host $CN } else { Write-Host $EN }
}

# When no target is given we run the broad, host-wide inventory.
$doAll = [string]::IsNullOrWhiteSpace($Target)

# Include a tool's detection only if we're in broad mode, or it matches -Target.
function Want([string]$name) {
    return ($doAll -or ($Target -ieq $name))
}

# ─────────── CONSENT GATE (reveal install paths/versions) ───────────
# ANY detection (broad host-wide OR narrow -Target) may reveal install paths +
# versions, which is privacy-sensitive inventory. Revealing that detail requires
# explicit opt-in; without it we still run but emit only a boolean result (SDI-1).
$reveal = $false
$autoWrite = $env:STATSOFT_AUTO_WRITE -eq '1'
$confirm = $env:STATSOFT_CONFIRM -eq '1'
if ($autoWrite) {
    $reveal = $true
} elseif ($confirm -and -not [Console]::IsInputRedirected) {
    Write-Lang "本操作将检测本机上已安装的统计软件（包含安装路径与版本）。" "This will detect installed statistical software (paths + versions) on this host."
    $prompt = if ($script:isZH) { "是否继续并揭示安装路径/版本？(y/N)" } else { "Proceed and reveal install paths/versions? (y/N)" }
    $ans = Read-Host $prompt
    if ($ans -match '^[yY]') { $reveal = $true }
} else {
    Write-Lang "检测仍会执行，但安装路径/版本将被隐藏（设置 STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1 可揭示）。" "Detection runs, but install paths/versions are hidden (set STATSOFT_AUTO_WRITE=1 / STATSOFT_CONFIRM=1 to reveal)."
}

$results = @{}

function Write-JsonOutput($obj) {
    $obj | ConvertTo-Json -Depth 3 -Compress
}

function Add-RResult($name, $installed, $path, $version) {
    if ($installed) {
        if ($reveal) {
            $results[$name] = @{
                installed = $true
                path = $path
                version = $version
                platform = "windows"
            }
        } else {
            # Without opt-in, reveal nothing sensitive — boolean only (SDI-1).
            $results[$name] = @{
                installed = $true
                path = $null
                version = $null
                platform = "windows"
            }
        }
    } else {
        if (-not $results.ContainsKey($name)) {
            $results[$name] = @{
                installed = $false
                path = $null
                version = $null
                platform = "windows"
            }
        }
    }
}

function Get-PathOrEmpty($paths) {
    foreach ($p in $paths) {
        if (Test-Path $p) { return $p }
    }
    return $null
}

function Get-RegistryValue($path, $name) {
    try {
        $item = Get-ItemProperty -Path $path -ErrorAction SilentlyContinue
        if ($item) { return $item.$name }
    } catch {}
    return $null
}

function Get-NsisSoftware($pattern) {
    # Search HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
    $regPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    $keys = Get-ChildItem $regPath -ErrorAction SilentlyContinue
    foreach ($key in $keys) {
        $props = Get-ItemProperty $key.PSPath -ErrorAction SilentlyContinue
        $dispName = $props.DisplayName
        if ($dispName -match $pattern) {
            $installLocation = $props.InstallLocation
            $version = $props.DisplayVersion
            return @{ DisplayName = $dispName; Path = $installLocation; Version = $version }
        }
    }
    return $null
}

function Get-NsisSoftwareWow64($pattern) {
    # Search the 32-bit registry (WoW6432Node)
    $regPath = "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    $keys = Get-ChildItem $regPath -ErrorAction SilentlyContinue
    foreach ($key in $keys) {
        $props = Get-ItemProperty $key.PSPath -ErrorAction SilentlyContinue
        $dispName = $props.DisplayName
        if ($dispName -match $pattern) {
            $installLocation = $props.InstallLocation
            $version = $props.DisplayVersion
            return @{ DisplayName = $dispName; Path = $installLocation; Version = $version }
        }
    }
    return $null
}

function Detect-ByPaths($pattern, $paths) {
    foreach ($basePath in $paths) {
        if (Test-Path $basePath) {
            $parent = Split-Path (Split-Path $basePath -Parent) -Parent
            # Try to extract the version number
            $leaf = Split-Path $basePath -Leaf
            if ($leaf -match '(\d+\.?\d*)') {
                return @{ Path = $parent; Version = $matches[1]; DisplayName = "$pattern ($leaf)" }
            }
            return @{ Path = $parent; Version = "unknown"; DisplayName = $pattern }
        }
    }
    return $null
}

function Detect-ByCommand($command) {
    $cmd = Get-Command $command -ErrorAction SilentlyContinue
    if ($cmd) {
        return @{ Path = $cmd.Source; Version = "unknown"; DisplayName = $command }
    }
    return $null
}

# ────────────── SOFTWARE DETECTION ──────────────
# Each block runs only when Want <name> is true (broad mode, or matching -Target).

# R
if (Want "R") {
    $regR = Get-NsisSoftware "R for Windows"
    $regR2 = Get-NsisSoftwareWow64 "R for Windows"
    $foundR = $null
    foreach ($pr in @("C:\Program Files\R\R-4.5.1\bin\R.exe", "C:\Program Files\R\R-4.4.2\bin\R.exe", "C:\Program Files\R\R-4.3.1\bin\R.exe", "C:\Program Files\R\R-4.2.1\bin\R.exe")) {
        if (Test-Path $pr) {
            $foundR = @{ Path = Split-Path (Split-Path $pr -Parent) -Parent; Version = (Split-Path $pr -Leaf).Replace("R-",""); DisplayName = "R" }
            break
        }
    }
    if (-not $foundR -and $regR) {
        $foundR = @{ Path = $regR.Path; Version = $regR.Version; DisplayName = $regR.DisplayName }
    }
    if (-not $foundR -and $regR2) {
        $foundR = @{ Path = $regR2.Path; Version = $regR2.Version; DisplayName = $regR2.DisplayName }
    }
    Add-RResult "R" $foundR $foundR.Path $foundR.Version
}

# Python
if (Want "Python") {
    $cmdPy = Detect-ByCommand "python"
    $cmdPy2 = Detect-ByCommand "python3"
    if ($cmdPy) { Add-RResult "Python" $true $cmdPy.Path "unknown" }
    elseif ($cmdPy2) { Add-RResult "Python" $true $cmdPy2.Path "unknown" }
}

# SPSS Statistics — probe registry, then a few fixed system drives (C:/D:) only.
# This does NOT enumerate every mounted volume; it is a bounded set of known paths.
if (Want "SPSS Statistics") {
    $regSpss = Get-NsisSoftware "IBM SPSS Statistics"
    $regSpss2 = Get-NsisSoftwareWow64 "IBM SPSS Statistics"
    $foundSpss = $regSpss
    if (-not $foundSpss) { $foundSpss = $regSpss2 }
    if (-not $foundSpss) {
        $drives = @("C", "D")
        $patterns = @(
            "{0}:\Program Files\IBM\SPSS\Statistics",
            "{0}:\Program Files (x86)\IBM\SPSS\Statistics",
            "{0}:\SPSS\Statistics",
            "{0}:\IBM\SPSS\Statistics"
        )
        foreach ($d in $drives) {
            if ($foundSpss) { break }
            foreach ($pat in $patterns) {
                if ($foundSpss) { break }
                $base = $pat -f $d
                if (Test-Path $base) {
                    $subdirs = Get-ChildItem $base -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending
                    if ($subdirs.Count -gt 0) {
                        $foundSpss = @{ Path = (Join-Path $base $subdirs[0].Name); Version = $subdirs[0].Name; DisplayName = "IBM SPSS Statistics $($subdirs[0].Name)" }
                        break
                    }
                }
            }
        }
    }
    Add-RResult "SPSS Statistics" $foundSpss $foundSpss.Path $foundSpss.Version
}

# SPSS Modeler
if (Want "SPSS Modeler") {
    $regModeler = Get-NsisSoftware "IBM SPSS Modeler"
    $regModeler2 = Get-NsisSoftwareWow64 "IBM SPSS Modeler"
    $foundModeler = $regModeler
    if (-not $foundModeler) { $foundModeler = $regModeler2 }
    Add-RResult "SPSS Modeler" $foundModeler $foundModeler.Path $foundModeler.Version
}

# Stata
if (Want "Stata") {
    $pathsStata = @()
    $stataVersions = @("Stata19", "Stata18", "Stata17", "Stata16", "Stata15", "Stata14", "Stata13", "Stata12", "Stata11")
    foreach ($sv in $stataVersions) {
        $pathsStata += "C:\Program Files\$sv\StataMP-64.exe"
        $pathsStata += "C:\Program Files (x86)\$sv\StataMP.exe"
        $pathsStata += "C:\Program Files\$sv\StataSE-64.exe"
        $pathsStata += "C:\Program Files (x86)\$sv\StataSE.exe"
    }
    $foundStata = Detect-ByPaths "Stata" $pathsStata
    $regStata = Get-NsisSoftware "Stata"
    $regStata2 = Get-NsisSoftwareWow64 "Stata"
    if (-not $foundStata -and $regStata) {
        $foundStata = @{ Path = $regStata.Path; Version = $regStata.Version; DisplayName = $regStata.DisplayName }
    }
    if (-not $foundStata -and $regStata2) {
        $foundStata = @{ Path = $regStata2.Path; Version = $regStata2.Version; DisplayName = $regStata2.DisplayName }
    }
    Add-RResult "Stata" $foundStata $foundStata.Path $foundStata.Version
}

# SAS (SAS Foundation)
if (Want "SAS") {
    $regSas = Get-NsisSoftware "SAS Foundation"
    $regSas2 = Get-NsisSoftwareWow64 "SAS Foundation"
    $foundSas = $regSas
    if (-not $foundSas) { $foundSas = $regSas2 }
    Add-RResult "SAS" $foundSas $foundSas.Path $foundSas.Version
}

# Matlab
if (Want "Matlab") {
    $regMatlab = Get-NsisSoftware "MATLAB"
    $regMatlab2 = Get-NsisSoftwareWow64 "MATLAB"
    $foundMatlab = $regMatlab
    if (-not $foundMatlab) { $foundMatlab = $regMatlab2 }
    if (-not $foundMatlab) {
        $mwPaths = @("C:\Program Files\MATLAB\R2025a", "C:\Program Files\MATLAB\R2024b", "C:\Program Files\MATLAB\R2024a")
        foreach ($mp in $mwPaths) {
            if (Test-Path $mp) {
                $foundMatlab = @{ Path = $mp; Version = ($mp -replace '.*R','R'); DisplayName = "MATLAB" }
                break
            }
        }
    }
    Add-RResult "Matlab" $foundMatlab $foundMatlab.Path $foundMatlab.Version
}

# Mathematica
if (Want "Mathematica") {
    $regMath = Get-NsisSoftware "Mathematica"
    $regMath2 = Get-NsisSoftwareWow64 "Mathematica"
    $foundMath = $regMath
    if (-not $foundMath) { $foundMath = $regMath2 }
    if (-not $foundMath) {
        $mathPaths = @("C:\Program Files\Wolfram Research\Mathematica\14.0", "C:\Program Files\Wolfram Research\Mathematica\13.0", "C:\Program Files\Wolfram Research\Mathematica\12.0", "C:\Program Files (x86)\Wolfram Research\Mathematica")
        foreach ($mp in $mathPaths) { if (Test-Path $mp) { $foundMath = @{ Path = $mp; Version = (Split-Path $mp -Leaf); DisplayName = "Mathematica" } ; break } }
    }
    Add-RResult "Mathematica" $foundMath $foundMath.Path $foundMath.Version
}

# JMP
if (Want "JMP") {
    $regJmp = Get-NsisSoftware "JMP"
    $regJmp2 = Get-NsisSoftwareWow64 "JMP"
    $foundJmp = $regJmp
    if (-not $foundJmp) { $foundJmp = $regJmp2 }
    Add-RResult "JMP" $foundJmp $foundJmp.Path $foundJmp.Version
}

# Rattle
if (Want "Rattle") {
    $cmdRattle = Detect-ByCommand "rattle"
    if ($cmdRattle) { Add-RResult "Rattle" $true $cmdRattle.Path }
}

# Weka
if (Want "Weka") {
    $pathsWeka = @("C:\Program Files\Weka-3-8*", "C:\Program Files (x86)\Weka")
    $foundWeka = $null
    foreach ($wp in $pathsWeka) { if (Test-Path $wp) { $foundWeka = @{ Path = $wp; Version = "unknown"; DisplayName = "Weka" } ; break } }
    $cmdWeka = Get-Command "java" -ErrorAction SilentlyContinue
    if (-not $foundWeka -and $cmdWeka) {
        foreach ($wp in $pathsWeka) {
            if (Test-Path (Join-Path $wp "weka.jar")) {
                $foundWeka = @{ Path = $wp; Version = "unknown"; DisplayName = "Weka" }; break
            }
        }
    }
    Add-RResult "Weka" $foundWeka $foundWeka.Path $foundWeka.Version
}

# Julia
if (Want "Julia") {
    $cmdJulia = Detect-ByCommand "julia"
    if ($cmdJulia) { Add-RResult "Julia" $true $cmdJulia.Path }
}

# Gretl
if (Want "Gretl") {
    $regGretl = Get-NsisSoftware "gretl"
    $regGretl2 = Get-NsisSoftwareWow64 "gretl"
    $foundGretl = $regGretl
    if (-not $foundGretl) { $foundGretl = $regGretl2 }
    Add-RResult "Gretl" $foundGretl $foundGretl.Path $foundGretl.Version
}

# PSPP
if (Want "PSPP") {
    $regPspp = Get-NsisSoftware "PSPP"
    $regPspp2 = Get-NsisSoftwareWow64 "PSPP"
    $foundPspp = $regPspp
    if (-not $foundPspp) { $foundPspp = $regPspp2 }
    Add-RResult "PSPP" $foundPspp $foundPspp.Path $foundPspp.Version
}

# JASP
if (Want "JASP") {
    $regJasp = Get-NsisSoftware "JASP"
    $regJasp2 = Get-NsisSoftwareWow64 "JASP"
    $foundJasp = $regJasp
    if (-not $foundJasp) { $foundJasp = $regJasp2 }
    Add-RResult "JASP" $foundJasp $foundJasp.Path $foundJasp.Version
}

# jamovi
if (Want "jamovi") {
    $regJam = Get-NsisSoftware "jamovi"
    $regJam2 = Get-NsisSoftwareWow64 "jamovi"
    $foundJam = $regJam
    if (-not $foundJam) { $foundJam = $regJam2 }
    Add-RResult "jamovi" $foundJam $foundJam.Path $foundJam.Version
}

# KNIME
if (Want "KNIME") {
    $regKnime = Get-NsisSoftware "KNIME"
    $regKnime2 = Get-NsisSoftwareWow64 "KNIME"
    $foundKnime = $regKnime
    if (-not $foundKnime) { $foundKnime = $regKnime2 }
    Add-RResult "KNIME" $foundKnime $foundKnime.Path $foundKnime.Version
}

# Orange
if (Want "Orange") {
    $regOrange = Get-NsisSoftware "Orange"
    $regOrange2 = Get-NsisSoftwareWow64 "Orange"
    $foundOrange = $regOrange
    if (-not $foundOrange) { $foundOrange = $regOrange2 }
    Add-RResult "Orange" $foundOrange $foundOrange.Path $foundOrange.Version
}

# LIMDEP / NLOGIT
if (Want "LIMDEP") {
    $regLimdep = Get-NsisSoftware "LIMDEP"
    $regLimdep2 = Get-NsisSoftwareWow64 "LIMDEP"
    $foundLimdep = $regLimdep
    if (-not $foundLimdep) { $foundLimdep = $regLimdep2 }
    Add-RResult "LIMDEP" $foundLimdep $foundLimdep.Path $foundLimdep.Version
}

# Microfit
if (Want "Microfit") {
    $regMicro = Get-NsisSoftware "Microfit"
    $regMicro2 = Get-NsisSoftwareWow64 "Microfit"
    $foundMicro = $regMicro
    if (-not $foundMicro) { $foundMicro = $regMicro2 }
    Add-RResult "Microfit" $foundMicro $foundMicro.Path $foundMicro.Version
}

# EViews
if (Want "EViews") {
    $regEv = Get-NsisSoftware "EViews"
    $regEv2 = Get-NsisSoftwareWow64 "EViews"
    $foundEv = $regEv
    if (-not $foundEv) { $foundEv = $regEv2 }
    Add-RResult "EViews" $foundEv $foundEv.Path $foundEv.Version
}

# Statistica
if (Want "Statistica") {
    $regStat = Get-NsisSoftware "Statistica"
    $regStat2 = Get-NsisSoftwareWow64 "Statistica"
    $foundStat = $regStat
    if (-not $foundStat) { $foundStat = $regStat2 }
    Add-RResult "Statistica" $foundStat $foundStat.Path $foundStat.Version
}

# AMOS
if (Want "AMOS") {
    $regAmos = Get-NsisSoftware "IBM SPSS Amos"
    $regAmos2 = Get-NsisSoftwareWow64 "IBM SPSS Amos"
    $foundAmos = $regAmos
    if (-not $foundAmos) { $foundAmos = $regAmos2 }
    Add-RResult "AMOS" $foundAmos $foundAmos.Path $foundAmos.Version
}

# Q (MRKS)
if (Want "Q_MRKS") {
    $regQ = Get-NsisSoftware "Q Research"
    $regQ2 = Get-NsisSoftwareWow64 "Q Research"
    $foundQ = $regQ
    if (-not $foundQ) { $foundQ = $regQ2 }
    Add-RResult "Q_MRKS" $foundQ $foundQ.Path $foundQ.Version
}

# Origin
if (Want "Origin") {
    $regOrigin = Get-NsisSoftware "OriginLab Origin"
    $regOrigin2 = Get-NsisSoftwareWow64 "OriginLab Origin"
    $foundOrigin = $regOrigin
    if (-not $foundOrigin) { $foundOrigin = $regOrigin2 }
    if (-not $foundOrigin) {
        $oPaths = @("C:\Program Files\OriginLab\Origin2025", "C:\Program Files\OriginLab\Origin2024", "C:\Program Files (x86)\OriginLab\Origin2023")
        foreach ($op in $oPaths) { if (Test-Path $op) { $foundOrigin = @{ Path = $op; Version = (Split-Path $op -Leaf); DisplayName = "Origin" } ; break } }
    }
    Add-RResult "Origin" $foundOrigin $foundOrigin.Path $foundOrigin.Version
}

# NCSS
if (Want "NCSS") {
    $regNCSS = Get-NsisSoftware "NCSS"
    $regNCSS2 = Get-NsisSoftwareWow64 "NCSS"
    $foundNCSS = $regNCSS
    if (-not $foundNCSS) { $foundNCSS = $regNCSS2 }
    Add-RResult "NCSS" $foundNCSS $foundNCSS.Path $foundNCSS.Version
}

# Mplus
if (Want "Mplus") {
    $regMplus = Get-NsisSoftware "Mplus"
    $regMplus2 = Get-NsisSoftwareWow64 "Mplus"
    $foundMplus = $regMplus
    if (-not $foundMplus) { $foundMplus = $regMplus2 }
    Add-RResult "Mplus" $foundMplus $foundMplus.Path $foundMplus.Version
}

# Minitab
if (Want "Minitab") {
    # Prefer the core "Minitab NN" / "Minitab Statistical Software" entry over the
    # "Minitab Modules" / "minitab shared" add-on, and pick the highest version.
    $regRoots = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    )
    $minitabCore = $null
    foreach ($root in $regRoots) {
        $keys = Get-ChildItem $root -ErrorAction SilentlyContinue
        foreach ($key in $keys) {
            $props = Get-ItemProperty $key.PSPath -ErrorAction SilentlyContinue
            if ($props.DisplayName -match 'Minitab' -and $props.DisplayName -notmatch 'Modules|Shared') {
                if (-not $minitabCore -or ($props.DisplayVersion -gt $minitabCore.Version)) {
                    $minitabCore = @{ Path = $props.InstallLocation; Version = $props.DisplayVersion; DisplayName = $props.DisplayName }
                }
            }
        }
    }
    $foundMinitab = $minitabCore
    if (-not $foundMinitab) {
        $mPaths = @(
            "C:\Program Files\Minitab\Minitab 22",
            "C:\Program Files\Minitab\Minitab 21",
            "C:\Program Files\Minitab\Minitab 20",
            "C:\Program Files\Minitab\Minitab 19",
            "C:\Program Files (x86)\Minitab\Minitab 18"
        )
        foreach ($mp in $mPaths) {
            if (Test-Path (Join-Path $mp "mtb.exe")) {
                $foundMinitab = @{ Path = $mp; Version = (Split-Path $mp -Leaf) -replace 'Minitab ',''; DisplayName = "Minitab" }
                break
            }
        }
    }
    Add-RResult "Minitab" $foundMinitab $foundMinitab.Path $foundMinitab.Version
}

# SHAZAM
if (Want "SHAZAM") {
    $regShaz = Get-NsisSoftware "SHAZAM"
    $regShaz2 = Get-NsisSoftwareWow64 "SHAZAM"
    $foundShaz = $regShaz
    if (-not $foundShaz) { $foundShaz = $regShaz2 }
    Add-RResult "SHAZAM" $foundShaz $foundShaz.Path $foundShaz.Version
}

# TSP
if (Want "TSP") {
    $regTsp = Get-NsisSoftware "TSP"
    $regTsp2 = Get-NsisSoftwareWow64 "TSP"
    $foundTsp = $regTsp
    if (-not $foundTsp) { $foundTsp = $regTsp2 }
    Add-RResult "TSP" $foundTsp $foundTsp.Path $foundTsp.Version
}

# StatTransfer
if (Want "StatTransfer") {
    $regSt = Get-NsisSoftware "StatTransfer"
    $regSt2 = Get-NsisSoftwareWow64 "StatTransfer"
    $foundSt = $regSt
    if (-not $foundSt) { $foundSt = $regSt2 }
    Add-RResult "StatTransfer" $foundSt $foundSt.Path $foundSt.Version
}

# GenStat
if (Want "GenStat") {
    $regGs = Get-NsisSoftware "GenStat"
    $regGs2 = Get-NsisSoftwareWow64 "GenStat"
    $foundGs = $regGs
    if (-not $foundGs) { $foundGs = $regGs2 }
    Add-RResult "GenStat" $foundGs $foundGs.Path $foundGs.Version
}

# CmdStan
if (Want "CmdStan") {
    $cmdStanDir = if ($env:CMDSTAN) { $env:CMDSTAN } else { $null }
    if (-not $cmdStanDir) {
        # NOTE: user-home candidates (C:\Users\<user>\.cmdstan) are intentionally
        # excluded from broad scanning — probing personal profile directories
        # discloses private dev environments beyond the bounded system-level
        # inventory scope (SDI-3). Only system-wide locations are probed here;
        # an explicit $env:CMDSTAN (user-specified) is still honored above.
        $candidates = @("C:\cmdstan", "C:\Tools\cmdstan")
        foreach ($c in $candidates) { if (Test-Path $c) { $cmdStanDir = $c ; break } }
    }
    if ($cmdStanDir) { Add-RResult "CmdStan" $true $cmdStanDir (Split-Path $cmdStanDir -Leaf) }
}

# ────────────── OUTPUT ──────────────
Write-JsonOutput $results
