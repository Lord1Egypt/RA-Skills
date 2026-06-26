# Install Python 3.11

## Goal
Install `python3.11` and make it available in `PATH` before running this skill.

## Option A: `pyenv` (Recommended on macOS)
1. Install `pyenv`:
```bash
brew update
brew install pyenv
```
2. Add init to `~/.zshrc`:
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc
```
3. Install Python 3.11 and set local version:
```bash
pyenv install -s 3.11.11
pyenv local 3.11.11
python3.11 --version
```

## Option B: Homebrew `python@3.11`
1. Install:
```bash
brew update
brew install python@3.11
```
2. Add PATH if needed:
```bash
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
python3.11 --version
```

If you are on Intel Mac, the path may be `/usr/local/opt/python@3.11/bin`.

## Create Skill Venv
After `python3.11` is ready:
```bash
cd /Users/lyg/software/sql2bi/skills/sql-to-bi-builder
bash scripts/setup_venv.sh --with-dev
source .venv/bin/activate
python --version
```

Expected output: `Python 3.11.x`.

## Troubleshooting
- `python3.11 not found in PATH`:
  open a new terminal or run `source ~/.zshrc`, then retry.
- `No module named yaml`:
  run `bash scripts/setup_venv.sh --with-dev` again in this skill directory.
