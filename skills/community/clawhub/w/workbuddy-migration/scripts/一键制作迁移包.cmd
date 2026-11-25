@echo off
chcp 65001 >nul
title WorkBuddy 一键制作迁移包
cd /d %~dp0
:menu
cls
echo ================================================================
echo   WorkBuddy 换电脑迁移 - 一键制作迁移包（在旧电脑运行）
echo ================================================================
echo.
echo   制作前请先完全退出 WorkBuddy（否则数据可能不完整）。
echo.
echo   [1] 完整迁移包（推荐）：配置层 + 项目层 + 数据层
echo   [2] 仅配置层：技能 / 长期记忆 / 会话工作区 / 生态配置（小包）
echo   [3] 仅项目层：git 仓库 bundle + 数据目录 + 便携 git
echo   [4] 仅数据层：会话历史 / 修改备份 / blob / 索引
echo   [5] 试运行：只扫描生成清单，不拷贝任何文件
echo   [0] 退出
echo.
set "c="
set /p c=请选择 [1]:
if "%c%"=="" set c=1
if "%c%"=="0" exit /b
if "%c%"=="1" set "SCOPE=full"
if "%c%"=="2" set "SCOPE=config"
if "%c%"=="3" set "SCOPE=projects"
if "%c%"=="4" set "SCOPE=data"
if "%c%"=="5" set "SCOPE=full" & set "DRY=-DryRun"
if "%SCOPE%"=="" goto menu
echo.
echo 开始制作（范围: %SCOPE%）...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-WBMigration.ps1" -Scope %SCOPE% %DRY%
echo.
pause
