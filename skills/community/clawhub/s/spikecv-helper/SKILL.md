---
name: spikecv-helper
description: Help AI Agents answer questions and execute tasks for SpikeCV, an ultra-high-speed spike camera vision framework. Use when the user asks about spike cameras, SpikeCV repository, spike dataset download, running vision task like tracking, reconstruction through spike vision, etc.

---

# SpikeCV Agent Skill

*last updated: 2026-04-28*

This document is designed to equip an AI Agent (or developer) with the necessary prior knowledge and instructions to answer questions and execute tasks within the SpikeCV repository.

Any command execution or conceptual question should be informed by the context in this document and the attached references. 

> **Before reading**: If you're unfamiliar with spike cameras or SpikeCV's architecture, first read `references/About_SpikeCV.md`.

---

## 🧭 Quick Lookup

Use this table to jump to the right section. If it's not here, the answer isn't in this skill.

| You want... | Go to... |
|---|---|
| What is SpikeCV? | `references/About_SpikeCV.md` |
| Install SpikeCV | [§ Installation](#-installation) |
| SpikeCV API docs | [spikecv.readthedocs.io](https://spikecv.readthedocs.io) |
| SpikeCV Project directory structure | [§ Project Layout](#-project-layout) |
| Run `spikecv` CLI (download, track, reconst) | [§ CLI Reference](#-cli-reference) |
| Full publication list (up-to-date) | [spikecv.github.io/publications.html](https://spikecv.github.io/publications.html) |
| Algorithm and it's theory | search for `docs/source/核心操作.rst` 🇨🇳 or source code under `SpikeCV/spkProc/` 🇬🇧 `SpikeCV/examples` 🇬🇧, you might get it wrong, so notify user to look up the details in publication for exact theory |
| SpikeCV event, competition, Team contact, contribution, hardware | `references/About_SpikeCV.md` |
| Dataset descriptions | `references/About_SpikeCV.md` |
| Troubleshooting | [§ Gotchas & Common Errors](#-gotchas--common-errors) |

**Not in this skill?** → Defer to the user or suggest SpikeCV [website](https://spikecv.github.io) and SpikeCV team contact (spikecv@outlook.com).

---

## 📦 Installation

**Prerequisites**:
- Python ≥ 3.10
- Python virtual environment (**Conda** recommended): see [install_miniconda.md](references/install_miniconda.md) for a step-by-step setup guide from scratch.

```bash
git clone https://github.com/Zyj061/SpikeCV
cd SpikeCV
pip install .[cli]
```

Optional extras:
```bash
pip install .[tracking]   # for SNNTracker/SpikeSORT
```

**Verify**:
```bash
spikecv --help
```

**Quick health check** (downloads ~40 MB and runs TFSTP reconstruction):
```bash
spikecv data download --dataset recVidarReal2019 --agent-used
cd datasets/
spikecv proc reconst --agent-used
```

---

## 🛠 CLI Reference

SpikeCV provides the `spikecv` command for wrapper interactions. After installation, you can use it to download datasets and run processing algorithms. 

All commands accept `--agent-used` to return structured JSON output. **Always include this flag.**

> **Note**: Feel free to explore other CLI options and parameters as needed. The following examples only showcase partial subcommands and parameters, the CLI may support additional features or algorithms. Always refer to `--help` for the most up-to-date command options and usage instructions.

### `spikecv data download`

Download a dataset from the OpenI platform:

```bash
spikecv data download --dataset <name> --local-dir <path> --agent-used
```
| Dataset | For Task | 
|---|---|
| `recVidarReal2019` | Reconstruction |
| `motVidarReal2020` | Tracking | 

**⚠️ Path gotcha**: Data lands in `<local-dir>/<dataset>/`. Default local-dir is `datasets/`, so your dat files end up at `datasets/recVidarReal2019/classA/car-100kmh.dat`, NOT `recVidarReal2019/classA/car-100kmh.dat`.

### `spikecv proc reconst`

Reconstruct visible images from a raw `.dat` spike stream. Default algorithm: **TFSTP**.

```bash
# From the datasets/ directory:
cd datasets/
spikecv proc reconst --dat-file-path recVidarReal2019/classA/car-100kmh.dat --agent-used

# Or with an absolute/explicit path:
spikecv proc reconst --dat-file-path /path/to/recVidarReal2019/classA/car-100kmh.dat \
                     --yaml-file-path /path/to/recVidarReal2019/config.yaml \
                     --agent-used
```

**Key parameters**:
- `--dat-file-path`: Path to `.dat` spike stream file
- `--yaml-file-path`: Path to `config.yaml` for the dataset (default: `recVidarReal2019/config.yaml`)
- `--begin-idx`: Starting frame index (default: 500)
- `--block-len`: How many spike frames to process (default: 1500)
- `--stp-d`, `--stp-F`, `--stp-f`: STP model parameters

**⚠️ Path gotcha**: The default `yaml-file-path` is `recVidarReal2019/config.yaml` (relative to cwd). If you download the dataset using the CLI, it lives under `datasets/recVidarReal2019/`. You must either `cd datasets/` first or pass explicit paths.

### `spikecv proc track`

Run multi-object tracking on spike data. Default algorithm: **SNNTracker**.

```bash
spikecv proc track --scene-idx 0 --metrics --agent-used
```

**Key parameters**:
- `--scene-idx`: Scene index 0–6
- `--metrics`: (Optional) Calculate MOTA/IDF1 metrics (requires ground truth labels)

**⚠️ Dataset**: Tracking uses `motVidarReal2020`, not `recVidarReal2019`.

---

## 📁 Project Layout

```
SpikeCV/
├── SpikeCV/
│   ├── cli/               # CLI command definitions (typer)
│   ├── device/            # Hardware driver for spike cameras
│   ├── examples/          # Standalone test scripts (**NOT for agent use**, use CLI instead)
│   ├── metrics/           # Quantitative evaluation (PSNR, SSIM, MOTA, IDF1, AEPE)
│   ├── spkData/           # Data loaders + config.yaml parsing
│   │   └── load_dat.py    # ParaDict generation, SpikeStream class
│   ├── spkProc/           # ⭐ Core algorithms
│   │   ├── filters/       # STP filter (background removal)
│   │   ├── reconstruction/ # TFI, TFP, TFSTP, SSML
│   │   ├── tracking/      # SNNTracker, SpikeSORT
│   │   ├── detection/     # STDP, Motion-based detection
│   │   ├── recognition/   # RPSNet, SVM, VGG
│   │   ├── depth_estimation/ # SpikeT (Transformer)
│   │   ├── optical_flow/  # SCFlow
│   │   └── augment/       # Data augmentation
│   ├── utils/             # Path helpers
│   └── visualization/     # Video generation from spikes
├── docs/
│   ├── spike_algo.md      # deprecated
│   ├── data_processing.md # deprecated
│   ├── tools.md           # deprecated
│   ├── examples.md        # deprecated
│   └── source/            # 🇨🇳 Sphinx sources (readthedocs)
├── Publications.md        # 📄 Publication list (may be stale — use website instead)
├── README.md / README_en.md
└── CONTRIBUTING.md / CONTRIBUTING_en.md
```

### 🌐 Documentation by Language

| File(s) | Language | Best for |
|---|---|---|
| `docs/source/*.rst` | 🇨🇳 Chinese | API, little Algorithm theory, code examples |
| `SpikeCV/spkProc/**/*.py` (source code) | 🇬🇧 English | Algorithm math + implementation details |
| `README_en.md`, `CONTRIBUTING_en.md` | 🇬🇧 English | Setup, contribution workflow |
| `Publications.md` | 🇬🇧 English | Publication list (stale — see website) |

---

## 🚨 Rules (SHOULD NOT DO)

These are not suggestions — following them prevents errors and hallucinations:

1. **Use CLI, not example scripts** — If a task has a `spikecv` CLI command, use it. Do NOT run `SpikeCV/examples/test_snntracker.py` or similar standalone scripts directly.
2. **Always include `--agent-used`** — Otherwise the CLI prints log text, not structured JSON.
3. **Do not modify SpikeCV code** — Suggest the user contact the team instead (spikecv@outlook.com).
4. **Do not hallucinate external resources** — For contacts, purchases, or contributions, only use info from `references/About_SpikeCV.md`.
5. **For publication/paper queries → always use the website** — `Publications.md` in the repo may be outdated. Point to [spikecv.github.io/publications.html](https://spikecv.github.io/publications.html) as the canonical source.

---

## 🐛 Gotchas & Common Errors

| Symptom | Cause | Fix |
|---|---|---|
| `"Data path '...config.yaml' does not exist"` | `--yaml-file-path` is relative but you're not in the right directory | `cd datasets/` first, or pass full path |
| `spikecv proc track` fails | Wrong dataset — using `recVidarReal2019` instead of `motVidarReal2020` | Download correct dataset first |
| `--scene-idx` out of range | `motVidarReal2020` only has scenes 0–6 | Use a value in [0, 6] |
| `--scene-idx` in range but still broken | some of the scene data might not have uploaded by the developer, check carefully if the corresponding scene appear in the downloaded dataset | don't use the scene that's not downloaded |
| `spikecv` not found | CLI not installed or not in PATH | Run `pip install .[cli]` from SpikeCV root |
| `--agent-used` not working (no JSON output) | Using an older SpikeCV version | Update to latest, or check `spikecv --help` for flag name |