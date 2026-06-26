# 创建新功能分支和规范文件的 PowerShell 脚本
# 此脚本根据功能描述自动创建 Git 分支和初始化规范文档

param(
    [Parameter(Mandatory=$true)]
    [string]$Json,

    [int]$Number = 1,

    [string]$ShortName = "",

    [switch]$JsonInput = $false
)

# 功能：创建新功能分支和规范文件
# 使用方法：
# .\create-new-feature.ps1 -Json "功能描述" -Number 5 -ShortName "user-auth"
# 或者
# .\create-new-feature.ps1 -Json "功能描述" -JsonInput

Write-Host "正在创建新功能..."
Write-Host "功能描述: $Json"
Write-Host "分支编号: $Number"
Write-Host "简称: $ShortName"

# 构建分支名称
$branchName = "$Number-$ShortName"
Write-Host "分支名称: $branchName"

# 创建并切换到新分支
& git checkout -b $branchName

# 创建功能目录结构
$featureDir = "specs\$branchName"
New-Item -ItemType Directory -Path $featureDir -Force
New-Item -ItemType Directory -Path "$featureDir\checklists" -Force

# 创建规范文件路径
$specFile = "$featureDir\spec.md"
Write-Host "规范文件: $specFile"

# 输出结果供调用方使用
@{
    BRANCH_NAME = $branchName
    SPEC_FILE = $specFile
    FEATURE_DIR = $featureDir
} | ConvertTo-Json