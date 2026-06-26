# Install And Run

## Repository Markers

Treat a checkout as REINVENT4 when it includes:

- `install.py`
- `pyproject.toml`
- `reinvent/`
- `configs/`

## Platform Guidance

- Upstream states Linux is the fully validated platform.
- Windows supports GPU and CPU but is only partially tested.
- macOS supports CPU only and is also only partially tested.
- Python requirement from `pyproject.toml`: `>=3.10`.

## Install Flow

1. Create an isolated Python environment.
2. Change into the repo root.
3. Inspect installer options first:

```bash
python install.py --help
```

4. Choose the backend token that matches the machine:

- macOS CPU: `mac`
- Linux CPU: `cpu`
- Linux CUDA: e.g. `cu126`
- Linux ROCm: e.g. `rocm6.4`
- Intel XPU: `xpu`

5. Prefer a dry run before the real install:

```bash
python install.py mac -d none --dry-run
python install.py cpu -d none --dry-run
python install.py cu126 --dry-run
```

## Optional Dependencies

`install.py` supports these dependency sets:

- `all`: upstream default; broadest install
- `none`: minimal install path
- `openeye`: OpenEye ROCS-related extras
- `isim`: iSIM-related extras

Practical rule:

- Use `-d none` for a minimal install, smoke test, or environments without
licensed OpenEye tooling.
- Use the default `all` only when the user actually wants the full upstream
dependency set and accepts heavier installs.

Observed local dry-run behavior from the checked-out repo:

- `python3 install.py mac -d none --dry-run` prints `pip install .`
- `python3 install.py cpu --dry-run` prints a `pip install .[all]` command with
  PyTorch CPU wheels and the OpenEye extra index URL

## Verify The Install

After installation, verify the CLI:

```bash
reinvent --help
reinvent_datapre --help
```

## Main Runtime Commands

Run REINVENT with a config file:

```bash
reinvent -l sampling.log configs/sampling.toml
```

Omit `-l sampling.log` to log to the console instead.

Run the datapipeline preprocessor with a TOML config:

```bash
reinvent_datapre configs/data_pipeline.toml
```

The preprocessor also accepts `-l <file>` for logging.

## Execution Rules

- Start from the example TOML files in `configs/`.
- Update model, prior, SMILES, output, and log paths before execution.
- Keep device selection consistent with the chosen backend and host hardware.
- If a user only wants a syntax or dependency sanity check, prefer `--dry-run`
or `--help` over a full install.
