# statsoft-modeler.ps1 -- SPSS Modeler CLI wrapper (batch mode)
# Uses clemb.exe (CLEmbedded Modeler)
#
# Usage:
#   statsoft-modeler run <stream.str> [-log <file>] [-scriptlang python|legacy]
#   statsoft-modeler run-script <script.txt> [-log <file>] [-scriptlang python|legacy]
#   statsoft-modeler server-run <stream.str> -hostname <host> -port <port> [-log <file>]
#   statsoft-modeler info

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "run-script", "server-run", "info")]
    [string]$Command,

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$scriptDir  = Split-Path $MyInvocation.MyCommand.Path -Parent
$configPath = Join-Path $scriptDir "..\config.json"

# Locate clemb.exe -- try config.json first
$clembExe = $null
if (Test-Path $configPath) {
    $cfg = Get-Content $configPath -Raw | ConvertFrom-Json
    if ($cfg."SPSS Modeler" -and $cfg."SPSS Modeler".Path -and (Test-Path $cfg."SPSS Modeler".Path)) {
        $clembExe = $cfg."SPSS Modeler".Path
    }
}

# Auto-search if not in config
if (-not $clembExe) {
    $candidates = @(
        "C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe",
        "C:\Program Files\IBM\SPSS\Modeler\18.1\bin\clemb.exe",
        "C:\Program Files\IBM\SPSS\Modeler\18.2\bin\clemb.exe",
        "C:\Program Files\IBM\SPSS\Modeler\18.3\bin\clemb.exe",
        "C:\Program Files\IBM\SPSS\Modeler\18.4\bin\clemb.exe",
        "C:\Program Files\IBM\SPSS\Modeler\18.5\bin\clemb.exe",
        "C:\Program Files\IBM\SPSS\Modeler\18.6\bin\clemb.exe",
        "C:\Program Files (x86)\IBM\SPSS\Modeler\18.0\bin\clemb.exe",
        "C:\Program Files (x86)\IBM\SPSS\Modeler\18.1\bin\clemb.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { $clembExe = $c; break }
    }
}

if (-not $clembExe -or -not (Test-Path $clembExe)) {
    Write-Error "SPSS Modeler (clemb.exe) not found. Run setup_modeler.ps1 first."
    exit 1
}

$binDir        = Split-Path $clembExe -Parent
$modelerClient = Join-Path $binDir "modelerclient.exe"
$version       = if (Test-Path $modelerClient) { [System.Diagnostics.FileVersionInfo]::GetVersionInfo($modelerClient).FileVersion } else { "unknown" }

Write-Host "[statsoft-modeler] clemb:   $clembExe" -ForegroundColor Cyan
Write-Host "[statsoft-modeler] version: $version" -ForegroundColor Cyan

function Invoke-Clemb {
    param(
        [hashtable]$Options,
        [string]$LogFile
    )
    $argList = @("-local")

    if ($Options["stream"])    { $argList += '-stream "{0}"' -f $Options["stream"] }
    if ($Options["state"])     { $argList += '-state "{0}"'  -f $Options["state"] }
    if ($Options["script"])    { $argList += '-script "{0}"' -f $Options["script"] }
    if ($Options["project"])   { $argList += '-project "{0}"' -f $Options["project"] }
    if ($Options["output"])    { $argList += '-output "{0}"' -f $Options["output"] }
    if ($Options["model"])     { $argList += '-model "{0}"'  -f $Options["model"] }
    if ($Options["scriptlang"]){ $argList += '-scriptlang "{0}"' -f $Options["scriptlang"] }

    if ($Options["server"])    { $argList += "-server" }
    if ($Options["hostname"])  { $argList += '-hostname "{0}"' -f $Options["hostname"] }
    if ($Options["port"])      { $argList += "-port $($Options["port"])" }
    if ($Options["username"])  { $argList += '-username "{0}"' -f $Options["username"] }
    if ($Options["password"])  { $argList += '-password "{0}"' -f $Options["password"] }
    if ($Options["use_ssl"])   { $argList += "-use_ssl" }
    if ($Options["cluster"])   { $argList += '-cluster "{0}"' -f $Options["cluster"] }

    if ($LogFile)              { $argList += '-log "{0}"' -f $LogFile }
    if ($Options["appendlog"]) { $argList += "-appendlog" }
    if ($Options["nolog"])     { $argList += "-nolog" }
    if ($Options["directory"]) { $argList += '-directory "{0}"' -f $Options["directory"] }

    $argList += "-execute"

    Write-Host "[statsoft-modeler] Args: $($argList -join ' ')" -ForegroundColor Yellow

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName               = $clembExe
    $psi.Arguments              = $argList -join ' '
    $psi.UseShellExecute        = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError  = $true
    $psi.CreateNoWindow         = $true

    $proc = [System.Diagnostics.Process]::Start($psi)
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit(600000)

    if ($stdout) { Write-Host $stdout }
    if ($stderr) { Write-Warning $stderr }
    Write-Host "[statsoft-modeler] Exit code: $($proc.ExitCode)" -ForegroundColor Green
    return $proc.ExitCode
}

switch ($Command) {
    "info" {
        Write-Host "`n=== SPSS Modeler environment ===" -ForegroundColor Yellow
        Write-Host "Version:           $version"
        Write-Host "clemb.exe:         $clembExe"
        Write-Host "modelerclient.exe: $(if (Test-Path $modelerClient) { 'Found' } else { 'Not found' })"
        Write-Host "bin dir:           $binDir"
        Write-Host ""
        Write-Host "clemb -help output:" -ForegroundColor Yellow
        & $clembExe -help 2>&1 | ForEach-Object { Write-Host "  $_" }
    }

    "run" {
        if ($Args.Count -eq 0) { Write-Error "Missing stream file path."; exit 1 }
        $streamFile = $Args[0]
        if (-not (Test-Path $streamFile)) { Write-Error "Stream file not found: $streamFile"; exit 1 }
        $logFile = Join-Path $PWD "modeler_run.log"
        $rc = Invoke-Clemb @{ "stream" = $streamFile } $logFile
        exit $rc
    }

    "run-script" {
        if ($Args.Count -eq 0) { Write-Error "Missing script file path."; exit 1 }
        $scriptFile = $Args[0]
        if (-not (Test-Path $scriptFile)) { Write-Error "Script file not found: $scriptFile"; exit 1 }
        $logFile = Join-Path $PWD "modeler_script.log"
        $rc = Invoke-Clemb @{ "script" = $scriptFile; "scriptlang" = "python" } $logFile
        exit $rc
    }

    "server-run" {
        if ($Args.Count -eq 0) { Write-Error "Missing stream file path."; exit 1 }
        $streamFile = $Args[0]
        if (-not (Test-Path $streamFile)) { Write-Error "Stream file not found: $streamFile"; exit 1 }
        $logFile = Join-Path $PWD "modeler_server.log"
        $rc = Invoke-Clemb @{ "stream" = $streamFile; "server" = $true; "hostname" = "localhost"; "port" = "80" } $logFile
        exit $rc
    }

    default {
        Write-Error "Unknown command: $Command"
        Write-Host "Usage: statsoft-modeler (run|run-script|server-run|info) [args]"
    }
}
