$ErrorActionPreference = "SilentlyContinue"

try {
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
} catch {}

try {
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
} catch {}

if ($env:OS -ne "Windows_NT") {
    Write-Error "This helper script only supports Windows."
    exit 1
}

$items = @{}

function Test-CommandExists {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Add-AppRecord {
    param(
        [string]$Name,
        [string]$Version,
        [string]$DownloadUrl,
        [string]$Comments,
        [string]$SourceTag
    )

    if ([string]::IsNullOrWhiteSpace($Name)) { return }

    $cleanName = $Name.Trim()
    $key = $cleanName.ToLowerInvariant()
    $cleanVersion = if ($Version) { $Version.Trim() } else { "" }
    $cleanUrl = if ($DownloadUrl) { $DownloadUrl.Trim() } else { "" }
    $cleanComments = if ($Comments) { $Comments.Trim() } else { "" }

    $sourceRank = if ($SourceTag -eq "package_manager") { 2 } else { 1 }

    if (-not $items.ContainsKey($key)) {
        $items[$key] = [pscustomobject]@{
            name = $cleanName
            version = $cleanVersion
            download_url = $cleanUrl
            comments = $cleanComments
            source_rank = $sourceRank
            source_tag = $SourceTag
        }
        return
    }

    $existing = $items[$key]

    if ([string]::IsNullOrWhiteSpace($existing.version) -and $cleanVersion) {
        $existing.version = $cleanVersion
    }

    if ([string]::IsNullOrWhiteSpace($existing.download_url) -and $cleanUrl) {
        $existing.download_url = $cleanUrl
    }

    if ($sourceRank -gt $existing.source_rank) {
        if ($cleanComments) {
            $existing.comments = $cleanComments
        }
        $existing.source_tag = $SourceTag
        $existing.source_rank = $sourceRank
    } elseif ($cleanComments) {
        if ($existing.comments -notlike ("*" + $cleanComments + "*")) {
            if ([string]::IsNullOrWhiteSpace($existing.comments)) {
                $existing.comments = $cleanComments
            } else {
                $existing.comments = $existing.comments.Trim("; ") + "; " + $cleanComments
            }
        }
    }

    if ([string]::IsNullOrWhiteSpace($existing.source_tag) -and $SourceTag) {
        $existing.source_tag = $SourceTag
    }
}

function Get-CommentForUrl {
    param(
        [string]$Source,
        [string]$Url,
        [bool]$FromCli
    )

    if ($FromCli -and $Url) {
        return "Detected from $Source. URL provided by CLI/package metadata."
    }

    if ($Url) {
        return "Detected from $Source. URL may not be a real download URL; it may be a vendor or product page."
    }

    return "Detected from $Source. Reinstall URL not confirmed."
}

function Collect-Windows {
    $uninstallPaths = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )

    Get-ItemProperty $uninstallPaths |
        Where-Object {
            $_.DisplayName -and
            $_.SystemComponent -ne 1 -and
            $_.ReleaseType -notin @("Update", "Hotfix", "Security Update") -and
            $_.ParentKeyName -eq $null
        } |
        ForEach-Object {
            $url = ""
            if ($_.URLInfoAbout) {
                $url = $_.URLInfoAbout
            } elseif ($_.HelpLink) {
                $url = $_.HelpLink
            }

            $comments = Get-CommentForUrl -Source "Windows uninstall registry" -Url $url -FromCli:$false
            Add-AppRecord -Name $_.DisplayName -Version $_.DisplayVersion -DownloadUrl $url -Comments $comments -SourceTag "registry"
        }

    if (-not (Test-CommandExists "winget")) { return }

    $wingetOutput = & winget list --accept-source-agreements --disable-interactivity 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $wingetOutput) { return }

    $headerIndex = -1
    $separatorIndex = -1
    for ($i = 0; $i -lt $wingetOutput.Count; $i++) {
        if ($wingetOutput[$i] -match "^-{3,}") {
            $separatorIndex = $i
            $headerIndex = $i - 1
            break
        }
    }

    if ($headerIndex -lt 0 -or $separatorIndex -lt 0) { return }

    $header = $wingetOutput[$headerIndex]
    $idPos = $header.IndexOf("Id")
    $verPos = $header.IndexOf("Version")
    $availPos = $header.IndexOf("Available")
    $sourcePos = $header.IndexOf("Source")

    if ($idPos -lt 0) { $idPos = 40 }
    if ($verPos -lt 0) { $verPos = 80 }
    if ($sourcePos -lt 0) { $sourcePos = $header.Length }

    if ($availPos -gt $verPos) {
        $versionEnd = $availPos
    } elseif ($sourcePos -gt $verPos) {
        $versionEnd = $sourcePos
    } else {
        $versionEnd = $header.Length
    }

    for ($i = $separatorIndex + 1; $i -lt $wingetOutput.Count; $i++) {
        $line = $wingetOutput[$i]
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line.Length -lt 2) { continue }

        $name = $line.Substring(0, [Math]::Min($idPos, $line.Length)).Trim()
        $version = ""
        $pkgId = ""

        if ($line.Length -gt $idPos) {
            $idLen = [Math]::Max(0, [Math]::Min($verPos, $line.Length) - $idPos)
            if ($idLen -gt 0) {
                $pkgId = $line.Substring($idPos, $idLen).Trim()
            }
        }

        if ($line.Length -gt $verPos) {
            $verLen = [Math]::Max(0, [Math]::Min($versionEnd, $line.Length) - $verPos)
            if ($verLen -gt 0) {
                $version = $line.Substring($verPos, $verLen).Trim()
            }
        }

        if (-not [string]::IsNullOrWhiteSpace($name)) {
            $comments = "Detected in winget. Likely reinstallable automatically."
            if ($pkgId) {
                $comments = "Detected in winget ($pkgId). Likely reinstallable automatically."
            }
            Add-AppRecord -Name $name -Version $version -DownloadUrl "" -Comments $comments -SourceTag "package_manager"
        }
    }
}

Collect-Windows

$rows = $items.Values |
    Sort-Object name |
    Select-Object name, version, download_url, comments, source_tag

@($rows) | ConvertTo-Json -Depth 3
