# statsoft-graphpad.ps1 — GraphPad Prism GUI helper (detection and reading only; no CLI / no batch automation)
# GraphPad Prism has no CLI mode and cannot run silent batch jobs. This script only:
#   1) Manually launch the GraphPad Prism GUI to open a file (no wait, no analysis driving)
#   2) Read-only read/validate .pzfx file structure (via the prismwriter Python library, no GUI)
#   3) Read a user-provided log file
# Usage:
#   statsoft-graphpad open <pzfx_file>                    # manually launch GUI to open file (no automation)
#   statsoft-graphpad data-info <pzfx_file> [--vars ...]   # read-only structure read
#   statsoft-graphpad read-log <log_path>                 # read log

param(
    [Parameter(Position=0)]
    [ValidateSet("open", "data-info", "read-log")]
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

# Read config
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\config.json" }
if (-not (Test-Path $configPath)) { $configPath = Join-Path $PSScriptRoot "..\..\config.json" }
if (-not (Test-Path $configPath)) {
    Write-Error (if ($script:isZH){"配置文件不存在: $configPath。请先运行 setup_graphpad.ps1"}else{"Config file not found: $configPath. Please run setup_graphpad.ps1 first."})
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json
$graphPadPath = $config.GraphPad.Path

if (-not (Test-Path $graphPadPath)) {
    Write-Error (if ($script:isZH){"GraphPad Prism 可执行文件不存在: $graphPadPath"}else{"GraphPad Prism executable not found: $graphPadPath"})
    exit 1
}

switch ($Command) {
    "open" {
        $pzfxFile = $Args[0]
        if ($pzfxFile -and -not (Test-Path $pzfxFile)) {
            Write-Error (if ($script:isZH){"PZFX 文件不存在: $pzfxFile"}else{"PZFX file not found: $pzfxFile"})
            exit 1
        }
        Write-Lang "GraphPad Prism 无 CLI 模式，正在手动启动 GUI（不自动化分析）..." "GraphPad Prism has no CLI mode; launching GUI manually (no automation)..." -Color Cyan
        if ($pzfxFile) {
            Start-Process -FilePath $graphPadPath -ArgumentList $pzfxFile
        } else {
            Start-Process -FilePath $graphPadPath
        }
        Write-Lang "已打开 GraphPad Prism，请手动操作。" "GraphPad Prism opened; please operate manually."
    }

    "data-info" {
        $pzfxFile = $Args[0]
        if (-not (Test-Path $pzfxFile)) {
            Write-Error (if ($script:isZH){"PZFX 文件不存在: $pzfxFile"}else{"PZFX file not found: $pzfxFile"})
            exit 1
        }

        # Pass the PZFX path as a command-line ARGUMENT to Python (NEVER
        # interpolate it into source) -> no Python code injection via a crafted
        # file path. The temp script is disclosed and removed in a finally block.
        Write-Lang "创建临时 Python 脚本（仅本次运行，结束后删除）:" "Creating temporary Python script (this run only, deleted afterward):" -Color Gray
        $tempPy = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.py'
        Write-Host "  $tempPy" -ForegroundColor Gray
        $pythonScript = @"
import sys, json
from prismwriter import PrismFile
path = sys.argv[1]
pf = PrismFile(path)
info = {'tables': list(pf.tables.keys()), 'metadata': pf.metadata}
print(json.dumps(info, indent=2))
"@
        try {
            $pythonScript | Set-Content $tempPy -Encoding UTF8
            python $tempPy "$pzfxFile" 2>&1
        } finally {
            Remove-Item $tempPy -ErrorAction SilentlyContinue
        }
    }

    "read-log" {
        $logPath = $Args[0]
        if (-not (Test-Path $logPath)) {
            Write-Error (if ($script:isZH){"日志文件不存在: $logPath"}else{"Log file not found: $logPath"})
            exit 1
        }

        Get-Content $logPath
    }
}
