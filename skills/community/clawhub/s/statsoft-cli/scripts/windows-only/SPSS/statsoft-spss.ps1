# statsoft-spss.ps1 — SPSS CLI wrapper
# Invocation priority:
#   1) stats.com console build -> -production silent -nologo (preferred, no splash)
#   2) SPSS bundled Python -> StartSPSS() + Submit() + StopSPSS (fallback, no splash)
#   3) stats.exe -> -production silent -nologo (last resort, may show splash)

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "run-batch", "data-info", "version", "check-syntax")]
    [string]$Command,

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

# Language detection: Chinese on zh-* UI culture, English otherwise.
$script:isZH = [System.Globalization.CultureInfo]::CurrentUICulture.Name.StartsWith("zh")
function Write-Lang {
    param([string]$CN, [string]$EN, [System.ConsoleColor]$Color = "White")
    if ($script:isZH) { Write-Host $CN -ForegroundColor $Color }
    else { Write-Host $EN -ForegroundColor $Color }
}

$ErrorActionPreference = "Stop"

# ============================================================
# Initialization
# ============================================================
$scriptDir  = Split-Path $MyInvocation.MyCommand.Path -Parent
$helperPy   = Join-Path $scriptDir "spss_helper.py"

        # Read config
$configPath = Join-Path $scriptDir "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $scriptDir "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $scriptDir "..\..\config.json" }
$statsPython = $null
$statsExe = $null
$statsCom = $null

if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        if ($config."SPSS Statistics" -and $config."SPSS Statistics".Path) {
            $p = $config."SPSS Statistics".Path  # 指向 stats.exe
            $baseDir = Split-Path $p -Parent
            # Python (same dir as stats.exe)
            $pythonCand = Join-Path $baseDir "Python3\python.exe"
            if (Test-Path $pythonCand) { $statsPython = $pythonCand }
            # stats.com (same dir as stats.exe)
            $comCand = Join-Path $baseDir "stats.com"
            if (Test-Path $comCand) { $statsCom = $comCand }
            $statsExe = $p
        }
    } catch { }
}

# Dynamic scan
if (-not $statsPython -or -not $statsCom) {
    # Fixed system drives only (C:, D:) — no full host inventory of mounted volumes
    $drives = @("C", "D")
    $versions = @("26", "27", "28", "29", "30")
    $patterns = @(
        "{0}:\Program Files\IBM\SPSS\Statistics\{1}",
        "{0}:\Program Files (x86)\IBM\SPSS\Statistics\{1}",
        "{0}:\Program Files\IBM\SPSS30\Statistics\{1}",
        "{0}:\SPSS\Statistics\{1}",
        "{0}:\IBM\SPSS\Statistics\{1}"
    )
    foreach ($d in $drives) {
        if ($statsPython -and $statsCom -and $statsExe) { break }
        foreach ($v in $versions) {
            if ($statsPython -and $statsCom -and $statsExe) { break }
            foreach ($pat in $patterns) {
                $dir = $pat -f $d, $v
                if (Test-Path $dir) {
                    if (-not $statsPython) { $candPy = Join-Path $dir "Python3\python.exe"; if (Test-Path $candPy) { $statsPython = $candPy } }
                    if (-not $statsCom)  { $candCom  = Join-Path $dir "stats.com"; if (Test-Path $candCom) { $statsCom = $candCom } }
                    if (-not $statsExe)  { $candStat = Join-Path $dir "stats.exe"; if (Test-Path $candStat) { $statsExe = $candStat } }
                }
            }
        }
    }
}

if (-not $statsPython -and -not $statsCom) {
    Write-Warning (if ($script:isZH){"未检测到 SPSS"}else{"SPSS not found"}); exit 1
}

# Detection-phase disclosure gate (SDI-3 / SDI-4): binaries paths are detailed
# inventory data — revealed only when STATSOFT_REVEAL=1. Default detection
# reports only the boolean installed result (no path, no version detail).
if ($env:STATSOFT_REVEAL -eq '1') {
    if ($statsCom)   { Write-Host "stats.com: $statsCom" -ForegroundColor Cyan }
    if ($statsPython) { Write-Host "Python: $statsPython" -ForegroundColor Cyan }
    if ($statsExe)    { Write-Host "stats.exe: $statsExe" -ForegroundColor Cyan }
} else {
    $found = @()
    if ($statsCom)   { $found += "stats.com" }
    if ($statsPython) { $found += "bundled-python" }
    if ($statsExe)    { $found += "stats.exe" }
    if ($found.Count -gt 0) {
        Write-Lang "检测到 SPSS: $($found -join ', ') (set STATSOFT_REVEAL=1 to reveal paths)" "SPSS detected: $($found -join ', ') (set STATSOFT_REVEAL=1 to reveal paths)" -Color Cyan
    }
}

