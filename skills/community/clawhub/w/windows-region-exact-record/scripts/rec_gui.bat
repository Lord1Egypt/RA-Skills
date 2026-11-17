@echo off
REM Win Region Recorder (GUI) - drag to select a region, then Start / Stop recording.
REM Requires Python 3.8+ (tkinter NOT needed). ffmpeg: .\ffmpeg\bin\ffmpeg.exe, else PATH.
REM   --sec N              preset a time limit (0 = stop manually)
REM   --out DIR            output folder (default: %USERPROFILE%\Videos\Screen Recordings)
REM   --selftest "X Y W H" QA mode: record that region without touching the mouse

setlocal
set "HERE=%~dp0"
set "PY="
if exist "%HERE%python\pythonw.exe" set "PY=%HERE%python\pythonw.exe"
if not defined PY if defined SCREENREC_PYW set "PY=%SCREENREC_PYW%"
if not defined PY for /f "delims=" %%i in ('where pythonw 2^>nul') do if not defined PY set "PY=%%i"
if not defined PY (
  echo [ERROR] pythonw.exe not found.
  echo         Install Python 3.8+ and add it to PATH,
  echo         or set SCREENREC_PYW to the full path of pythonw.exe.
  pause
  exit /b 1
)
start "" "%PY%" "%HERE%region_rec_gui.py" %*
exit /b 0
