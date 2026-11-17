# statsoft-sas.ps1 — SAS EXECUTION wrapper (NOT a setup/detection tool).
# This script INVOKES the third-party SAS binary and CREATES temporary/log files.
# It does NOT modify config.json or environment variables.
#
# Commands:
#   run <sas_file> [-LogFile <name>]  EXECUTES SAS on the given program; writes a
#                                     .log/.lst in the current directory.
#                                     Requires explicit authorization (default-deny).
#   data-info <sas_file>              EXECUTES SAS (proc contents) on the USER-SUPPLIED
#                                     file via a temporary .sas file (auto-deleted).
#                                     Requires the same authorization gate as `run`.
#   read-log <log_path>              Read-only: prints an existing SAS log. No execution.
#
# Authorization (for `run` and `data-info`): FAIL-CLOSED. Proceeds ONLY when
#   STATSOFT_AUTO_WRITE=1, or STATSOFT_CONFIRM=1 on a TTY answered `y`.
# Log/temp paths are constrained to the current working directory (no traversal).

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "data-info", "read-log")]
    [string]$Command,
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,
    
    [string]$LogFile
)

# ============================================================
# Language Detection
# ============================================================
$systemLang = [System.Globalization.CultureInfo]::CurrentUICulture.Name
$script:isZH = $systemLang.StartsWith("zh")

function Write-Lang {
    param(
        [string]$CN,
        [string]$EN,
        [System.ConsoleColor]$Color = "White"
    )
    if ($script:isZH) {
        Write-Host $CN -ForegroundColor $Color
    } else {
        Write-Host $EN -ForegroundColor $Color
    }
}

function Write-Lang-Warning {
    param(
        [string]$CN,
        [string]$EN
    )
    if ($script:isZH) {
        Write-Warning $CN
    } else {
        Write-Warning $EN
    }
}

# Headless launcher (no GUI popup) — single enforcement point for the skill default.
$__d = $PSScriptRoot
while ($__d -and -not (Test-Path (Join-Path $__d "common/invoke_hidden.ps1"))) {
    $__p = Split-Path $__d -Parent; if ($__p -eq $__d) { break }; $__d = $__p
}
. (Join-Path $__d "common/invoke_hidden.ps1")

function Test-UserAuthorizedToRun {
    # Execution authorization gate — FAIL-CLOSED (default deny).
    # Proceed ONLY when an explicit opt-in is present:
    #   * STATSOFT_AUTO_WRITE=1                          -> non-interactive/agent opt-in
    #   * STATSOFT_CONFIRM=1 AND a real TTY AND user answers y -> interactive confirm
    # Any other case (incl. a plain user invocation without opt-in) -> deny, so
    # an agent or upstream tool cannot trigger third-party execution unexpectedly.
    $autoWrite = $env:STATSOFT_AUTO_WRITE -eq '1'
    $confirm = $env:STATSOFT_CONFIRM -eq '1'
    if ($autoWrite) { return $true }
    if ($confirm -and -not [Console]::IsInputRedirected) {
        $prompt = if ($script:isZH) { "确认运行 SAS？该操作将执行第三方外部二进制 (y/N)" } else { "Confirm running SAS? This executes a third-party external binary (y/N)" }
        $ans = Read-Host $prompt
        return ($ans -match '^[yY]')
    }
    return $false
}

function Resolve-SafeLogPath {
    # Constrain user-supplied log output to a plain filename inside the current
    # working directory. Reject absolute/rooted paths and parent traversal so a
    # caller cannot write an arbitrary file elsewhere on disk (SDI-1).
    param(
        [string]$Requested,
        [string]$DefaultName
    )
    if (-not $Requested) { return (Join-Path $PWD $DefaultName) }
    if ([System.IO.Path]::IsPathRooted($Requested) -or $Requested -match '[\\/]|\.\.') {
        $leaf = Split-Path $Requested -Leaf
        Write-Lang-Warning "已忽略不安全的日志路径，仅使用文件名并写入当前目录: $leaf" "Ignored unsafe log path; using filename in current directory only: $leaf"
        return (Join-Path $PWD $leaf)
    }
    return (Join-Path $PWD $Requested)
}

