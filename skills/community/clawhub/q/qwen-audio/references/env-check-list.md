Check the items below. After each item is done, update this file and mark [x] as completed.
Only complete the section for your current OS.

## Confirm current OS
- [ ] Confirm whether you are on macOS or Windows.
  - macOS: `uname -s` should print `Darwin`.
  - Windows (PowerShell): `$env:OS` should include `Windows`.

## Verify `.venv` and Python version (>= 3.10)
- [ ] macOS
  - Check `.venv`: `[ -d .venv ] && echo ".venv exists" || echo ".venv missing"`
  - If missing, create env: `uv sync --prerelease=allow`
  - Check Python version: `uv run python -c "import sys; print(sys.version)"`

- [ ] Windows (PowerShell)
  - Check `.venv`: `if (Test-Path .venv) { '.venv exists' } else { '.venv missing' }`
  - If missing, create env: `uv sync --prerelease=allow`
  - Check Python version: `uv run python -c "import sys; print(sys.version)"`

## Verify platform-specific dependencies
- [ ] macOS dependency check
  - Verify `mlx-audio`: `uv run python -c "import mlx_audio; print('mlx-audio ok')"`
  - If missing: `uv add mlx-audio --prerelease=allow`

- [ ] Windows dependency check
  - Verify `qwen-asr`, `qwen-tts`, `torch`:
    `uv run python -c "import qwen_asr, qwen_tts, torch; print('qwen-asr/qwen-tts/torch ok')"`
  - If missing: `uv sync --prerelease=allow`

