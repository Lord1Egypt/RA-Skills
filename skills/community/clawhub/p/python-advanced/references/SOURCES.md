# Python Advanced — Sources

Fetched / canonical official references:

- asyncio — Asynchronous I/O: https://docs.python.org/3/library/asyncio.html
- Python Packaging User Guide — Packaging Python Projects: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Python typing: https://docs.python.org/3/library/typing.html
- pathlib: https://docs.python.org/3/library/pathlib.html
- subprocess: https://docs.python.org/3/library/subprocess.html
- venv: https://docs.python.org/3/library/venv.html
- concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html
- pytest: https://docs.pytest.org/
- ruff: https://docs.astral.sh/ruff/
- mypy: https://mypy.readthedocs.io/
- PyO3: https://pyo3.rs/
- maturin: https://www.maturin.rs/

Local verification:

```text
Python 3.13.5
templates/async_tasks.py → [0, 2, 4, 6, 8] + timeout (exit 0)
templates/run_subprocess.py → exit 0, stdout "hello"
templates/cli_app.py → parsed JSON and wrote out file (exit 0)
```

Notes:

- `subprocess.py` as a local filename shadows the stdlib; the template is named `run_subprocess.py`.
- Do not run `pytest` from a directory containing an unrelated `pytest.py`.
- The PyO3 template is illustrative and not compiled here.
