@echo off
rem zhuangshi_statesync launcher (ASCII only on purpose; untested on real Windows)
setlocal
set "HERE=%~dp0"
set "PY=%PYTHON%"
if not defined PY set "PY=python"
"%PY%" "%HERE%zhuangshi_statesync.py" %*
