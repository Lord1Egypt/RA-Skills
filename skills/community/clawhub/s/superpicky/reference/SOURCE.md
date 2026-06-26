# Reference metadata

## Upstream

- https://github.com/jamesphotography/SuperPicky  
- **Commit used for docs/help snapshot:** `7d4422e630d8d78a04326e877d86a11d17c3f178`

## What stays in `reference/`

CLI-oriented copies only: `cli-help-captured.txt`, `docs/cli-reference.md`, `manifest机制说明.md`, `BIRDID_OPTIMIZATION_GUIDE.md`, `requirements*.txt`. (Upstream `README*.md` removed — overlapped marketing/overview; CLI truth is `cli-help-captured.txt`.)

## `scripts/install.sh`

Installs to **`$SKILL/.upstream/`** and **`$SKILL/.upstream/.venv/`**. Python 3.10–3.12 preferred; **CUDA** vs **macOS** vs **CPU** torch selection. **`verify_environment`** unless `--skip-verify`. Errors: **`[superpicky-cli verify] ERROR:`**.

**Entry:** **`${SKILL}/scripts/run.sh`** (absolute path when called from automation). Resolves `--py` and upstream CLIs to absolute paths before `exec`.

## `cli-help-captured.txt`

- **Captured (UTC):** 2026-03-24T04:35:56Z  
- **Python:** 3.12.12  
- **Via:** `scripts/run.sh` (cwd = `.upstream`)

### Pip note (macOS arm64)

Upstream `torch==2.7.1+cpu` may not install; use `requirements_base.txt` + PyPI `torch` / `torchvision` / `torchaudio` (what `install.sh` does on Darwin).

## Models

`process` / `identify` need weights: `./scripts/run.sh --py scripts/download_models.py` after install.
