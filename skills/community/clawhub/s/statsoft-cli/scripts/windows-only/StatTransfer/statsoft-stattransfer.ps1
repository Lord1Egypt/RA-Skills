# statsoft-stattransfer.ps1 — StatTransfer CLI 包装器
#
# 用法:
#   statsoft-stattransfer version                              # 显示版本
#   statsoft-stattransfer formats                              # 列出支持格式
#   statsoft-stattransfer run <input> <output> [options]        # 单文件转换
#   statsoft-stattransfer batch <input_pattern> <output_dir>    # 批量转换
#
# 示例:
#   statsoft-stattransfer run data.sav data.csv
#   statsoft-stattransfer run data.spss data.dta
#   statsoft-stattransfer batch "C:\data\*.sav" "C:\output\"
#
# 支持格式: SAS, SPSS, Stata, R, S-Plus, SigmaPlot, Excel, CSV, ASCII, ODBC, MATLAB, etc.

param(
    [Parameter(Position=0)]
    [ValidateSet("version", "formats", "run", "batch")]
    [string]$Command,

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,

    [string]$LogFile
)

# 读取配置
$configPath = "$PSScriptRoot\..\config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "[CN] 配置文件不存在: $configPath。请先配置 StatTransfer"
    Write-Error "[EN] Config file not found: $configPath. Please configure StatTransfer first"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$stExePath = $config.StatTransfer.Path

if (-not (Test-Path $stExePath)) {
    Write-Error "[CN] StatTransfer 可执行文件不存在: $stExePath"
    Write-Error "[EN] StatTransfer executable not found: $stExePath"
    exit 1
}

# 安全路径验证 - 已知合法父目录白名单
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
    Write-Error "[CN] 路径安全验证失败: $stExePath 不在允许的安装目录列表中"
    Write-Error "[EN] Path security validation failed: $stExePath is not in allowed installation directories"
    exit 1
}

