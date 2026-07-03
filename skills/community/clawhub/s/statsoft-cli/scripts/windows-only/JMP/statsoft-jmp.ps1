# statsoft-jmp.ps1 — JMP CLI 包装器（高级模式）
# 用法:
#   statsoft-jmp run <jsl_file> [--log-file <path>] [--silent]
#   statsoft-jmp data-info <jmp_file> [--vars var1 var2]
#   statsoft-jmp read-log <log_path>

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "data-info", "read-log")]
    [string]$Command,
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,
    
    [string]$LogFile,
    [switch]$Silent
)

# 读取配置
$configPath = "$PSScriptRoot\..\config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "[CN] 配置文件不存在: $configPath。请先运行 setup_jmp.ps1 / [EN] Config file not found: $configPath. Please run setup_jmp.ps1 first."
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$jmpPath = $config.JMP.Path

if (-not (Test-Path $jmpPath)) {
    Write-Error "[CN] JMP 可执行文件不存在: $jmpPath / [EN] JMP executable not found: $jmpPath"
    exit 1
}

switch ($Command) {
    "run" {
        $jslFile = $Args[0]
        if (-not (Test-Path $jslFile)) {
            Write-Error "[CN] JSL 脚本不存在: $jslFile / [EN] JSL script not found: $jslFile"
            exit 1
        }
        
        $logPath = if ($LogFile) { $LogFile } else { Join-Path $PWD "jmp-log.txt" }
        Write-Host "[CN] 执行 JMP 脚本: $jslFile" -ForegroundColor Cyan
        Write-Host "[EN] Executing JMP script: $jslFile" -ForegroundColor Cyan
        Write-Host "[CN] 日志输出: $logPath" -ForegroundColor Gray
        Write-Host "[EN] Log output: $logPath" -ForegroundColor Gray
        
        # 构建参数
        $jmpArgs = @("/R", "`"$jslFile`"")
        if ($Silent) {
            $jmpArgs = @("/S") + $jmpArgs
        }
        
        # 执行 JMP
        & $jmpPath $jmpArgs 2>&1 | Tee-Object -FilePath $logPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[CN] JMP 执行完成" -ForegroundColor Green
            Write-Host "[EN] JMP execution complete" -ForegroundColor Green
        } else {
            Write-Warning "[CN] JMP 退出码: $LASTEXITCODE"
            Write-Warning "[EN] JMP exit code: $LASTEXITCODE"
        }
    }
    
    "data-info" {
        $jmpFile = $Args[0]
        if (-not (Test-Path $jmpFile)) {
            Write-Error "[CN] JMP 数据文件不存在: $jmpFile / [EN] JMP data file not found: $jmpFile"
            exit 1
        }
        
        # 生成临时 JSL 脚本获取数据结构
        $tempJsl = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.jsl'
        @"
dt = Open("$jmpFile");
dt << Show Properties();
"@ | Set-Content $tempJsl -Encoding UTF8
        
        & $jmpPath /R $tempJsl 2>&1
        Remove-Item $tempJsl -ErrorAction SilentlyContinue
    }
    
    "read-log" {
        $logPath = $Args[0]
        if (-not (Test-Path $logPath)) {
            Write-Error "[CN] 日志文件不存在: $logPath / [EN] Log file not found: $logPath"
            exit 1
        }
        
        Get-Content $logPath
    }
}