# ============================================================
# Preferred: stats.com console build (no splash)
# ============================================================
function Invoke-SPSSConsole {
    param( [string]$SpjFile )
    Write-Lang "`n调用 SPSS (首选: stats.com, 无闪屏)..." "Calling SPSS (preferred: stats.com, no splash)..." -Color Yellow

    if (-not $statsCom -or -not (Test-Path $statsCom)) {
        Write-Warning (if ($script:isZH){"未找到 stats.com"}else{"stats.com not found"}); return $false
    }

    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $statsCom
        $psi.Arguments = "'-production' 'silent' '-nologo' `"$SpjFile`""
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true

        $p = [System.Diagnostics.Process]::Start($psi)
        $stdout = $p.StandardOutput.ReadToEnd()
        $stderr = $p.StandardError.ReadToEnd()
        $p.WaitForExit(300000)

        if ($stdout) { Write-Host $stdout }
        if ($stderr) { Write-Warning $stderr }

        $exitCode = $p.ExitCode
        Write-Lang "退出码: $exitCode" "Exit code: $exitCode" -Color $(if ($exitCode -eq 0) {"Green"} else {"Red"})
        return ($exitCode -eq 0)
    } catch {
        Write-Error (if ($script:isZH){"执行出错: $($_.Exception.Message)"}else{"Execution error: $($_.Exception.Message)"})
        return $false
    }
}

# ============================================================
# Fallback: bundled Python (no splash)
# ============================================================
function Invoke-SPSSBuiltinPython {
    param( [string]$SpsFile )
    Write-Lang "`n调用 SPSS (备用: 内置 Python, 无闪屏)..." "Calling SPSS (backup: bundled Python, no splash)..." -Color Yellow

    if (-not $statsPython -or -not (Test-Path $statsPython)) {
        Write-Warning (if ($script:isZH){"未找到内置 Python"}else{"bundled Python not found"}); return $false
    }

    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $statsPython
        $psi.Arguments = "`"$helperPy`" run-internal `"$SpsFile`" `"$statsPython`""
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true
        $psi.EnvironmentVariables["PATH"] = (Split-Path $statsPython -Parent) + ";" + $psi.EnvironmentVariables["PATH"]

        $p = [System.Diagnostics.Process]::Start($psi)
        $stdout = $p.StandardOutput.ReadToEnd()
        $stderr = $p.StandardError.ReadToEnd()
        if (-not $p.WaitForExit(300000)) { $p.Kill() }

        if ($stdout) { Write-Host $stdout }
        if ($stderr) { Write-Warning $stderr }

        $exitCode = $p.ExitCode
        Write-Lang "退出码: $exitCode" "Exit code: $exitCode" -Color $(if ($exitCode -eq 0) {"Green"} else {"Red"})
        return ($exitCode -eq 0)
    } catch {
        Write-Error (if ($script:isZH){"执行出错: $($_.Exception.Message)"}else{"Execution error: $($_.Exception.Message)"})
        return $false
    }
}

