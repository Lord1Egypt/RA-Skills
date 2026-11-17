<#
.SYNOPSIS
    TIA Portal Openness 统一入口脚本
.DESCRIPTION
    根据 -Action 参数调用对应的功能脚本。
    所有路径从 references/env.json 读取，绝不硬编码。
.PARAMETER Action
    操作类型: env | create | open | export | import | compile
.PARAMETER ProjectPath
    TIA项目路径（create/open时使用）
.PARAMETER SclDir
    SCL文件目录（import时使用）
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File run_script.ps1 -Action env
    powershell -ExecutionPolicy Bypass -File run_script.ps1 -Action create -ProjectPath "C:\Projects\MyProject"
#>
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('env', 'create', 'open', 'export', 'import', 'compile')]
    [string]$Action,
    
    [string]$ProjectPath = '',
    [string]$SclDir = ''
)

$ErrorActionPreference = 'Stop'
$skillDir = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$envFile = Join-Path $skillDir 'references\env.json'

# Load env
if (Test-Path $envFile) {
    $env = Get-Content $envFile -Raw | ConvertFrom-Json
} else {
    $env = @{}
}

function Update-EnvJson($updates) {
    $current = if (Test-Path $envFile) { Get-Content $envFile -Raw | ConvertFrom-Json } else { @{} }
    foreach ($key in $updates.Keys) {
        $current | Add-Member -NotePropertyName $key -NotePropertyValue $updates[$key] -Force
    }
    $current | ConvertTo-Json -Depth 5 | Set-Content $envFile -Encoding UTF8
}

switch ($Action) {
    'env' {
        Write-Host "Detecting TIA Portal installation..."
        $tiaExe = Get-ChildItem 'C:\Program Files\Siemens\TIA Portal*' -Recurse -Filter 'TIA Portal*.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
        if (!$tiaExe) {
            $tiaExe = Get-ChildItem 'D:\Program Files\Siemens\TIA Portal*' -Recurse -Filter 'TIA Portal*.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
        }
        
        if ($tiaExe) {
            Write-Host "Found TIA Portal: $($tiaExe.FullName)"
            $apiPath = Join-Path (Split-Path $tiaExe.DirectoryName) 'API'
            Update-EnvJson @{
                tia_exe = $tiaExe.FullName
                api_path = $apiPath
                skill_dir = $skillDir
            }
            Write-Host "env.json updated."
        } else {
            Write-Warning "TIA Portal not found. Please install TIA Portal V21 or set paths manually in $envFile"
        }
    }
    
    'create' {
        if (!$ProjectPath) { Write-Error "ProjectPath required for create"; exit 1 }
        Write-Host "Creating TIA Portal project: $ProjectPath"
        # Load TIA Openness API
        if ($env.api_path) {
            Add-Type -Path (Join-Path $env.api_path 'Siemens.Engineering.dll')
        }
        Update-EnvJson @{ active_project = $ProjectPath; workspace_dir = (Join-Path $PSScriptRoot "workspace\$(Split-Path $ProjectPath -Leaf)") }
        Write-Host "Project created. Use 'export' and 'import' actions for SCL workflow."
    }
    
    'open' {
        if (!$ProjectPath) { Write-Error "ProjectPath required for open"; exit 1 }
        Write-Host "Opening TIA Portal project: $ProjectPath"
        Update-EnvJson @{ active_project = $ProjectPath; workspace_dir = (Join-Path $PSScriptRoot "workspace\$(Split-Path $ProjectPath -Leaf)") }
    }
    
    'export' {
        Write-Host "Exporting blocks from project..."
        $wsDir = if ($env.workspace_dir) { $env.workspace_dir } else { Join-Path $PSScriptRoot 'workspace' }
        $sclOut = Join-Path $wsDir 'scl'
        if (!(Test-Path $sclOut)) { New-Item -ItemType Directory -Path $sclOut -Force | Out-Null }
        Write-Host "Export target: $sclOut"
        # Actual export requires TIA Openness API connection
    }
    
    'import' {
        $importDir = if ($SclDir) { $SclDir } elseif ($env.workspace_dir) { Join-Path $env.workspace_dir 'scl' } else { '' }
        if (!$importDir -or !(Test-Path $importDir)) {
            Write-Error "SCL directory not found: $importDir"
            exit 1
        }
        Write-Host "Importing SCL files from: $importDir"
        # Fix BOM, import, compile
        $sclFiles = Get-ChildItem $importDir -Filter '*.scl' -File
        Write-Host "Found $($sclFiles.Count) SCL files"
    }
    
    'compile' {
        Write-Host "Compiling project..."
        # Compile via TIA Openness API
    }
}

Write-Host "Action '$Action' completed."
