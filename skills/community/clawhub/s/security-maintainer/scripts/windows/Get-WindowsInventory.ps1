<#
.SYNOPSIS
    Gathers Windows software and update inventory deterministically and safely.
    Recopila de forma determinista y segura el inventario de software de Windows.
    Does NOT modify configuration or install software.
    NO realiza modificaciones de configuración ni instalaciones.
#>

[CmdletBinding()]
param (
    [switch]$IncludeRegistry = $true,
    [switch]$IncludeWinget = $true,
    [switch]$IncludeWindowsUpdate = $true
)

$ErrorActionPreference = "SilentlyContinue"
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

$result = [PSCustomObject]@{
    os_info = $null
    winget_installed = @()
    winget_upgrades = @()
    registry_installed = @()
    windows_updates_pending = @()
    reboot_pending = $false
}

# 1. Información del Sistema Operativo
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $result.os_info = [PSCustomObject]@{
        caption = $os.Caption
        version = $os.Version
        build_number = $os.BuildNumber
        os_architecture = $os.OSArchitecture
        last_boot_up_time = $os.LastBootUpTime.ToString("o")
    }
} catch {
    $result.os_info = [PSCustomObject]@{
        caption = "Microsoft Windows"
        version = [System.Environment]::OSVersion.VersionString
        build_number = ""
        os_architecture = "x64"
        last_boot_up_time = ""
    }
}

# 2. Detección de Reinicio Pendiente
$rebootPendingPaths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired",
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending"
)
foreach ($path in $rebootPendingPaths) {
    if (Test-Path $path) {
        $result.reboot_pending = $true
        break
    }
}

# 3. Aplicaciones vía WinGet
if ($IncludeWinget -and (Get-Command winget -ErrorAction SilentlyContinue)) {
    try {
        $wingetUpgradesRaw = winget upgrade --accept-source-agreements --disable-interactivity 2>$null
        $upgradesList = @()
        $headerIdx = -1
        for ($i = 0; $i -lt $wingetUpgradesRaw.Count; $i++) {
            if ($wingetUpgradesRaw[$i] -match "^-{5,}") {
                $headerIdx = $i - 1
                break
            }
        }

        if ($headerIdx -ge 0) {
            for ($i = $headerIdx + 2; $i -lt $wingetUpgradesRaw.Count; $i++) {
                $line = $wingetUpgradesRaw[$i]
                if ([string]::IsNullOrWhiteSpace($line) -or $line -match "^\d+\s+(actualizaciones|paquete|upgrades|package)") {
                    break
                }
                $parts = [regex]::Split($line.Trim(), "\s{2,}")
                if ($parts.Count -ge 4) {
                    $src = "winget"
                    if ($parts.Count -ge 5) {
                        $src = $parts[4].Trim()
                        $avail = $parts[3].Trim()
                        $inst = $parts[2].Trim()
                        $id = $parts[1].Trim()
                        $name = $parts[0].Trim()
                    } elseif ($parts[3] -in @("winget", "msstore")) {
                        $src = $parts[3].Trim()
                        $avail = $parts[2].Trim()
                        if ($parts[1] -match "^(\S+)\s+(.+)$") {
                            $id = $Matches[1].Trim()
                            $inst = $Matches[2].Trim()
                            $name = $parts[0].Trim()
                        } else {
                            $lastSpace = $parts[0].LastIndexOf(" ")
                            if ($lastSpace -gt 0) {
                                $name = $parts[0].Substring(0, $lastSpace).Trim()
                                $id = $parts[0].Substring($lastSpace + 1).Trim()
                            } else {
                                $name = $parts[0].Trim()
                                $id = $parts[0].Trim()
                            }
                            $inst = $parts[1].Trim()
                        }
                    } else {
                        $name = $parts[0].Trim()
                        $id = $parts[1].Trim()
                        $inst = $parts[2].Trim()
                        $avail = $parts[3].Trim()
                        if ($avail -match "\s+(winget|msstore)$") {
                            $src = $Matches[1]
                            $avail = ($avail -replace "\s+(winget|msstore)$", "").Trim()
                        }
                    }

                    $upgradesList += [PSCustomObject]@{
                        name = $name
                        id = $id
                        installed_version = $inst
                        latest_version = $avail
                        source = $src
                    }
                }
            }
        }
        $result.winget_upgrades = $upgradesList
    } catch {}
}

# 4. Aplicaciones en Registro (desinstaladores)
if ($IncludeRegistry) {
    $uninstallKeys = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    $regApps = @()
    foreach ($k in $uninstallKeys) {
        Get-ItemProperty $k 2>$null | Where-Object { $_.DisplayName -and -not $_.SystemComponent } | ForEach-Object {
            $regApps += [PSCustomObject]@{
                name = $_.DisplayName
                id = $_.PSChildName
                installed_version = if ($_.DisplayVersion) { $_.DisplayVersion } else { "desconocida" }
                publisher = $_.Publisher
                install_date = $_.InstallDate
                uninstall_string = if ($_.UninstallString) { "disponible" } else { "no_disponible" }
            }
        }
    }
    $result.registry_installed = $regApps
}

# 5. Windows Updates pendientes vía COM
if ($IncludeWindowsUpdate) {
    try {
        $updateJob = Start-Job -ScriptBlock {
            try {
                $session = New-Object -ComObject Microsoft.Update.Session
                $searcher = $session.CreateUpdateSearcher()
                $searcher.Online = $false
                $res = $searcher.Search("IsInstalled=0 and Type='Software'")
                $list = @()
                foreach ($u in $res.Updates) {
                    $kbArticles = @()
                    foreach ($kb in $u.KBArticleIDs) {
                        $kbArticles += "KB$kb"
                    }
                    $list += [PSCustomObject]@{
                        title = $u.Title
                        kb_articles = $kbArticles
                        is_mandatory = $u.IsMandatory
                        severity = $u.MsrcSeverity
                    }
                }
                return $list
            } catch {
                return @()
            }
        }
        $completed = Wait-Job $updateJob -Timeout 8
        if ($completed) {
            $result.windows_updates_pending = @(Receive-Job $updateJob)
        }
        Remove-Job $updateJob -Force 2>$null
    } catch {
        # Si la API COM no está disponible o requiere elevación, se deja vacío sin fallar
    }
}

$result | ConvertTo-Json -Depth 5 -Compress