# 读取配置
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (-not (Test-Path $configPath)) {
    Write-Error "$(if ($script:isZH) { '配置文件不存在' } else { 'Config file not found' }): $configPath"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$sasPath = $config.SAS.Path

if (-not (Test-Path $sasPath)) {
    Write-Error "$(if ($script:isZH) { 'SAS 可执行文件不存在' } else { 'SAS executable not found' }): $sasPath"
    exit 1
}

switch ($Command) {
    "run" {
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow
            exit 1
        }
        $sasFile = $Args[0]
        if (-not (Test-Path $sasFile)) {
            Write-Error "$(if ($script:isZH) { 'SAS 程序不存在' } else { 'SAS program not found' }): $sasFile"
            exit 1
        }
        
        $logPath = Resolve-SafeLogPath -Requested $LogFile -DefaultName "sas-log.log"
        $printPath = ($logPath -replace '\.log$', '.lst')
        if ($printPath -eq $logPath) { $printPath = "$logPath.lst" }
        
        Write-Lang "执行 SAS 程序: $sasFile" "Executing SAS program: $sasFile" -Color Cyan
        Write-Lang "日志输出（将写入当前目录）: $logPath" "Log output (written to current directory): $logPath" -Color Gray
        
        $result = Invoke-StatExe -FilePath $sasPath -ArgumentList "-batch","-nosplash","-sysin",$sasFile,"-log",$logPath,"-print",$printPath

        if ($result.ExitCode -eq 0) {
            Write-Lang "SAS 执行完成" "SAS execution complete" -Color Green
        } else {
            Write-Lang-Warning "SAS 退出码: $($result.ExitCode)" "SAS exit code: $($result.ExitCode)"
            if ($result.StdErr) { Write-Host $result.StdErr -ForegroundColor Red }
        }
    }
    
    "data-info" {
        # data-info EXECUTES the SAS binary and writes a temporary .sas file, so it
        # is gated by the same default-deny authorization as `run` (SDI-1).
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow
            exit 1
        }
        $sasFile = $Args[0]
        if (-not (Test-Path $sasFile)) {
            Write-Error "$(if ($script:isZH) { 'SAS 程序不存在' } else { 'SAS program not found' }): $sasFile"
            exit 1
        }

        $tempSas = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.sas'
        Write-Lang "执行 SAS（proc contents），将创建临时文件并在结束后删除" "Executing SAS (proc contents); a temporary file is created and deleted afterward." -Color Cyan
        try {
            # Inspect the USER-SUPPLIED SAS file (not a hardcoded dataset like sashelp.class).
            $safeFile = $sasFile.Replace('\', '/')
            # Write WITHOUT a UTF-8 BOM (some SAS runtimes treat the BOM as part of the
            # first statement).
            $sasContent = @"
proc contents data="$safeFile" details;
run;
"@
            [System.IO.File]::WriteAllText($tempSas, $sasContent, (New-Object System.Text.UTF8Encoding($false)))

            $result = Invoke-StatExe -FilePath $sasPath -ArgumentList "-batch","-nosplash","-sysin",$tempSas
            if ($result.StdOut) { Write-Host $result.StdOut }
            if ($result.ExitCode -ne 0 -and $result.StdErr) { Write-Host $result.StdErr -ForegroundColor Red }
        }
        finally {
            # Always clean up the temp file, even on failure/interrupt.
            Remove-Item $tempSas -ErrorAction SilentlyContinue
        }
    }
    
    "read-log" {
        $logPath = $Args[0]
        if (-not (Test-Path $logPath)) {
            Write-Error "$(if ($script:isZH) { '日志文件不存在' } else { 'Log file not found' }): $logPath"
            exit 1
        }
        
        Get-Content $logPath
    }
}
