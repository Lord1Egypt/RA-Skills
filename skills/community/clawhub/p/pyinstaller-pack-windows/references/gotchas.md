# PyInstaller on Windows — gotchas

Collected from real packaging of a Tkinter GUI (model_manager / claude_switcher).

## 1. `--icon` relative path resolves to `--workpath`, not cwd

Symptom: `FileNotFoundError: Icon input file <workpath>\mm.ico not found`.
Cause: PyInstaller resolves a relative `--icon` against `--workpath`, where the
file does not live.
Fix: pass an **absolute** path.
- Local: `--icon "C:\Users\you\project\mm.ico"`.
- CI: `--icon "$env:GITHUB_WORKSPACE\mm.ico"` (runner env var; avoids the
  GitHub Actions `$ { { } }` expression that WAFs flag as template injection).

## 2. Frozen `sys.executable` is the exe, not python

After `PyInstaller --onefile`, `sys.executable` points to the generated `.exe`.
If the app runs a child Python script (e.g. `install_free_llms.py`), do NOT use
`sys.executable`. Provide a fallback:

```python
def _host_python():
    # 受管/隔离 Python 未必在 PATH；直接用系统固定路径更稳
    for p in (r"C:\Python313\python.exe", r"C:\Python312\python.exe"):
        if os.path.exists(p):
            return p
    return sys.executable  # 兜底
```

## 3. Tkinter needs a system Python that actually ships tkinter

The managed WorkBuddy Python (`~/.workbuddy/binaries/python/.../3.13.12`) had no
tkinter, so freezing with it crashed at import. Package with the interpreter that
passes `python -c "import tkinter"` (usually the system `C:\Python313`).

## 4. `--onefile --windowed` for GUI apps

- `--onefile`: single portable exe (unpacks to a temp dir at launch; fine for
  small tools).
- `--windowed`: no console window. For CLI tools omit `--windowed` (keep console).

## 5. Version stamping from git tags

Keep `version.py` as the only version source. In CI, rewrite it before building:
- Release: `version = tag.trimStart('v')`  (e.g. `v1.2.0` -> `1.2.0`).
- Push: append `-dev` (e.g. `1.0.0-dev`) to distinguish dev builds.
Then `Set-Content version.py "__version__ = \"$ver\""`.

## 6. `.gitignore` whitelist for "ignore-all" repos

If the repo default-ignores everything (`*`) and whitelists a few files, also
whitelist the build inputs:
```
!version.py
!.github/
!.github/**
```
Otherwise the workflow file and version source won't be committed, and CI can't
run.

## 7. CI must run on `windows-latest`

Real Windows `.exe` can only be produced on a Windows runner. Use:
```yaml
runs-on: windows-latest
permissions:
  contents: write   # needed for gh release upload
```
Upload as artifact on push; attach to release on `release: [published]`.
