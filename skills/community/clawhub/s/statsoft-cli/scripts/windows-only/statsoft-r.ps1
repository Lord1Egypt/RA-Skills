# statsoft-r.ps1 — R CLI 包装器（高级模式）
# 用法:
#   statsoft-r run <r_file> [--log-file <path>]
#   statsoft-r install <package> [--repo <url>]
#   statsoft-r data-info <data_file> [--vars var1 var2]
#   statsoft-r read-log <log_path>
# ⚠️ SETUP/wrapper tool: runs R, installs packages (CRAN, explicit y/N), and persists config. NOT a read-only scanner.

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
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (-not (Test-Path $configPath)) {
    Write-Error "$(if ($script:isZH) { '配置文件不存在' } else { 'Config file not found' }): $configPath"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
# Resolve R path: prefer the configured R.Path; fall back to auto-detection;
# otherwise fail with a clear, friendly message (never a raw null-binding error).
$rPath = $null
if ($config.R -and $config.R.Path -and ($config.R.Path.Trim()) -ne "") {
    $rPath = $config.R.Path
} else {
    $detected = Get-Command Rscript -ErrorAction SilentlyContinue
    if ($detected) { $rPath = $detected.Source }
}

if (-not $rPath -or -not (Test-Path $rPath)) {
    Write-Error "$(if ($script:isZH) { '未配置或未检测到 Rscript.exe，请先运行 R 的检测/配置（setup_r）' } else { 'Rscript.exe not configured or detected; run R setup (setup_r) first' })"
    exit 1
}

function Test-UserAuthorizedToRun {
    # Execution/install authorization gate for R (external run, network package
    # install) — FAIL-CLOSED (default deny).
    # Proceed ONLY when an explicit opt-in is present:
    #   * STATSOFT_AUTO_WRITE=1                          -> non-interactive/agent opt-in
    #   * STATSOFT_CONFIRM=1 AND a real TTY AND user answers y -> interactive confirm
    $autoWrite = $env:STATSOFT_AUTO_WRITE -eq '1'
    $confirm = $env:STATSOFT_CONFIRM -eq '1'
    if ($autoWrite) { return $true }
    if ($confirm -and -not [Console]::IsInputRedirected) {
        $ans = Read-Host (if ($script:isZH) { "确认执行？该操作将运行第三方外部二进制 (y/N)" } else { "Confirm execution? This runs a third-party external binary (y/N)" })
        return ($ans -match '^[yY]')
    }
    return $false
}

switch ($Command) {
    "run" {
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消执行（未确认）" "Execution cancelled (not confirmed)." -Color Yellow
            return
        }
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

        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消安装" "Installation cancelled" -Color Yellow
            return
        }

        # SECURITY (B15): pass the package name + repo as command-line ARGUMENTS
        # to a temp R script — NEVER interpolate them into an `R -e` expression,
        # which would let a crafted `$package`/`$Repo` inject arbitrary R code.
        $installScript = @"
args <- commandArgs(trailingOnly=TRUE)
pkg <- args[1]
repo <- args[2]
install.packages(pkg, repos=repo, quiet=TRUE)
"@
        $tempInstall = Join-Path ([System.IO.Path]::GetTempPath()) ("statsoft_install_" + [System.Guid]::NewGuid().ToString("N") + ".R")
        try {
            $installScript | Set-Content $tempInstall -Encoding UTF8
            & $rPath $tempInstall "$package" "$Repo" 2>&1
        } finally {
            Remove-Item $tempInstall -ErrorAction SilentlyContinue
        }

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
        if (-not (Test-UserAuthorizedToRun)) {
            Write-Lang "已取消（未确认）" "Cancelled (not confirmed)." -Color Yellow
            return
        }

        $ext = [System.IO.Path]::GetExtension($dataFile).ToLower()

        # For Stata/SPSS formats, ensure the haven package is available.
        if ($ext -eq ".dta" -or $ext -eq ".sav") {
            Write-Lang "Stata/SPSS 文件需要 haven 包" "Stata/SPSS file requires the haven package" -Color Yellow
            $havenOk = & $rPath -e "cat(require('haven', quietly=TRUE))" 2>&1 | Out-String
            if ($havenOk.Trim() -ne "TRUE") {
                Write-Lang "haven 未安装。是否从 CRAN 安装（约 1-2 分钟）?" "haven not installed. Install from CRAN (~1-2 min)?" -Color Yellow
                if (-not (Test-UserAuthorizedToRun)) {
                    Write-Lang "已跳过安装，请手动安装 haven 后重试" "Skipped. Please install haven manually and retry" -Color Yellow
                    return
                }
                $havenScript = @"
args <- commandArgs(trailingOnly=TRUE)
repo <- args[1]
install.packages('haven', repos=repo, quiet=TRUE)
"@
                $tempHaven = Join-Path ([System.IO.Path]::GetTempPath()) ("statsoft_haven_" + [System.Guid]::NewGuid().ToString("N") + ".R")
                try {
                    $havenScript | Set-Content $tempHaven -Encoding UTF8
                    & $rPath $tempHaven "$Repo" 2>&1
                } finally {
                    Remove-Item $tempHaven -ErrorAction SilentlyContinue
                }
            }
        }

        # Build a temporary R script; pass the data file path as a command-line
        # ARGUMENT (NEVER interpolate it into source) -> no R code injection.
        $readExpr = switch ($ext) {
            ".csv"  { "df <- read.csv(args[1], nrows=10)" }
            ".rds"  { "df <- readRDS(args[1])" }
            ".dta"  { "df <- haven::read_dta(args[1])" }
            ".sav"  { "df <- haven::read_sav(args[1])" }
            default { $null }
        }
        if ($null -eq $readExpr) {
            Write-Lang-Warning "不支持的文件格式: $ext" "Unsupported file format: $ext"
            return
        }
        $rScript = @"
args <- commandArgs(trailingOnly=TRUE)
$readExpr
cat('Rows:', nrow(df), '\nCols:', ncol(df), '\n')
print(names(df))
print(summary(df))
"@
        $tempR = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.R'
        Write-Lang "创建临时 R 脚本（仅本次运行，结束后删除）:" "Creating a temporary R script (used only for this run, removed afterwards):" -Color Gray
        Write-Host "  $tempR" -ForegroundColor Gray
        try {
            $rScript | Set-Content $tempR -Encoding UTF8
            & $rPath $tempR "$dataFile" 2>&1
        } finally {
            Remove-Item $tempR -ErrorAction SilentlyContinue
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
