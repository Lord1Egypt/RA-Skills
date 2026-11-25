# 可移植 build_exe.cmd（复制时另存为 `build_exe.cmd`）

把下面内容保存为项目根目录的 `build_exe.cmd`，改完源码后双击即可打包。
路径全部相对本脚本所在目录（`%~dp0`），自动选 python，clone 到别处也能用。
依赖：Python 3.13 + `pip install pyinstaller`。

把两处脚本名（`model_manager` / `claude_model_switcher`）换成自己的即可。

```bat
@echo off
chcp 65001 >nul
rem 一键打包：把两个 .pyw 都打成单文件 exe，并复制到桌面。

set "BASE=%~dp0"
cd /d "%BASE%"

rem 自动选择 python：优先 PATH 里的 python，否则退回本机固定路径
where python >nul 2>nul
if %errorlevel%==0 (set "PY=python") else (set "PY=C:\Python313\python.exe")

echo [1/2] 打包 model_manager.exe ...
"%PY%" -m PyInstaller --noconfirm --onefile --windowed ^
  --name model_manager ^
  --icon "%BASE%mm.ico" ^
  --distpath "%BASE%dist" ^
  --workpath "%BASE%build_tmp" ^
  --specpath "%BASE%build_tmp" ^
  "%BASE%model_manager.pyw"
if errorlevel 1 (
    echo.
    echo [失败] model_manager 打包出错
    pause
    exit /b 1
)

echo [2/2] 打包 claude_switcher.exe ...
"%PY%" -m PyInstaller --noconfirm --onefile --windowed ^
  --name claude_switcher ^
  --icon "%BASE%mm.ico" ^
  --distpath "%BASE%dist" ^
  --workpath "%BASE%build_tmp" ^
  --specpath "%BASE%build_tmp" ^
  "%BASE%claude_model_switcher.pyw"
if errorlevel 1 (
    echo.
    echo [失败] claude_switcher 打包出错
    pause
    exit /b 1
)

copy /y "%BASE%dist\model_manager.exe" "%USERPROFILE%\Desktop\模型管理器.exe" >nul
copy /y "%BASE%dist\claude_switcher.exe" "%USERPROFILE%\Desktop\Claude 模型切换器.exe" >nul
echo.
echo [完成] 已生成 dist\model_manager.exe 与 dist\claude_switcher.exe，并复制到桌面
pause
```
