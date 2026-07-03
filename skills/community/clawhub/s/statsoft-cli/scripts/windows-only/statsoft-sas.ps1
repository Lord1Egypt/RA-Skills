# statsoft-sas.ps1 — SAS CLI 包装器（高级模式）
# 用法:
#   statsoft-sas run <sas_file> [--log-file <path>]
#   statsoft-sas data-info <sas_file> [--vars var1 var2]
#   statsoft-sas read-log <log_path>

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

# 读取配置
$configPath = "$PSScriptRoot\..\config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "$(if ($script:isZH) { '配置文件不存在' } else { 'Config file not found' }): $configPath"
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$sasPath = $config.SAS.Path

if (-not (Test-Path $sasPath)) {
    Write-Error "$(if ($script=isZH) { 'SAS 可执行文件不存在' } else { 'SAS executable not found' }): $sasPath"
    exit 1
}

switch ($Command) {
    "run" {
        $sasFile = $Args[0]
        if (-not (Test-Path $sasFile)) {
            Write-Error "$(if ($script:isZH) { 'SAS 程序不存在' } else { 'SAS program not found' }): $sasFile"
            exit 1
        }
        
        $logPath = if ($LogFile) { $LogFile } else { Join-Path $PWD "sas-log.log" }
        $printPath = if ($LogFile) { $LogFile -replace '\.log$', '.lst' } else { Join-Path $PWD "sas-output.lst" }
        
        Write-Lang "执行 SAS 程序: $sasFile" "Executing SAS program: $sasFile" -Color Cyan
        Write-Lang "日志输出: $logPath" "Log output: $logPath" -Color Gray
        
        & $sasPath -batch -nosplash -sysin $sasFile -log $logPath -print $printPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Lang "SAS 执行完成" "SAS execution complete" -Color Green
        } else {
            Write-Lang-Warning "SAS 退出码: $LASTEXITCODE" "SAS exit code: $LASTEXITCODE"
        }
    }
    
    "data-info" {
        $sasFile = $Args[0]
        if (-not (Test-Path $sasFile)) {
            Write-Error "$(if ($script:isZH) { 'SAS 程序不存在' } else { 'SAS program not found' }): $sasFile"
            exit 1
        }
        
        $tempSas = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.sas'
        @"
proc contents data=sashelp.class;
run;
"@ | Set-Content $tempSas -Encoding UTF8
        
        & $sasPath -batch -nosplash -sysin $tempSas 2>&1
        Remove-Item $tempSas -ErrorAction SilentlyContinue
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
