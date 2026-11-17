# Known Issues & Pitfalls (SPSS, Windows) — detailed root-cause

Two real failures reproduced when running SPSS on a host where the agent shell
injects its own `PYTHONPATH` (e.g. WorkBuddy Bash injects
`PYTHONPATH=<app>/cli/vendor/shim` with a `sitecustomize.py` using Python 3.6+
`os.fspath`). Recorded here so the agent never repeats them.

## 1. PYTHONPATH / `os.fspath` crash (critical)

- **Symptom**: `AttributeError: 'module' object has no attribute 'fspath'` the
  moment `spss.StartSPSS()` runs inside SPSS's **bundled Python 3.4**.
- **Root cause**: the injected `PYTHONPATH` shim's `sitecustomize.py` calls
  `os.fspath` (added in 3.6); SPSS 26's bundled Python is 3.4 and has no such
  symbol, so the interpreter aborts at startup.
- **Fix (preferred)**: use `spss_helper.py` — its `_minimal_env()` now **drops
  `PYTHONPATH`** for the bundled-Python paths (`run-internal` / `show-version`),
  so the agent never needs to touch the env manually.
- **Fix (manual, only for direct bundled-Python calls)**:
  ```bash
  PYTHONPATH= "C:/SPSS/26/Python3/python.exe" spss_helper.py run-internal "xx.sps"
  ```
- **Also**: SPSS bundled Python 3.4 has **no f-strings** — use `%s` or
  `.format()` for any string formatting in `.py` files you feed it.

## 2. `OUTPUT EXPORT` unavailable in headless / no-viewer mode

- **Symptom**: `OUTPUT EXPORT` / `OUTPUT SAVE` (to `.spv` / `.pdf`) fails or is a
  no-op when SPSS runs without the output viewer (the bundled-Python / `stats.com`
  backend has no viewer document).
- **Fix**: to get `.spv` / `.pdf`, go through the **Production Facility**:
  ```bash
  "C:/Program Files/IBM/SPSS/Statistics/26/stats.exe" --production "job.spj" silent -nologo
  ```
  (see `references/config-templates.md` for the `.spj` XML). Note `OUTPUT EXPORT`
  is also blocked inside production-job `.spj` files (see
  `references/command-examples.md`).

## 3. `SAVE OUTFILE` must point at an existing directory

- **Symptom**: `SAVE OUTFILE` to an absolute path whose directory does not exist
  fails — the skill's own `tests/test-syntax.sps` used to hard-code
  `C:/Users/WintoneFileSrv/...` and the self-test always failed.
- **Fix**: use a **relative** path (resolved against the `tests/` working dir),
  e.g. `SAVE OUTFILE="test-data.sav".` — already fixed in `tests/test-syntax.sps`.
