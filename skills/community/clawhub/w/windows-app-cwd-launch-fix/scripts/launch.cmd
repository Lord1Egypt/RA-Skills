@echo off
rem =====================================================================
rem  DyberPet launcher   >>>   DOUBLE-CLICK THIS FILE TO START  <<<
rem
rem  WHY THIS FILE EXISTS
rem  --------------------
rem  DyberPet resolves every "res\..." path against the WORKING DIRECTORY
rem  of the process (its settings.py sets basedir = '' on Windows).
rem  If the working directory is not this folder, it crashes with:
rem      FileNotFoundError: [Errno 2] No such file or directory:
rem                         'res/language/language.json'
rem  Double-clicking the .exe does NOT always guarantee a correct working
rem  directory, so this launcher forces it. It works from anywhere:
rem  Explorer, a shortcut, the Run dialog, a terminal in another folder.
rem
rem  Content is ASCII-only on purpose, and saved with CRLF line endings.
rem =====================================================================

setlocal
cd /d "%~dp0"

if not exist "%~dp0res\language\language.json" goto missing
if not exist "%~dp0_internal" goto missinginternal

rem  /d forces the startup directory of the child process as well,
rem  so this cannot break even if the cd above were ignored.
for %%F in ("%~dp0*.exe") do start "" /d "%~dp0" "%%~fF"
goto done

:missing
echo.
echo  [ERROR] res\language\language.json was not found next to this launcher.
echo          The package looks incomplete or was not fully unzipped.
echo.
echo  Expected in: %~dp0res\language\
echo.
pause
exit /b 1

:missinginternal
echo.
echo  [ERROR] The "_internal" folder was not found next to this launcher.
echo          This package must be unzipped completely before running.
echo          Do not run the .exe from inside the .zip preview.
echo.
echo  Folder: %~dp0
echo.
pause
exit /b 1

:done
endlocal
