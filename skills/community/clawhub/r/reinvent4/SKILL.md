---
name: reinvent4
description: Help install, configure, run, troubleshoot, and extend MolecularAI REINVENT4 for generative molecular design. Use when the user mentions REINVENT4 or Reinvent 4, asks about `reinvent` or `reinvent_datapre`, needs to choose an install backend like `mac`, `cpu`, `cu126`, `rocm6.4`, or `xpu`, wants help editing `configs/*.toml`, working with sampling, scoring, transfer learning, staged learning, notebooks, or scoring plugins, or needs guidance grounded in the upstream REINVENT4 repository.
---

# REINVENT4

Prefer a local REINVENT4 checkout over web summaries. Treat a directory as the
repo root when it contains `install.py`, `pyproject.toml`, `reinvent/`, and
`configs/`.

## Workflow

1. Classify the request: install, run configuration, data preprocessing,
notebook conversion, scoring plugin, or test/troubleshooting.
2. Read only the relevant reference file:
   - installation or CLI usage: `references/install-and-run.md`
   - TOML mode selection or parameter mapping: `references/config-modes.md`
   - plugins, notebooks, or tests: `references/plugins-and-tests.md`
3. Verify commands against the local checkout before proposing them. Prefer
`python install.py --help`, `python install.py <backend> --dry-run`, `reinvent
--help`, direct file inspection, and existing files under `configs/`.
4. Reuse the example configs in `configs/` instead of inventing schemas from
scratch.
5. Keep file paths explicit. Upstream example configs are templates and must be
adjusted to local model, SMILES, output, and log paths before execution.

## Installation Rules

- Use an isolated Python environment with Python 3.10 or newer.
- Map the processor/backend carefully:
  - macOS CPU: `mac`
  - Linux CPU: `cpu`
  - Linux NVIDIA CUDA: upstream examples use values like `cu126`
  - Linux AMD ROCm: upstream examples use values like `rocm6.4`
  - Intel XPU: `xpu`
  - Windows: CPU, CUDA, and XPU are supported, but upstream says Windows is
    only partially tested
- Remember that `install.py` defaults to optional dependency set `all`, which
includes extra packages such as `openeye` and `isim`.
- Prefer `-d none` for minimal or smoke-test installs unless the user
explicitly needs OpenEye ROCS or iSIM-related functionality.
- Use `--dry-run` before a real install whenever backend choice or dependency
resolution is uncertain.
- Verify a finished install with `reinvent --help`.

## Running REINVENT

- Main CLI entry point: `reinvent [-l logfile] <config.toml>`.
- Data pipeline entry point from `pyproject.toml`: `reinvent_datapre`.
- Prefer TOML because upstream ships maintained examples in `configs/`.
- When editing configs, update at least device selection, model/prior paths,
SMILES inputs, output files, and TensorBoard/log paths.

## Troubleshooting Rules

- On macOS, remind the user that upstream documents CPU-only support and says
macOS is only partially tested.
- If a macOS clone reports path collisions under
`contrib/tutorials/maize/adgpu_prepare`, avoid relying on those collided files
unless the user specifically needs that tutorial.
- For tests, warn that they require a JSON config with a non-existent
`MAIN_TEST_PATH`; some tests also require `OE_LICENSE`.
- Do not promise a full RL/TL run unless models, datasets, and optional
licensed tools are present locally.

## Source Files

Use these upstream files as the primary source of truth when they are present
in the local checkout:

- `README.md`
- `install.py`
- `pyproject.toml`
- `configs/README.md`
- `configs/PARAMS.md`
- `configs/SCORING.md`
- `notebooks/README.md`
- `tests/example_config.json`
