# statsoft-r.ps1 — R CLI 包装器（高级模式）
# 用法:
#   statsoft-r run <r_file> [--log-file <path>]
#   statsoft-r install <package> [--repo <url>]
#   statsoft-r data-info <data_file> [--vars var1 var2]
#   statsoft-r read-log <log_path>

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "install", "data-info", "read-log")]
    [string]$Command,
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,
    
    [string]$LogFile,
    [string]$Repo = "https://cran.r-project.org"
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

# 读取配置
$configPath = "$PSScriptRoot\..\config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "$(if ($script:isZH) { '配置文件不存在' } else { 'Config file not found' }): $configPath"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$rPath = $config.R.Path

if (-not (Test-Path $rPath)) {
    Write-Error "$(if ($script:isZH) { 'Rscript.exe 不存在' } else { 'Rscript.exe not found' }): $rPath"
    exit 1
}

switch ($Command) {
    "run" {
        $rFile = $Args[0]
        if (-not (Test-Path $rFile)) {
            Write-Error "$(if ($script:isZH) { 'R 脚本不存在' } else { 'R script not found' }): $rFile"
            exit 1
        }
        
        $logPath = if ($LogFile) { $LogFile } else { Join-Path $PWD "r-log.txt" }
        Write-Lang "执行 R 脚本: $rFile" "Executing R script: $rFile" -Color Cyan
        Write-Lang "日志输出: $logPath" "Log output: $logPath" -Color Gray
        
        & $rPath $rFile 2>&1 | Tee-Object -FilePath $logPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Lang "R 执行完成" "R execution complete" -Color Green
        } else {
            Write-Lang-Warning "R 退出码: $LASTEXITCODE" "R exit code: $LASTEXITCODE"
        }
    }
    
    "install" {
        $package = $Args[0]
        Write-Lang "准备安装 R 包: $package" "Preparing to install R package: $package" -Color Cyan
        Write-Lang "来源: $Repo" "Repository: $Repo" -Color Gray

        $confirm = "N"
        try {
            $confirm = Read-Host "$(if ($script:isZH) { '确认安装' } else { 'Confirm install' })? (y/N)"
        } catch {
            Write-Lang "非交互模式，默认跳过安装" "Non-interactive mode, defaulting to skip" -Color Yellow
        }

        if ($confirm -ne 'y' -and $confirm -ne 'Y') {
            Write-Lang "已取消安装" "Installation cancelled" -Color Yellow
            return
        }

        & $rPath -e "install.packages('$package', repos='$Repo', quiet=TRUE)" 2>&1

        if ($LASTEXITCODE -eq 0) {
            Write-Lang "包 '$package' 安装完成" "Package '$package' installed successfully" -Color Green
        } else {
            Write-Lang-Warning "CRAN 安装失败" "CRAN install failed"
        }
    }
    
    "data-info" {
        $dataFile = $Args[0]
        if (-not (Test-Path $dataFile)) {
            Write-Error "$(if ($script:isZH) { '数据文件不存在' } else { 'Data file not found' }): $dataFile"
            exit 1
        }

        $ext = [System.IO.Path]::GetExtension($dataFile).ToLower()

        switch ($ext) {
            ".csv" {
                & $rPath -e "df <- read.csv('$dataFile', nrows=10); cat('Rows:', nrow(df), '\nCols:', ncol(df), '\n'); print(names(df)); print(summary(df))" 2>&1
            }
            ".rds" {
                & $rPath -e "df <- readRDS('$dataFile'); cat('Dimensions:', dim(df), '\n'); print(names(df)); print(head(df))" 2>&1
            }
            ".dta" {
                Write-Lang "Stata (.dta) 文件需要 haven 包" "Stata (.dta) file requires haven package" -Color Yellow
                & $rPath -e "if (!require('haven', quietly=TRUE)) install.packages('haven'); df <- haven::read_dta('$dataFile'); cat('Rows:', nrow(df), '\nCols:', ncol(df), '\n'); print(names(df)); print(summary(df))" 2>&1
            }
            ".sav" {
                Write-Lang "SPSS (.sav) 文件需要 haven 包" "SPSS (.sav) file requires haven package" -Color Yellow
                & $rPath -e "if (!require('haven', quietly=TRUE)) install.packages('haven'); df <- haven::read_sav('$dataFile'); cat('Rows:', nrow(df), '\nCols:', ncol(df), '\n'); print(names(df)); print(summary(df))" 2>&1
            }
            default {
                Write-Lang-Warning "不支持的文件格式: $ext" "Unsupported file format: $ext"
            }
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
