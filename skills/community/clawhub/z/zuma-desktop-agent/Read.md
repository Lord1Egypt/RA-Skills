安装：
1. C:\Users\jhon\.openclaw\workspace\skills\
2. C:\Users\jhon\.qclaw\workspace\skills\
3. d:\QClaw\resources\openclaw\config\skills\、
4. 不安装，直接使用来源目录。

固定安装目录： 
创建文件：
C:\Users\jhon\.local\bin\skillhub.cmd
添加：
@echo off
set "CLI=%USERPROFILE%\.skillhub\skills_store_cli.py"
set "INSTALL_DIR=D:\QClaw\resources\openclaw\config\skills"
if not exist "%CLI%" (
  echo Error: CLI not found at %CLI% >&2
  exit /b 1
)
python3 "%CLI%" --dir "%INSTALL_DIR%" %* 2>nul || python "%CLI%" --dir "%INSTALL_DIR%" %* 2>nul || py -3 "%CLI%" --dir "%INSTALL_DIR%" %*


安装F:\SERVER_TENCENT\home\datad\nodeproject\SKILLS\zuma-cron-manager-v94 到 C:\Users\{当前用户}\.openclaw\workspace\skills\zuma-desktop-rpa-control
安装F:\SERVER_TENCENT\home\datad\nodeproject\SKILLS\zuma-cron-manager-v94 到 C:\Users\{当前用户}\.qclaw\workspace\skills\zuma-desktop-rpa-control

更新：
Copy-Item -Path "F:\SERVER_TENCENT\home\datad\nodeproject\SKILLS\zuma-cron-manager-v93\*" -Destination "$env:USERPROFILE\.openclaw\workspace\skills\zuma-cron-manager-v93" -Recurse -Force

重启：
openclaw gateway restart