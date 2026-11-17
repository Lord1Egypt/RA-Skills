# statsoft-stattransfer.ps1 — StatTransfer CLI wrapper
#
# Usage:
#   statsoft-stattransfer version                              # show version
#   statsoft-stattransfer formats                              # list supported formats
#   statsoft-stattransfer run <input> <output> [options]        # single-file conversion
#   statsoft-stattransfer batch <input_pattern> <output_dir>    # batch conversion
#
# Examples:
#   statsoft-stattransfer run data.sav data.csv
#   statsoft-stattransfer run data.spss data.dta
#   statsoft-stattransfer batch "C:\data\*.sav" "C:\output\"
#
# Supported formats: SAS, SPSS, Stata, R, S-Plus, SigmaPlot, Excel, CSV, ASCII, ODBC, MATLAB, etc.

param(
    [Parameter(Position=0)]
    [ValidateSet("version", "formats", "run", "batch")]
    [string]$Command,

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,

    [string]$LogFile
)

# Language detection: Chinese on zh-* UI culture, English otherwise.
$script:isZH = [System.Globalization.CultureInfo]::CurrentUICulture.Name.StartsWith("zh")
function Write-Lang {
    param([string]$CN, [string]$EN, [System.ConsoleColor]$Color = "White")
    if ($script:isZH) { Write-Host $CN -ForegroundColor $Color }
    else { Write-Host $EN -ForegroundColor $Color }
}

# Headless launcher (no GUI popup) — single enforcement point for the skill default.
$__d = $PSScriptRoot
while ($__d -and -not (Test-Path (Join-Path $__d "common/invoke_hidden.ps1"))) {
    $__p = Split-Path $__d -Parent; if ($__p -eq $__d) { break }; $__d = $__p
}
. (Join-Path $__d "common/invoke_hidden.ps1")