switch ($Command) {
    "version" {
        Write-Host "[CN] === StatTransfer 版本信息 ===" -ForegroundColor Cyan
        Write-Host "[EN] === StatTransfer Version Info ===" -ForegroundColor Cyan
        & $stExePath --version 2>&1
        Write-Host ""
        Write-Host "[CN] 配置路径: $($config.StatTransfer.Path)" -ForegroundColor Gray
        Write-Host "[EN] Config path: $($config.StatTransfer.Path)" -ForegroundColor Gray
        Write-Host "[CN] 配置版本: $($config.StatTransfer.Version)" -ForegroundColor Gray
        Write-Host "[EN] Config version: $($config.StatTransfer.Version)" -ForegroundColor Gray
    }

    "formats" {
        Write-Host "[CN] === StatTransfer 支持的数据格式 ===" -ForegroundColor Cyan
        Write-Host "[EN] === Supported Data Formats ===" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "[CN] 统计软件格式:" -ForegroundColor Yellow
        Write-Host "[EN] Statistical software formats:" -ForegroundColor Yellow
        Write-Host "  .sav       SPSS 数据文件" -ForegroundColor White
        Write-Host "  .dta       Stata 数据文件 (v4-16)" -ForegroundColor White
        Write-Host "  .sas7bdat  SAS 数据文件" -ForegroundColor White
        Write-Host "  .xpt       SAS 传输文件" -ForegroundColor White
        Write-Host "  .RData     R 数据文件" -ForegroundColor White
        Write-Host "  .sdd       SigmaPlot 文件" -ForegroundColor White
        Write-Host "  .mtp       Minitab 文件" -ForegroundColor White
        Write-Host "  .jmp       JMP 文件" -ForegroundColor White
        Write-Host "  .dbf       dBase 文件" -ForegroundColor White
        Write-Host "  .mdb/.accdb Microsoft Access 文件" -ForegroundColor White
        Write-Host ""
        Write-Host "[CN] 通用数据格式:" -ForegroundColor Yellow
        Write-Host "[EN] Common data formats:" -ForegroundColor Yellow
        Write-Host "  .csv       CSV 文件 (UTF-8, 带逗号分隔) / CSV file (UTF-8, comma-delimited)" -ForegroundColor White
        Write-Host "  .tsv       TSV 文件 (Tab 分隔)" -ForegroundColor White
        Write-Host "  .txt       ASCII 固定宽度文件" -ForegroundColor White
        Write-Host "  .xlsx      Excel 工作簿" -ForegroundColor White
        Write-Host "  .xls       Excel 97-2003 文件" -ForegroundColor White
        Write-Host ""
        Write-Host "[CN] 数据库格式:" -ForegroundColor Yellow
        Write-Host "[EN] Database formats:" -ForegroundColor Yellow
        Write-Host "  ODBC       [CN] 通过 ODBC 连接任意数据库 / [EN] Connect to any database via ODBC" -ForegroundColor White
        Write-Host ""
        Write-Host "[CN] 用法: statsoft-stattransfer run <输入文件> <输出文件>" -ForegroundColor Cyan
        Write-Host "[EN] Usage: statsoft-stattransfer run <input_file> <output_file>" -ForegroundColor Cyan
    }

    "run" {
        if ($Args.Count -lt 2) {
            Write-Error "[CN] 用法: statsoft-stattransfer run <输入文件> <输出文件>"
            Write-Error "[EN] Usage: statsoft-stattransfer run <input_file> <output_file>"
            exit 1
        }

        $inputFile = $Args[0]
        $outputFile = $Args[1]
        $extraArgs = @()
        for ($i = 2; $i -lt $Args.Count; $i++) {
            $extraArgs += $Args[$i]
        }

        if (-not (Test-Path $inputFile)) {
            Write-Error "[CN] 输入文件不存在: $inputFile"
            Write-Error "[EN] Input file not found: $inputFile"
            exit 1
        }

        # 安全检查 - 输入文件路径必须在合理目录内
        if (-not (Test-Path $outputFile -IsValid)) {
            Write-Error "[CN] 输出路径格式无效: $outputFile"
            Write-Error "[EN] Output path format invalid: $outputFile"
            exit 1
        }

        Write-Host "[CN] 统计软件数据格式转换" -ForegroundColor Cyan
        Write-Host "[EN] StatTransfer data format conversion" -ForegroundColor Cyan
        Write-Host "  输入 / Input: $inputFile" -ForegroundColor White
        Write-Host "  输出 / Output: $outputFile" -ForegroundColor White

        # 创建输出目录（如果不存在）
        $outputDir = Split-Path $outputFile -Parent
        if ($outputDir -and (-not (Test-Path $outputDir))) {
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }

        # 构建命令
        $cmdArgs = @($inputFile, $outputFile) + $extraArgs

        if ($LogFile) {
            Write-Host "  日志 / Log: $LogFile" -ForegroundColor Gray
        }

        Write-Host ""
        Write-Host "[CN] 执行 StatTransfer..." -ForegroundColor Yellow
        Write-Host "[EN] Executing StatTransfer..." -ForegroundColor Yellow

        $startTime = Get-Date

        $process = Start-Process -FilePath $stExePath `
            -ArgumentList $cmdArgs `
            -NoNewWindow `
            -Wait `
            -PassThru `
            -RedirectStandardError (Join-Path $env:TEMP "stattransfer-stderr.txt")

        $duration = (Get-Date) - $startTime
        Write-Host ""
        Write-Host "[CN] 完成 (耗时: $($duration.TotalSeconds.ToString('F1'))秒)" -ForegroundColor Green
        Write-Host "[EN] Done (duration: $($duration.TotalSeconds.ToString('F1'))s)" -ForegroundColor Green
        Write-Host "退出码 / Exit code: $($process.ExitCode)" -ForegroundColor Gray

        if ($process.ExitCode -ne 0) {
            $stderrFile = Join-Path $env:TEMP "stattransfer-stderr.txt"
            if (Test-Path $stderrFile) {
                $stderrContent = Get-Content $stderrFile -Raw
                if ($stderrContent.Trim()) {
                    Write-Host "[CN] 错误信息:" -ForegroundColor Red
                    Write-Host "[EN] Error details:" -ForegroundColor Red
                    Write-Host $stderrContent -ForegroundColor Red
                }
                Remove-Item $stderrFile -ErrorAction SilentlyContinue
            }
        }
    }

    "batch" {
        if ($Args.Count -lt 2) {
            Write-Error "[CN] 用法: statsoft-stattransfer batch <输入通配符> <输出目录>"
            Write-Error "[EN] Usage: statsoft-stattransfer batch <input_glob> <output_dir>"
            Write-Host '示例 / Example: statsoft-stattransfer batch "C:\data\*.sav" "C:\output\"'
            exit 1
        }

        $inputPattern = $Args[0]
        $outputDir = $Args[1]

        # 解析通配符目录
        $inputDir = Split-Path $inputPattern -Parent
        $inputFilter = Split-Path $inputPattern -Leaf

        if (-not (Test-Path $outputDir)) {
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }

        Write-Host "[CN] 批量转换" -ForegroundColor Cyan
        Write-Host "[EN] Batch conversion" -ForegroundColor Cyan
        Write-Host "  输入模式 / Input pattern: $inputPattern" -ForegroundColor White
        Write-Host "  输出目录 / Output directory: $outputDir" -ForegroundColor White

        $files = Get-ChildItem -Path $inputDir -Filter $inputFilter
        if ($files.Count -eq 0) {
            Write-Warning "[CN] 未找到匹配的文件: $inputPattern"
            Write-Warning "[EN] No matching files found: $inputPattern"
            exit 0
        }

        Write-Host "[CN] 找到 $($files.Count) 个文件" -ForegroundColor White
        Write-Host "[EN] Found $($files.Count) file(s)" -ForegroundColor White
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
                & $stExePath $file.FullName $outFile 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host " ✓" -ForegroundColor Green
                    $successCount++
                } else {
                    Write-Host " ✗ ExitCode: $LASTEXITCODE" -ForegroundColor Red
                    $failCount++
                }
            } catch {
                Write-Host " ✗ $($_.Exception.Message)" -ForegroundColor Red
                $failCount++
            }
        }

        Write-Host ""
        Write-Host "[CN] 结果: $successCount 成功, $failCount 失败" -ForegroundColor White
        Write-Host "[EN] Result: $successCount succeeded, $failCount failed" -ForegroundColor White
    }
}
