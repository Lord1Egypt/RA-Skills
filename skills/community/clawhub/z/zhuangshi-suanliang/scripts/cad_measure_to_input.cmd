@echo off
rem cad_measure_to_input launcher (ASCII only on purpose; untested on real Windows)
setlocal
set "HERE=%~dp0"
set "PY=%PYTHON%"
if not defined PY set "PY=python"
"%PY%" "%HERE%cad_measure_to_input.py" %*
