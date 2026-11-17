# M10 Python Environments: pyenv, uv, and System Python

This reference is based on the official [M10 image documentation](https://www.unihiker.com.cn/wiki/m10/burner) and the [UNIHIKER M10 documentation](https://www.unihiker.com.cn/wiki/m10/). Always trust live detection over version assumptions.

## Image versions

| System image | Typical Python environment |
|---|---|
| **V0.4.5+** | pyenv 3.12.7 by default, bundled `uv`, and cached Python 3.12 packages |
| **V0.4.1+** | pyenv with Python 3.8.5 and 3.12.7 |
| Earlier images | System `python3`, possibly without pyenv or uv |

## Required selection flow

1. Verify the M10 connection.
2. Run `scripts/detect_python_env.ps1`.
3. Present only detected pyenv versions and uv, plus system Python as a fallback.
4. Save the user's choice in `.m10-env.json`.
5. Use that environment for both execution and dependency installation.

Example pyenv configuration:

```json
{
  "host": "10.1.2.3",
  "mode": "pyenv",
  "python_version": "3.12.7",
  "python_bin": "/root/.pyenv/versions/3.12.7/bin/python3",
  "uv_path": "/usr/local/bin/uv",
  "uv_available": true
}
```

Example uv configuration:

```json
{
  "host": "10.1.2.3",
  "mode": "uv",
  "python_version": "3.12.7",
  "python_bin": "/root/.pyenv/versions/3.12.7/bin/python3",
  "uv_path": "/usr/local/bin/uv",
  "uv_available": true
}
```

## Commands by mode

| Mode | Run | Install dependencies |
|---|---|---|
| **pyenv** | `{python_bin} /tmp/m10_nl/program.py` | `{python_bin} -m pip install <package>` |
| **uv** | `uv run python /tmp/m10_nl/program.py` | `uv pip install <package>` |
| **system** | `python3 /tmp/m10_nl/program.py` | `python3 -m pip install <package>` |

Pass `-EnvFile .m10-env.json` to `run_on_m10.ps1` to select the saved mode automatically.

## Manual pyenv checks

```bash
pyenv versions
pyenv global 3.12.7
python3 --version
```

The conventional interpreter path is `/root/.pyenv/versions/<version>/bin/python3`.

## uv checks

```bash
uv --version
uv run python script.py
uv pip install requests
uv pip list
```

Do not mix bare `pip3` with uv after the user selects uv. Confirm that `unihiker` and `pinpong` exist in any non-default interpreter before deploying.
