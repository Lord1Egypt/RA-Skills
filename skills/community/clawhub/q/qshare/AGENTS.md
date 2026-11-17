# Repository Guidelines

## Project Structure & Module Organization

qshare is a small Python command-line package for sharing one local file through CNB uploads by default, with an optional TryCloudflare tunnel selected by `--cf`. Application code lives in `src/qshare/`: `cli.py` owns argument parsing, CNB prompts, local HTTP serving, tunnel lifecycle, and QR output; `cnb.py` implements CNB upload and deletion. `__main__.py` supports `python -m qshare`. Put unit and integration-style tests in `tests/test_qshare.py`; add focused test modules only when the test surface grows. `scripts/build_platform_wheels.py` post-processes built wheels to add platform-specific `cloudflared` binaries for `--cf`. Distribution artifacts belong in `dist/` and are generated, not hand-edited.

Keep `README.md`, `README.en.md`, `SKILL.md`, CLI help, and package descriptions consistent: CNB is the default, kept CNB files have a default 3-day retention, and only CNB supports immediate manual deletion of the current upload. The deletion prompt defaults to delete (Enter or `y`); `n` keeps the remote file. Local files are never deleted. `--cf` defaults to a 2-hour tunnel, and `--ttl`/`--port` apply only to that channel. PyPI uses `README.md` as the long description; publish a new version to update its project documentation.

## Build, Test, and Development Commands

Create an isolated environment and install the package in editable mode:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
PYTHONPATH=src pytest -q
```

Run the last command before submitting changes; it ensures tests import the source tree. Build standard artifacts with `uv build`. To prepare platform wheels containing pre-downloaded Cloudflare binaries, run `python scripts/build_platform_wheels.py --assets-dir /path/to/cloudflared-assets` after `uv build`.

## Coding Style & Naming Conventions

Use four-space indentation, standard-library-first imports, `snake_case` for functions and variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for module constants. Follow the surrounding code: type public helpers where practical, prefer `pathlib.Path` for paths, and keep messages suitable for a terminal CLI. Preserve the declared Python 3.6 compatibility; do not introduce syntax or standard-library APIs requiring later versions. No formatter or linter is configured, so keep edits consistent with nearby code and avoid unrelated reformatting.

## Testing Guidelines

Use pytest with tests named `test_<behavior>`. Exercise observable behavior and error paths, using `monkeypatch`, `tmp_path`, and `capsys` to avoid real network access, tunnels, browsers, or user-home writes. Changes to platform-dependent behavior should cover the relevant `os.name` branch. Add regression coverage for every bug fix.

## Commit & Pull Request Guidelines

Recent history favors brief, imperative subjects such as `add CNB upload channel`, `fix Windows QR scanner compatibility`, and conventional prefixes when useful (`feat:`, `fix:`, `chore:`). Keep commits narrow. Pull requests should state the user-visible change, testing performed, and any platform or packaging impact; link related issues and include terminal output or screenshots when CLI/QR presentation changes.

## Security & External Services

Treat public sharing and CNB uploads as security-sensitive. Running the default command starts a CNB upload immediately; preserve the explicit post-upload deletion prompt and tunnel URL validation. Never add credentials, private URLs, or sample sensitive files to the repository; test external-service paths through mocks.