# ============================================================
# Last resort: stats.exe (may show splash)
# ============================================================
function Invoke-SPSSExecutable {
    param( [string]$SpjFile )
    Write-Lang "`n调用 SPSS 最后备选: stats.exe (可能有闪屏)..." "Calling SPSS (last resort: stats.exe, may show splash)..." -Color Yellow

    if (-not $statsExe -or -not (Test-Path $statsExe)) {
        Write-Error (if ($script:isZH){"未找到 stats.exe"}else{"stats.exe not found"})
        return $false
    }

    $confirm = "N"
    try {
        $confirm = Read-Host (if ($script:isZH){"此方式可能出现闪屏。是否继续? (y/N)"}else{"May show splash. Continue? (y/N)"})
    } catch {
        Write-Lang "非交互模式，默认跳过" "Non-interactive mode, defaulting to skip" -Color Yellow
    }
    if ($confirm -ne 'y' -and $confirm -ne 'Y') { exit 1 }

    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $statsExe
        $psi.Arguments = "'-production' `"$SpjFile`" 'silent' '-nologo'"
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true

        $p = [System.Diagnostics.Process]::Start($psi)
        $stdout = $p.StandardOutput.ReadToEnd()
        $stderr = $p.StandardError.ReadToEnd()
        $p.WaitForExit(300000)

        if ($stdout) { Write-Host $stdout }
        if ($stderr) { Write-Warning $stderr }

        $exitCode = $p.ExitCode
        Write-Lang "退出码: $exitCode" "Exit code: $exitCode" -Color $(if ($exitCode -eq 0) {"Green"} else {"Red"})
        return ($exitCode -eq 0)
    } catch {
        Write-Error (if ($script:isZH){"执行出错: $($_.Exception.Message)"}else{"Execution error: $($_.Exception.Message)"})
        return $false
    }
}

# ============================================================
# Generate .spj file (SPSS 26+ new format)
# ============================================================
function New-SpssSpj {
    param( [string]$SpsFile, [string]$WorkDir )

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($SpsFile)
    $spjFile  = Join-Path $WorkDir "$baseName.spj"
    $spvFile  = Join-Path $WorkDir "$baseName.spv"
    # WARNING: must use forward slashes (required by SPSS Production Facility)
    $spsUrl   = ([System.IO.Path]::GetFullPath($SpsFile)) -replace '\\', '/'
    $spvUrl   = $spvFile -replace '\\', '/'

    $xml = @"
<?xml version="1.0" encoding="UTF-8"?>
<job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     print="false"
     syntaxErrorHandling="continue"
     syntaxFormat="interactive"
     unicode="true"
     xsi:schemaLocation="http://www.ibm.com/software/analytics/spss/xml/production http://www.ibm.com/software/analytics/spss/xml/production/production-1.4.xsd">
  <locale charset="UTF-8" country="CN" language="zh"/>
  <output outputFormat="viewer" outputPath="$spvUrl"/>
  <syntax syntaxPath="$spsUrl"/>
</job>
"@
    [System.IO.File]::WriteAllText($spjFile, $xml, [System.Text.Encoding]::UTF8)
    return $spjFile
}

# ============================================================
# Main dispatch
# ============================================================
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
        $ans = Read-Host (if ($script:isZH) { "确认运行 SPSS？该操作将执行第三方外部二进制 (y/N)" } else { "Confirm running SPSS? This executes a third-party external binary (y/N)" })
        return ($ans -match '^[yY]')
    }
    return $false
}

switch ($Command) {
    "run" {
        if (-not (Test-UserAuthorizedToRun)) { Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow; exit 1 }
        # ⚠️ Disclosure (TP4): this explicit run writes a TEMPORARY job file
        # <basename>.spj into the current working directory (auto-deleted after
        # the run) and a .spv analysis OUTPUT into the same directory (kept, as
        # it is the user's result). Both live in the USER's working directory,
        # never in the skill directory, and only on this authorized run.
        Write-Lang "⚠️ 将在当前工作目录写入临时作业文件 <basename>.spj（运行后自动删除）与分析输出 <basename>.spv（保留，位于用户工作目录而非技能目录）" "⚠️ Will write a temporary job file <basename>.spj (auto-deleted after run) and a .spv analysis output into the current working directory (user's dir, not the skill dir)." -Color Yellow
        $spsFile = $Args[0]
        if (-not $spsFile -or -not (Test-Path $spsFile)) {
            Write-Error (if ($script:isZH){"语法文件不存在: $spsFile"}else{"Syntax file not found"}); exit 1
        }

        $workDir = $PWD
        $spjFile = New-SpssSpj -SpsFile $spsFile -WorkDir $workDir

        # Preferred: stats.com
        $success = Invoke-SPSSConsole -SpjFile $spjFile
        if ($success) { Remove-Item $spjFile -ErrorAction SilentlyContinue; exit 0 }

        # Fallback: bundled Python
        Write-Host "" -ForegroundColor Yellow
        Write-Warning (if ($script:isZH){"stats.com 失败，尝试内置 Python..."}else{"stats.com failed. Trying Python fallback..."})
        $success = Invoke-SPSSBuiltinPython $spsFile

        if ($success) { Remove-Item $spjFile -ErrorAction SilentlyContinue; exit 0 }

        # Last resort: stats.exe
        Write-Host "" -ForegroundColor Yellow
        Write-Warning (if ($script:isZH){"Python 也失败，尝试 stats.exe..."}else{"Python also failed. Trying stats.exe..."})
        $success = Invoke-SPSSExecutable -SpjFile $spjFile

        Remove-Item $spjFile -ErrorAction SilentlyContinue
        exit [int](-not $success)
    }

    "run-batch" {
        if (-not (Test-UserAuthorizedToRun)) { Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow; exit 1 }
        # ⚠️ Disclosure (TP4): writes a TEMPORARY batch-master.sps + <basename>.spj
        # into the current working directory (both auto-deleted) and a .spv output
        # (kept) into the user's working directory — only on this authorized run.
        Write-Lang "⚠️ 批量运行将在当前工作目录写入临时文件（batch-master.sps、<basename>.spj，运行后自动删除）与 .spv 分析输出（保留，位于用户工作目录而非技能目录）" "⚠️ Batch run writes temporary files (batch-master.sps, <basename>.spj, auto-deleted) and a .spv output (kept) into the current working directory (user's dir, not the skill dir)." -Color Yellow
        if ($Args.Count -eq 0) { Write-Error (if ($script:isZH){"需提供语法文件路径"}else{"Please provide syntax file path"}); exit 1 }
        $workDir   = $PWD
        $masterSps = Join-Path $workDir "batch-master.sps"
        $lines     = @("* SPSS Batch Run", "SET PRINTBACK=ON.", "")
        foreach ($f in $Args) {
            if (-not (Test-Path $f)) { Write-Warning (if ($script:isZH){"跳过: $f"}else{"Skip: $f"}); continue }
            $lines += @("* File: $f", "INSERT FILE=`"$f`"", "")
        }
        [System.IO.File]::WriteAllText($masterSps, ($lines -join "`r`n"), [System.Text.Encoding]::UTF8)

        $spjFile = New-SpssSpj -SpsFile $masterSps -WorkDir $workDir

        # Priority chain: stats.com -> Python -> stats.exe
        $success = Invoke-SPSSConsole -SpjFile $spjFile
        if (-not $success) { $success = Invoke-SPSSBuiltinPython $masterSps }
        if (-not $success) { $success = Invoke-SPSSExecutable -SpjFile $spjFile }

        Remove-Item $spjFile -ErrorAction SilentlyContinue
        Remove-Item $masterSps -ErrorAction SilentlyContinue
        exit [int](-not $success)
    }

    "data-info" {
        $savFile = $Args[0]
        if (-not $savFile -or -not (Test-Path $savFile)) { Write-Error (if ($script:isZH){"数据文件不存在"}else{"Data file not found"}); exit 1 }
        # data-info AND version both launch an external Python interpreter (the
        # SPSS engine), so they pass the SAME default-deny execution gate as
        # run/run-batch (SDI-1/SDI-4). Every command that starts a third-party
        # binary is gated here.
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Error (if ($script:isZH){"未授权执行"}else{"Execution not authorized (default-deny). Set STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1 to opt in."})
            exit 1
        }
        $helperPy = Join-Path $scriptDir "_data_info.py"
        if (-not (Test-Path $helperPy)) { Write-Error (if ($script:isZH){"缺少辅助脚本 _data_info.py"}else{"Missing helper _data_info.py"}); exit 1 }
        # Prefer the SPSS-bundled interpreter ($statsPython) to keep execution
        # within the declared SPSS trust boundary; fall back to a resolved
        # absolute host python.exe only if the bundled one is unavailable.
        # The path is passed to the helper as a safe argv argument (no interpolation).
        # data-info MUST use the SPSS-bundled interpreter to stay within the
        # declared SPSS trust boundary; the host-python fallback is removed (SDI-1).
        $pyExe = $null
        if ($statsPython -and (Test-Path $statsPython)) {
            $pyExe = $statsPython
        }
        if (-not $pyExe) {
            Write-Error (if ($script:isZH){"未找到 SPSS 内置 Python（data-info 仅使用 SPSS 内置解释器，不允许回退到宿主 Python）"}else{"SPSS-bundled Python not found (data-info requires the SPSS-bundled interpreter; host Python fallback is disabled)"})
            exit 1
        }
        & $pyExe $helperPy $savFile
    }

    "version" {
        # version launches the SPSS-bundled Python interpreter and starts the
        # SPSS engine (third-party code execution), so it MUST pass the SAME
        # default-deny gate as run/run-batch/data-info (SDI-1/SDI-4), AND it
        # requires the verification opt-in STATSOFT_VERIFY=1 because it
        # executes the external SPSS engine for a --version query.
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Error (if ($script:isZH){"未授权执行"}else{"Execution not authorized (default-deny). Set STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1 to opt in."})
            exit 1
        }
        if ($env:STATSOFT_VERIFY -ne '1') {
            Write-Error (if ($script:isZH){"version 需要 STATSOFT_VERIFY=1 以启动第三方 SPSS 引擎进行版本查询"}else{"version requires STATSOFT_VERIFY=1 to launch the third-party SPSS engine for a version query (default-deny)."})
            exit 1
        }
        if (-not $statsPython) { Write-Error (if ($script:isZH){"未找到内置 Python"}else{"bundled Python not found"}); exit 1 }
        & $statsPython -c "import spss; spss.StartSPSS(); print(getattr(spss,'__version__','unknown')); spss.StopSPSS()"
    }

    "check-syntax" {
        $spsFile = $Args[0]
        if (-not $spsFile -or -not (Test-Path $spsFile)) { Write-Error (if ($script:isZH){"语法文件不存在"}else{"Syntax file not found"}); exit 1 }
        Get-Content $spsFile -Head 10
    }
}