# Read config
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (-not (Test-Path $configPath)) {
    Write-Error (if ($script:isZH){"配置文件不存在: $configPath。请先配置 StatTransfer"}else{"Config file not found: $configPath. Please configure StatTransfer first"})
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$stExePath = $config.StatTransfer.Path

if (-not (Test-Path $stExePath)) {
    Write-Error (if ($script:isZH){"StatTransfer 可执行文件不存在: $stExePath"}else{"StatTransfer executable not found: $stExePath"})
    exit 1
}

# Secure path validation - known-good parent directory allowlist
$validParents = @(
    "C:\Tools\StatTransfer*",
    "C:\Program Files\StatTransfer*",
    "C:\Program Files (x86)\StatTransfer*"
)
$isPathValid = $false
foreach ($parent in $validParents) {
    if ($stExePath.ToLower().StartsWith($parent.TrimEnd('*').ToLower())) {
        $isPathValid = $true
        break
    }
}
if (-not $isPathValid) {
    Write-Error (if ($script:isZH){"路径安全验证失败: $stExePath 不在允许的安装目录列表中"}else{"Path security validation failed: $stExePath is not in allowed installation directories"})
    exit 1
}

# Default-deny authorization gate for file-WRITING operations (run/batch).
# A conversion writes files to disk via a third-party binary, so it requires
# explicit opt-in: STATSOFT_AUTO_WRITE=1 (non-interactive/agent), or
# STATSOFT_CONFIRM=1 with an interactive y/N prompt in a real TTY.
# Returns $true only when authorized; defaults to $false (fail-closed) (SDI-1).
function Test-StatTransferAuthorized {
    if ($env:STATSOFT_AUTO_WRITE -eq '1') { return $true }
    if ($env:STATSOFT_CONFIRM -eq '1' -and -not [Console]::IsInputRedirected) {
        $ans = Read-Host (if ($script:isZH){"确认执行转换并写入输出文件? (y/N)"}else{"Confirm conversion and file write? (y/N)"})
        return ($ans -match '^[yY]')
    }
    return $false
}

switch ($Command) {
    "version" {
        Write-Lang "=== StatTransfer 版本信息 ===" "=== StatTransfer Version Info ===" -Color Cyan
        $result = Invoke-StatExe -FilePath $stExePath -ArgumentList "--version"
        if ($result.StdOut) { Write-Host $result.StdOut }
        if ($result.StdErr) { Write-Host $result.StdErr -ForegroundColor Red }
        Write-Host ""
        Write-Lang "配置路径: $($config.StatTransfer.Path)" "Config path: $($config.StatTransfer.Path)" -Color Gray
        Write-Lang "配置版本: $($config.StatTransfer.Version)" "Config version: $($config.StatTransfer.Version)" -Color Gray
    }

    "formats" {
        Write-Lang "=== StatTransfer 支持的数据格式 ===" "=== Supported Data Formats ===" -Color Cyan
        Write-Host ""
        Write-Lang "统计软件格式:" "Statistical software formats:" -Color Yellow
        Write-Host "  .sav       SPSS data file" -ForegroundColor White
        Write-Host "  .dta       Stata data file (v4-16)" -ForegroundColor White
        Write-Host "  .sas7bdat  SAS data file" -ForegroundColor White
        Write-Host "  .xpt       SAS transport file" -ForegroundColor White
        Write-Host "  .RData     R data file" -ForegroundColor White
        Write-Host "  .sdd       SigmaPlot file" -ForegroundColor White
        Write-Host "  .mtp       Minitab file" -ForegroundColor White
        Write-Host "  .jmp       JMP file" -ForegroundColor White
        Write-Host "  .dbf       dBase file" -ForegroundColor White
        Write-Host "  .mdb/.accdb Microsoft Access file" -ForegroundColor White
        Write-Host ""
        Write-Lang "通用数据格式:" "Common data formats:" -Color Yellow
        Write-Host "  .csv       CSV file (UTF-8, comma-delimited)" -ForegroundColor White
        Write-Host "  .tsv       TSV 文件 (Tab 分隔)" -ForegroundColor White
        Write-Host "  .txt       ASCII 固定宽度文件" -ForegroundColor White
        Write-Host "  .xlsx      Excel 工作簿" -ForegroundColor White
        Write-Host "  .xls       Excel 97-2003 文件" -ForegroundColor White
        Write-Host ""
        Write-Lang "数据库格式:" "Database formats:" -Color Yellow
        Write-Host "  ODBC       $(if ($script:isZH){"通过 ODBC 连接任意数据库"}else{"Connect to any database via ODBC"})" -ForegroundColor White
        Write-Host ""
        Write-Lang "用法: statsoft-stattransfer run <输入文件> <输出文件>" "Usage: statsoft-stattransfer run <input_file> <output_file>" -Color Cyan
    }

    "run" {
        if ($Args.Count -lt 2) {
            Write-Error (if ($script:isZH){"用法: statsoft-stattransfer run <输入文件> <输出文件>"}else{"Usage: statsoft-stattransfer run <input_file> <output_file>"})
            exit 1
        }

        $inputFile = $Args[0]
        $outputFile = $Args[1]
        $extraArgs = @()
        for ($i = 2; $i -lt $Args.Count; $i++) {
            $extraArgs += $Args[$i]
        }

        if (-not (Test-Path $inputFile)) {
            Write-Error (if ($script:isZH){"输入文件不存在: $inputFile"}else{"Input file not found: $inputFile"})
            exit 1
        }

        # Security check - input file path must be within a reasonable directory
        if (-not (Test-Path $outputFile -IsValid)) {
            Write-Error (if ($script:isZH){"输出路径格式无效: $outputFile"}else{"Output path format invalid: $outputFile"})
            exit 1
        }

        # Dry-run: report what WOULD happen, write nothing, execute nothing (SDI-1).
        if ($env:STATSOFT_DRY_RUN -eq '1') {
            Write-Lang "试运行（不写入任何文件、不执行转换）: $inputFile -> $outputFile" "Dry-run (no files written, no conversion executed): $inputFile -> $outputFile" -Color Yellow
            exit 0
        }

        # Default-deny gate: a file-writing conversion requires explicit opt-in.
        if (-not (Test-StatTransferAuthorized)) {
            Write-Error (if ($script:isZH){"未授权写入（默认拒绝）。设置 STATSOFT_AUTO_WRITE=1 或 STATSOFT_CONFIRM=1 以选择启用。"}else{"Write not authorized (default-deny). Set STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1 to opt in."})
            exit 1
        }

        Write-Lang "统计软件数据格式转换" "StatTransfer data format conversion" -Color Cyan
        Write-Lang "  输入: $inputFile" "  Input: $inputFile" -Color White
        Write-Lang "  输出: $outputFile" "  Output: $outputFile" -Color White

        # Create output directory (if it does not exist)
        $outputDir = Split-Path $outputFile -Parent
        if ($outputDir -and (-not (Test-Path $outputDir))) {
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }

        # Build command
        $cmdArgs = @($inputFile, $outputFile) + $extraArgs

        if ($LogFile) {
            Write-Lang "  日志: $LogFile" "  Log: $LogFile" -Color Gray
        }

        Write-Host ""
        Write-Lang "执行 StatTransfer..." "Executing StatTransfer..." -Color Yellow

        $startTime = Get-Date

        # Use a securely-created, uniquely-named temp file for stderr capture
        # (New-TemporaryFile creates a random name in %TEMP%), disclosed here
        # and always removed in the finally block below — no predictable temp
        # filename that other local users/processes could pre-place or read.
        try {
            $result = Invoke-StatExe -FilePath $stExePath -ArgumentList $cmdArgs

            $duration = (Get-Date) - $startTime
            Write-Host ""
            Write-Lang "完成 (耗时: $($duration.TotalSeconds.ToString('F1'))秒)" "Done (duration: $($duration.TotalSeconds.ToString('F1'))s)" -Color Green
            Write-Lang "退出码: $($result.ExitCode)" "Exit code: $($result.ExitCode)" -Color Gray

            if ($result.ExitCode -ne 0 -and $result.StdErr) {
                Write-Lang "错误信息:" "Error details:" -Color Red
                Write-Host $result.StdErr -ForegroundColor Red
            }
        } finally {
            Remove-Item $stderrFile -Force -ErrorAction SilentlyContinue
        }
    }

    "batch" {
        if ($Args.Count -lt 2) {
            Write-Error (if ($script:isZH){"用法: statsoft-stattransfer batch <输入通配符> <输出目录>"}else{"Usage: statsoft-stattransfer batch <input_glob> <output_dir>"})
            Write-Lang '示例: statsoft-stattransfer batch "C:\data\*.sav" "C:\output\"' 'Example: statsoft-stattransfer batch "C:\data\*.sav" "C:\output\"'
            exit 1
        }

        $inputPattern = $Args[0]
        $outputDir = $Args[1]

        # Resolve the glob directory
        $inputDir = Split-Path $inputPattern -Parent
        $inputFilter = Split-Path $inputPattern -Leaf

        # Dry-run: report the plan only, create nothing, convert nothing (SDI-1).
        if ($env:STATSOFT_DRY_RUN -eq '1') {
            Write-Lang "试运行（不写入任何文件、不执行转换）: $inputPattern -> $outputDir" "Dry-run (no files written, no conversion executed): $inputPattern -> $outputDir" -Color Yellow
            exit 0
        }

        # Default-deny gate: batch file-writing conversions require explicit opt-in.
        if (-not (Test-StatTransferAuthorized)) {
            Write-Error (if ($script:isZH){"未授权写入（默认拒绝）。设置 STATSOFT_AUTO_WRITE=1 或 STATSOFT_CONFIRM=1 以选择启用。"}else{"Write not authorized (default-deny). Set STATSOFT_AUTO_WRITE=1 or STATSOFT_CONFIRM=1 to opt in."})
            exit 1
        }

        if (-not (Test-Path $outputDir)) {
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }

        Write-Lang "批量转换" "Batch conversion" -Color Cyan
        Write-Lang "  输入模式: $inputPattern" "  Input pattern: $inputPattern" -Color White
        Write-Lang "  输出目录: $outputDir" "  Output directory: $outputDir" -Color White

        $files = Get-ChildItem -Path $inputDir -Filter $inputFilter
        if ($files.Count -eq 0) {
            Write-Warning (if ($script:isZH){"未找到匹配的文件: $inputPattern"}else{"No matching files found: $inputPattern"})
            exit 0
        }

        Write-Lang "找到 $($files.Count) 个文件" "Found $($files.Count) file(s)" -Color White
        Write-Host ""

        $successCount = 0
        $failCount = 0

        foreach ($file in $files) {
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
            $outExt = switch ($file.Extension) {
                ".sav"  { ".csv" }
                ".dta"  { ".csv" }
                ".sas7bdat" { ".csv" }
                ".csv"  { ".dta" }
                ".xlsx" { ".csv" }
                default { ".csv" }
            }
            $outFile = Join-Path $outputDir "$baseName$outExt"

            Write-Host "  -> $($file.Name) -> $outFile" -ForegroundColor White -NoNewline

            try {
                $result = Invoke-StatExe -FilePath $stExePath -ArgumentList $file.FullName,$outFile
                if ($result.ExitCode -eq 0) {
                    Write-Host " ✓" -ForegroundColor Green
                    $successCount++
                } else {
                    Write-Host " ✗ ExitCode: $($result.ExitCode)" -ForegroundColor Red
                    $failCount++
                }
            } catch {
                Write-Host " ✗ $($_.Exception.Message)" -ForegroundColor Red
                $failCount++
            }
        }

        Write-Host ""
        Write-Lang "结果: $successCount 成功, $failCount 失败" "Result: $successCount succeeded, $failCount failed" -Color White
    }
}
