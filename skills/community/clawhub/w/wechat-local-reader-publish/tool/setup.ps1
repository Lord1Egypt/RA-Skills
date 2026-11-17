# wechat-local-reader 安装脚本（Windows PowerShell）
# 在 WorkBuddy PowerShell 或系统 PowerShell 中执行： .\tool\setup.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "[1/3] 创建隔离虚拟环境 .venv ..."
python -m venv .venv

Write-Host "[2/3] 安装依赖并注册 wechat-cli 命令 ..."
& .venv\Scripts\python.exe -m pip install --upgrade pip -q
& .venv\Scripts\python.exe -m pip install -e . -q

Write-Host "[3/3] 生成启动器 wechat-cli.bat ..."
@"
@echo off
"$root\.venv\Scripts\wechat-cli.exe" %*
"@ | Out-File -Encoding ascii wechat-cli.bat

Write-Host ""
Write-Host "安装完成。把 $root 加入 PATH 后，即可直接运行："
Write-Host "    wechat-cli --help"
Write-Host "或在该目录内使用： wechat-cli.bat --help"
