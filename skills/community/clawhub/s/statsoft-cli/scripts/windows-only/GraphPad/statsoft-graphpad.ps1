# statsoft-graphpad.ps1 — GraphPad Prism CLI 包装器（高级模式）
# 用法:
#   statsoft-graphpad run <pzfx_file> [--log-file <path>]
#   statsoft-graphpad data-info <pzfx_file> [--vars var1 var2]
#   statsoft-graphpad read-log <log_path>

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "data-info", "read-log")]
    [string]$Command,
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args,
    
    [string]$LogFile
)

# 读取配置
$configPath = "$PSScriptRoot\..\config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "[CN] 配置文件不存在: $configPath。请先运行 setup_graphpad.ps1 / [EN] Config file not found: $configPath. Please run setup_graphpad.ps1 first."
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$graphPadPath = $config.GraphPad.Path

if (-not (Test-Path $graphPadPath)) {
    Write-Error "[CN] GraphPad Prism 可执行文件不存在: $graphPadPath / [EN] GraphPad Prism executable not found: $graphPadPath"
    exit 1
}

switch ($Command) {
    "run" {
        $pzfxFile = $Args[0]
        if (-not (Test-Path $pzfxFile)) {
            Write-Error "[CN] PZFX 文件不存在: $pzfxFile / [EN] PZFX file not found: $pzfxFile"
            exit 1
        }
        
        $logPath = if ($LogFile) { $LogFile } else { Join-Path $PWD "graphpad-log.txt" }
        Write-Host "[CN] 执行 GraphPad Prism 文件: $pzfxFile" -ForegroundColor Cyan
        Write-Host "[EN] Executing GraphPad Prism file: $pzfxFile" -ForegroundColor Cyan
        Write-Host "[CN] 日志输出: $logPath" -ForegroundColor Gray
        Write-Host "[EN] Log output: $logPath" -ForegroundColor Gray
        
        # 执行 GraphPad Prism
        & $graphPadPath $pzfxFile 2>&1 | Tee-Object -FilePath $logPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[CN] GraphPad Prism 执行完成" -ForegroundColor Green
            Write-Host "[EN] GraphPad Prism execution complete" -ForegroundColor Green
        } else {
            Write-Warning "[CN] GraphPad Prism 退出码: $LASTEXITCODE"
            Write-Warning "[EN] GraphPad Prism exit code: $LASTEXITCODE"
        }
    }
    
    "data-info" {
        $pzfxFile = $Args[0]
        if (-not (Test-Path $pzfxFile)) {
            Write-Error "[CN] PZFX 文件不存在: $pzfxFile / [EN] PZFX file not found: $pzfxFile"
            exit 1
        }
        
        # 使用 Python prismWriter 获取数据结构
        $pythonScript = @"
from prismwriter import PrismFile
import json
pf = PrismFile('$pzfxFile')
info = {
    'tables': list(pf.tables.keys()),
    'metadata': pf.metadata
}
print(json.dumps(info, indent=2))
"@
        
        $tempPy = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.py'
        $pythonScript | Set-Content $tempPy -Encoding UTF8
        
        python $tempPy 2>&1
        Remove-Item $tempPy -ErrorAction SilentlyContinue
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
