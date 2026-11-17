# statsoft-stata.ps1 — STATA EXECUTION wrapper (NOT a setup/detection tool).
# Mirrors statsoft-sas.ps1: this script INVOKES the third-party Stata binary and
# CREATES temporary/log files. It does NOT modify config.json or environment variables.
#
# Commands:
#   run <do_file> [-LogFile <name>]  EXECUTES Stata on the given do-file (.do) in batch
#                                    mode (/e do); Stata writes a .log in the current
#                                    directory. Requires explicit authorization (default-deny).
#   data-info <dta_file>             EXECUTES Stata (use ... clear; describe) on the
#                                    USER-SUPPLIED .dta via a temporary .do file (auto-deleted).
#                                    Requires the same authorization gate as `run`.
#   read-log <log_path>              Read-only: prints an existing Stata log. No execution.
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
        $prompt = if ($script:isZH) { "确认运行 Stata？该操作将执行第三方外部二进制 (y/N)" } else { "Confirm running Stata? This executes a third-party external binary (y/N)" }
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

# Headless launcher (no GUI popup) — single enforcement point for the skill default.
$__d = $PSScriptRoot
while ($__d -and -not (Test-Path (Join-Path $__d "common/invoke_hidden.ps1"))) {
    $__p = Split-Path $__d -Parent; if ($__p -eq $__d) { break }; $__d = $__p
}
. (Join-Path $__d "common/invoke_hidden.ps1")

# 读取配置
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (-not (Test-Path $configPath)) {
    Write-Error "$(if ($script:isZH) { '配置文件不存在' } else { 'Config file not found' }): $configPath"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$stataPath = $config.STATA.Path

if (-not (Test-Path $stataPath)) {
    Write-Error "$(if ($script:isZH) { 'Stata 可执行文件不存在' } else { 'Stata executable not found' }): $stataPath"
    exit 1
}

switch ($Command) {
    "run" {
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow
            exit 1
        }
        $doFile = $Args[0]
        if (-not (Test-Path $doFile)) {
            Write-Error "$(if ($script:isZH) { 'Stata do 文件不存在' } else { 'Stata do-file not found' }): $doFile"
            exit 1
        }

        $logPath = Resolve-SafeLogPath -Requested $LogFile -DefaultName "stata-log.log"
        Write-Lang "执行 Stata do 文件: $doFile" "Executing Stata do-file: $doFile" -Color Cyan
        Write-Lang "日志输出（Stata 自动写入 do 文件同目录的同名 .log，执行后自动展示）" "Log output (Stata writes a same-basename .log next to the do-file; shown automatically after execution)" -Color Gray

        # Stata batch mode: /e do <file> runs the do-file then exits.
        # Launched hidden (no GUI popup). Stata writes <dofile>.log in the process
        # WORKING DIRECTORY (not next to the do-file, and /e takes no log argument),
        # so we set the working directory to the do-file's folder: the log then
        # lands beside the do-file and is auto-displayed below.
        $doDir = Split-Path -Parent (Resolve-Path $doFile).Path
        $result = Invoke-StatExe -FilePath $stataPath -ArgumentList "/e","do",$doFile -WorkingDirectory $doDir

        if ($result.ExitCode -eq 0) {
            Write-Lang "Stata 执行完成" "Stata execution complete" -Color Green
        } else {
            Write-Lang-Warning "Stata 退出码: $($result.ExitCode)" "Stata exit code: $($result.ExitCode)"
            if ($result.StdErr) { Write-Host $result.StdErr -ForegroundColor Red }
        }

        # Surface the batch log so hidden execution still yields visible output.
        $autoLog = $doFile -replace '\.do$', '.log'
        if (Test-Path $autoLog) {
            Write-Lang "--- Stata 日志 ($autoLog) ---" "--- Stata log ($autoLog) ---" -Color Gray
            Get-Content $autoLog
        } else {
            Write-Lang-Warning "未找到 Stata 批处理日志: $autoLog" "Stata batch log not found: $autoLog"
        }
    }

    "data-info" {
        # data-info EXECUTES the Stata binary and writes a temporary .do file, so it
        # is gated by the same default-deny authorization as `run` (SDI-1).
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow
            exit 1
        }
        $dtaFile = $Args[0]
        if (-not (Test-Path $dtaFile)) {
            Write-Error "$(if ($script:isZH) { 'Stata 数据文件不存在' } else { 'Stata data file not found' }): $dtaFile"
            exit 1
        }

        $tempDo = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.do'
        Write-Lang "执行 Stata（describe），将创建临时文件并在结束后删除" "Executing Stata (describe); a temporary file is created and deleted afterward." -Color Cyan
        try {
            # Inspect the USER-SUPPLIED .dta file (not a hardcoded dataset).
            $safeFile = $dtaFile.Replace('\', '/')
            # Open an explicit log so output is captured even when the window is hidden.
            $tempLog = $tempDo -replace '\.do$', '.log'
            $doContent = @"
log using "$tempLog", replace text
use "$safeFile", clear
describe
log close
"@
            # Write WITHOUT a UTF-8 BOM: Stata treats the BOM as part of the first
            # command and the `log using` line silently fails (no output captured).
            [System.IO.File]::WriteAllText($tempDo, $doContent, (New-Object System.Text.UTF8Encoding($false)))

            $result = Invoke-StatExe -FilePath $stataPath -ArgumentList "/e","do",$tempDo
            if (Test-Path $tempLog) {
                Get-Content $tempLog
                Remove-Item $tempLog -Force -ErrorAction SilentlyContinue
            } elseif ($result.StdOut) {
                Write-Host $result.StdOut
            }
            if ($result.ExitCode -ne 0 -and $result.StdErr) {
                Write-Host $result.StdErr -ForegroundColor Red
            }
        }
        finally {
            # Always clean up the temp file, even on failure/interrupt.
            Remove-Item $tempDo -ErrorAction SilentlyContinue
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
