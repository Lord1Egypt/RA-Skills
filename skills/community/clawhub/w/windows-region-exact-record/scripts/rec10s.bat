@echo off
REM Win Region Recorder (CLI) - pick two corners, then record an exact number of seconds.
REM   rec10s.bat            click top-left + bottom-right, 3s countdown, then exactly 10s
REM   rec10s.bat last       reuse the stored region in last_region.txt
REM   rec10s.bat pick       only pick/cache a region (no recording)
REM   rec10s.bat check      blink the capture box for 3s to verify the region
REM Requires Python 3.8+ (console python.exe). ffmpeg: .\ffmpeg\bin\ffmpeg.exe, else PATH.

setlocal
set "HERE=%~dp0"
set "PY="
if exist "%HERE%python\python.exe" set "PY=%HERE%python\python.exe"
if not defined PY if defined SCREENREC_PY set "PY=%SCREENREC_PY%"
if not defined PY for /f "delims=" %%i in ('where python 2^>nul') do if not defined PY set "PY=%%i"
if not defined PY (
  echo [ERROR] python.exe not found.
  echo         Install Python 3.8+ and add it to PATH,
  echo         or set SCREENREC_PY to the full path of python.exe.
  pause
  exit /b 1
)

if /I "%~1"=="pick"  goto PICK
if /I "%~1"=="check" goto CHECK
if /I "%~1"=="last"  goto LAST

echo Click the TOP-LEFT corner, then the BOTTOM-RIGHT corner of the region ...
"%PY%" "%HERE%rec_region.py" --sec 10 --pick --countdown 3
goto END

:LAST
echo Recording 10 seconds of the stored region ...
"%PY%" "%HERE%rec_region.py" --sec 10 --countdown 3
goto END

:PICK
"%PY%" "%HERE%pick_region.py" --seconds 10
goto END

:CHECK
"%PY%" "%HERE%rec_region.py" --check
goto END

:END
echo.
pause
endlocal
