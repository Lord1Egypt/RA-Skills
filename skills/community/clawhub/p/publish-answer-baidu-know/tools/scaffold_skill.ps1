#Requires -Version 5.1
<#
.SYNOPSIS
  Scaffold a new skill directory from skill-template (excludes .git).

.EXAMPLE
  .\tools\scaffold_skill.ps1 -Slug my-new-skill -Destination D:\OpenClaw\client-gdcm\my-new-skill
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Slug,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Test-KebabSlug([string]$Value) {
    return $Value -match '^[a-z0-9]+(-[a-z0-9]+)*$'
}

function Write-ScaffoldNextSteps([string]$TargetPath) {
    Write-Host ""
    Write-Host "=== 脚手架复制完成 ===" -ForegroundColor Green
    Write-Host ("目标目录: " + $TargetPath)
    Write-Host ""
    Write-Host "请在本机继续执行（未自动 git init，避免误操作）：" -ForegroundColor Yellow
    Write-Host ('  cd "' + $TargetPath + '"')
    Write-Host "  Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue"
    Write-Host "  git init"
    Write-Host "  git remote add origin <你的新技能仓库 URL>"
    Write-Host "  git remote -v"
    Write-Host "  python tests/run_tests.py -v"
    Write-Host ""
}

$TemplateRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$TargetPath = $Destination

if (-not (Test-KebabSlug $Slug)) {
    throw "Slug must be kebab-case. Got: $Slug"
}

$leaf = Split-Path -Leaf ($TargetPath.TrimEnd('\', '/'))
if ($leaf -ne $Slug) {
    throw "Destination leaf '$leaf' must match -Slug '$Slug'."
}

$parent = Split-Path -Parent $TargetPath
if (-not $parent -or -not (Test-Path -LiteralPath $parent)) {
    throw "Parent directory does not exist: $parent"
}

$gitPath = Join-Path $TargetPath ".git"
if (Test-Path -LiteralPath $gitPath) {
    throw "Target already has .git at $gitPath . Remove it first or use an empty destination."
}

$targetExists = Test-Path -LiteralPath $TargetPath
if ($targetExists) {
    $entries = @(Get-ChildItem -LiteralPath $TargetPath -Force -ErrorAction SilentlyContinue)
    if ($entries.Count -gt 0 -and -not $Force) {
        throw "Target exists and is not empty: $TargetPath . Use -Force or pick an empty directory."
    }
}

$excludeDirs = @(".git", ".pytest_cache", "__pycache__")
$excludeFiles = @(".env", ".env.local")

function Copy-TemplateTree {
    param(
        [string]$Source,
        [string]$Dest
    )
    if (-not (Test-Path -LiteralPath $Dest)) {
        New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    }
    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        $name = $_.Name
        if ($excludeDirs -contains $name) { return }
        if ($excludeFiles -contains $name) { return }
        if ($name -like "*.pyc") { return }

        $srcPath = $_.FullName
        $dstPath = Join-Path $Dest $name
        if ($_.PSIsContainer) {
            Copy-TemplateTree -Source $srcPath -Dest $dstPath
        }
        else {
            Copy-Item -LiteralPath $srcPath -Destination $dstPath -Force
        }
    }
}

Write-Host "Copy template: $TemplateRoot -> $TargetPath" -ForegroundColor Cyan
Copy-TemplateTree -Source $TemplateRoot -Dest $TargetPath

$marker = Join-Path $TargetPath ".openclaw-skill-template"
if (Test-Path -LiteralPath $marker) {
    Remove-Item -LiteralPath $marker -Force
}

Write-ScaffoldNextSteps -TargetPath (Resolve-Path -LiteralPath $TargetPath).Path
