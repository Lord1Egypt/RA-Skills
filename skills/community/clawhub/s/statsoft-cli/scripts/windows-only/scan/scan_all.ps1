# scan_all.ps1 — Windows 批量检测已安装统计软件
# 输出 JSON 格式：{"R":{"installed":true,"path":"...","version":"..."},...}
# 注册表检测 + 常见路径扫描 + 命令行 which

$ErrorActionPreference = "SilentlyContinue"

$results = @{}

function Write-JsonOutput($obj) {
    $obj | ConvertTo-Json -Depth 3 -Compress
}

function Add-RResult($name, $installed, $path, $version) {
    if ($installed -or $null -eq $installed) {
        $results[$name] = @{
            installed = $true
            path = $path
            version = $version
            platform = "windows"
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
    # 搜索 HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
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
    # 搜索 32-bit 注册表 (WoW6432Node)
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
            # 尝试提取版本号
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

# R
$regR = Get-NsisSoftware "R for Windows"
$regR2 = Get-NsisSoftwareWow64 "R for Windows"
$pathsR = @("C:\Program Files\R\R*\bin\R.exe", "C:\Program Files (x86)\R\R*\bin\R.exe")
$foundR = $null
# Check path-based
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

# Python
$cmdPy = Detect-ByCommand "python"
$cmdPy2 = Detect-ByCommand "python3"
if ($cmdPy) { Add-RResult "Python" $true $cmdPy.Path (& python --version 2>&1) } else {
    if ($cmdPy2) { Add-RResult "Python" $cmdPy2 }
}

# SPSS Statistics — 动态扫描所有盘符 / Dynamic scan all drives
$regSpss = Get-NsisSoftware "IBM SPSS Statistics"
$regSpss2 = Get-NsisSoftwareWow64 "IBM SPSS Statistics"
$foundSpss = $regSpss
if (-not $foundSpss) { $foundSpss = $regSpss2 }
# Also check known paths dynamically
if (-not $foundSpss) {
    $drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 } | Select-Object -ExpandProperty Name
    $versions = @("30", "29", "28", "27", "26")
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

# SPSS Modeler
$regModeler = Get-NsisSoftware "IBM SPSS Modeler"
$regModeler2 = Get-NsisSoftwareWow64 "IBM SPSS Modeler"
$foundModeler = $regModeler
if (-not $foundModeler) { $foundModeler = $regModeler2 }
Add-RResult "SPSS Modeler" $foundModeler $foundModeler.Path $foundModeler.Version

# Stata
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

# SAS (SAS Foundation)
$regSas = Get-NsisSoftware "SAS Foundation"
$regSas2 = Get-NsisSoftwareWow64 "SAS Foundation"
$foundSas = $regSas
if (-not $foundSas) { $foundSas = $regSas2 }
Add-RResult "SAS" $foundSas $foundSas.Path $foundSas.Version

# R (already handled, but let's also add RStudio detection)
# Matlab
$regMatlab = Get-NsisSoftware "MATLAB"
$regMatlab2 = Get-NsisSoftwareWow64 "MATLAB"
$foundMatlab = $regMatlab
if (-not $foundMatlab) { $foundMatlab = $regMatlab2 }
if (-not $foundMatlab) {
    # Try mathworks paths
    $mwPaths = @("C:\Program Files\MATLAB\R2025a", "C:\Program Files\MATLAB\R2024b", "C:\Program Files\MATLAB\R2024a")
    foreach ($mp in $mwPaths) {
        if (Test-Path $mp) {
            & "$mp\bin\matlab.exe" -batch "disp(version)" 2>&1 | Out-Null
            $foundMatlab = @{ Path = $mp; Version = ($mp -replace '.*R','R'); DisplayName = "MATLAB" }
            break
        }
    }
}
Add-RResult "Matlab" $foundMatlab $foundMatlab.Path $foundMatlab.Version

# Mathematica
$regMath = Get-NsisSoftware "Mathematica"
$regMath2 = Get-NsisSoftwareWow64 "Mathematica"
$foundMath = $regMath
if (-not $foundMath) { $foundMath = $regMath2 }
if (-not $foundMath) {
    $mathPaths = @("C:\Program Files\Wolfram Research\Mathematica\14.0", "C:\Program Files\Wolfram Research\Mathematica\13.0", "C:\Program Files\Wolfram Research\Mathematica\12.0", "C:\Program Files (x86)\Wolfram Research\Mathematica")
    foreach ($mp in $mathPaths) { if (Test-Path $mp) { $foundMath = @{ Path = $mp; Version = (Split-Path $mp -Leaf); DisplayName = "Mathematica" } ; break } }
}
Add-RResult "Mathematica" $foundMath $foundMath.Path $foundMath.Version

# JMP
$regJmp = Get-NsisSoftware "JMP"
$regJmp2 = Get-NsisSoftwareWow64 "JMP"
$foundJmp = $regJmp
if (-not $foundJmp) { $foundJmp = $regJmp2 }
Add-RResult "JMP" $foundJmp $foundJmp.Path $foundJmp.Version

# Rattle
$cmdRattle = Detect-ByCommand "rattle"
if ($cmdRattle) { Add-RResult "Rattle" $true $cmdRattle.Path }

# Weka
$pathsWeka = @("C:\Program Files\Weka-3-8*", "C:\Program Files (x86)\Weka")
$foundWeka = $null
foreach ($wp in $pathsWeka) { if (Test-Path $wp) { $foundWeka = @{ Path = $wp; Version = "unknown"; DisplayName = "Weka" } ; break } }
# Try command
$cmdWeka = Get-Command "java" -ErrorAction SilentlyContinue
if (-not $foundWeka -and $cmdWeka) {
    # Check if weka.jar exists nearby
    foreach ($wp in $pathsWeka) {
        if (Test-Path (Join-Path $wp "weka.jar")) {
            $foundWeka = @{ Path = $wp; Version = "unknown"; DisplayName = "Weka" }; break
        }
    }
}
Add-RResult "Weka" $foundWeka $foundWeka.Path $foundWeka.Version

# Julia
$pathsJulia = @("C:\Program Files\Julia*\bin\julia.exe", "C:\Users\*\AppData\Local\Programs\Julia*\bin\julia.exe")
$cmdJulia = Detect-ByCommand "julia"
if ($cmdJulia) { Add-RResult "Julia" $true $cmdJulia.Path }

# Gretl
$regGretl = Get-NsisSoftware "gretl"
$regGretl2 = Get-NsisSoftwareWow64 "gretl"
$foundGretl = $regGretl
if (-not $foundGretl) { $foundGretl = $regGretl2 }
Add-RResult "Gretl" $foundGretl $foundGretl.Path $foundGretl.Version

# PSPP
$regPspp = Get-NsisSoftware "PSPP"
$regPspp2 = Get-NsisSoftwareWow64 "PSPP"
$foundPspp = $regPspp
if (-not $foundPspp) { $foundPspp = $regPspp2 }
Add-RResult "PSPP" $foundPspp $foundPspp.Path $foundPspp.Version

# JASP
$regJasp = Get-NsisSoftware "JASP"
$regJasp2 = Get-NsisSoftwareWow64 "JASP"
$foundJasp = $regJasp
if (-not $foundJasp) { $foundJasp = $regJasp2 }
Add-RResult "JASP" $foundJasp $foundJasp.Path $foundJasp.Version

# jamovi
$regJam = Get-NsisSoftware "jamovi"
$regJam2 = Get-NsisSoftwareWow64 "jamovi"
$foundJam = $regJam
if (-not $foundJam) { $foundJam = $regJam2 }
Add-RResult "jamovi" $foundJam $foundJam.Path $foundJam.Version

# KNIME
$regKnime = Get-NsisSoftware "KNIME"
$regKnime2 = Get-NsisSoftwareWow64 "KNIME"
$foundKnime = $regKnime
if (-not $foundKnime) { $foundKnime = $regKnime2 }
Add-RResult "KNIME" $foundKnime $foundKnime.Path $foundKnime.Version

# H2O (installed via Python, treat as Python package)
$cmdH2O = Detect-ByCommand "python"
# Cannot reliably detect pip packages list here; handled by config script

# Orange
$regOrange = Get-NsisSoftware "Orange"
$regOrange2 = Get-NsisSoftwareWow64 "Orange"
$foundOrange = $regOrange
if (-not $foundOrange) { $foundOrange = $regOrange2 }
Add-RResult "Orange" $foundOrange $foundOrange.Path $foundOrange.Version

# LIMDEP / NLOGIT
$regLimdep = Get-NsisSoftware "LIMDEP"
$regLimdep2 = Get-NsisSoftwareWow64 "LIMDEP"
$foundLimdep = $regLimdep
if (-not $foundLimdep) { $foundLimdep = $regLimdep2 }
Add-RResult "LIMDEP" $foundLimdep $foundLimdep.Path $foundLimdep.Version

# Microfit
$regMicro = Get-NsisSoftware "Microfit"
$regMicro2 = Get-NsisSoftwareWow64 "Microfit"
$foundMicro = $regMicro
if (-not $foundMicro) { $foundMicro = $regMicro2 }
Add-RResult "Microfit" $foundMicro $foundMicro.Path $foundMicro.Version

# EViews
$regEv = Get-NsisSoftware "EViews"
$regEv2 = Get-NlisSoftwareWow64 "EViews"
$foundEv = $regEv
if (-not $foundEv) { $foundEv = $regEv2 }
Add-RResult "EViews" $foundEv $foundEv.Path $foundEv.Version

# Statistica
$regStat = Get-NsisSoftware "Statistica"
$regStat2 = Get-NlisSoftwareWow64 "Statistica"
$foundStat = $regStat
if (-not $foundStat) { $foundStat = $regStat2 }
Add-RResult "Statistica" $foundStat $foundStat.Path $foundStat.Version

# AMOS
$regAmos = Get-NlisSoftware "IBM SPSS Amos"
$regAmos2 = Get-NlisSoftwareWow64 "IBM SPSS Amos"
$foundAmos = $regAmos
if (-not $foundAmos) { $foundAmos = $regAmos2 }
Add-RResult "AMOS" $foundAmos $foundAmos.Path $foundAmos.Version

# Q (MRKS)
$regQ = Get-NlisSoftware "Q Research"
$regQ2 = Get-NlisSoftwareWow64 "Q Research"
$foundQ = $regQ
if (-not $foundQ) { $foundQ = $regQ2 }
Add-RResult "Q (MRKS)" $foundQ $foundQ.Path $foundQ.Version

# Origin
$regOrigin = Get-NlisSoftware "OriginLab Origin"
$regOrigin2 = Get-NlisSoftwareWow64 "OriginLab Origin"
$foundOrigin = $regOrigin
if (-not $foundOrigin) { $foundOrigin = $regOrigin2 }
if (-not $foundOrigin) {
    $oPaths = @("C:\Program Files\OriginLab\Origin2025", "C:\Program Files\OriginLab\Origin2024", "C:\Program Files (x86)\OriginLab\Origin2023")
    foreach ($op in $oPaths) { if (Test-Path $op) { $foundOrigin = @{ Path = $op; Version = (Split-Path $op -Leaf); DisplayName = "Origin" } ; break } }
}
Add-RResult "Origin" $foundOrigin $foundOrigin.Path $foundOrigin.Version

# NCSS
$regNCSS = Get-NlisSoftware "NCSS"
$regNCSS2 = Get-NlisSoftwareWow64 "NCSS"
$foundNCSS = $regNCSS
if (-not $foundNCSS) { $foundNCSS = $regNCSS2 }
Add-RResult "NCSS" $foundNCSS $foundNCSS.Path $foundNCSS.Version

# Mplus
$regMplus = Get-NlisSoftware "Mplus"
$regMplus2 = Get-NlisSoftwareWow64 "Mplus"
$foundMplus = $regMplus
if (-not $foundMplus) { $foundMplus = $regMplus2 }
Add-RResult "Mplus" $foundMplus $foundMplus.Path $foundMplus.Version

# SHAZAM
$regShaz = Get-NlisSoftware "SHAZAM"
$regShaz2 = Get-NlisSoftwareWow64 "SHAZAM"
$foundShaz = $regShaz
if (-not $foundShaz) { $foundShaz = $regShaz2 }
Add-RResult "SHAZAM" $foundShaz $foundShaz.Path $foundShaz.Version

# TSP
$regTsp = Get-NlisSoftware "TSP"
$regTsp2 = Get-NlisSoftwareWow64 "TSP"
$foundTsp = $regTsp
if (-not $foundTsp) { $foundTsp = $regTsp2 }
Add-RResult "TSP" $foundTsp $foundTsp.Path $foundTsp.Version

# StatTransfer
$regSt = Get-NlisSoftware "StatTransfer"
$regSt2 = Get-NlisSoftwareWow64 "StatTransfer"
$foundSt = $regSt
if (-not $foundSt) { $foundSt = $regSt2 }
Add-RResult "StatTransfer" $foundSt $foundSt.Path $foundSt.Version

# GenStat
$regGs = Get-NlisSoftware "GenStat"
$regGs2 = Get-NlisSoftwareWow64 "GenStat"
$foundGs = $regGs
if (-not $foundGs) { $foundGs = $regGs2 }
Add-RResult "GenStat" $foundGs $foundGs.Path $foundGs.Version

# CmdStan
$cmdStanDir = if ($env:CMDSTAN) { $env:CMDSTAN } else { $null }
if (-not $cmdStanDir) {
    $candidates = @("C:\Users\$env:USERNAME\.cmdstan", "C:\Users\$env:USERNAME\cmdstan", "C:\cmdstan", "C:\Tools\cmdstan")
    foreach ($c in $candidates) { if (Test-Path $c) { $cmdStanDir = $c ; break } }
}
if ($cmdStanDir) { Add-RResult "CmdStan" $true $cmdStanDir (Split-Path $cmdStanDir -Leaf) }

# ────────────── OUTPUT ──────────────
Write-JsonOutput $results
