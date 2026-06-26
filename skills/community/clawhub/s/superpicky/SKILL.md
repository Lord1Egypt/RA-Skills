---
name: superpicky-cli
description: >-
  SuperPicky CLI skill: use absolute paths to scripts/install.sh and scripts/run.sh
  for automation; run.sh three entries (superpicky_cli, birdid_cli, --region-query)
  and --py; reference/cli-help-captured.txt.
---

# SuperPicky CLI (skill)

[SuperPicky](https://github.com/jamesphotography/SuperPicky) — bird photo AI culling (`superpicky_cli.py`, `birdid_cli.py`). This skill only covers **CLI paths** under **`$SKILL`** (directory containing this file).

## Three entry modes (`run.sh`)

All user-facing commands go through **`${SKILL}/scripts/run.sh`** (use the **absolute** path when cwd is not `$SKILL`). There are **three** entry modes (plus one helper):

| # | How you invoke | Program | What it is for |
|---|----------------|---------|----------------|
| **1** | **`"${SKILL}/scripts/run.sh"`** *then the same args as* `superpicky_cli.py` | `superpicky_cli.py` | **Main pipeline:** `process` / `reset` / `restar` / `info` / `burst` / `identify` (folder culling, EXIF, stars, optional auto BirdID). |
| **2** | **`"${SKILL}/scripts/run.sh" --birdid`** *then the same args as* `birdid_cli.py` | `birdid_cli.py` | **Standalone BirdID:** batch `identify`, `organize` by species, `reset`, `list-countries`; OSEA / eBird filters. |
| **3** | **`"${SKILL}/scripts/run.sh" --region-query`** *then args for* `ebird_region_query.py` | `ebird_region_query.py` | **Code lookup only:** fuzzy match place names → eBird **country/region codes** for use in (1) or (2) (`--birdid-country`, `--birdid-region`, `-c`, `-r`). |

**Helper (not a separate “product” entry):** `--py PATH` — run a script with the same venv. **PATH** may be absolute, or relative to **`.upstream/`** (internally normalized to an absolute path before `exec`).

### Absolute paths (required for agents / cron)

- **`install.sh` / `run.sh` / `capture-cli-help.sh`:** when another tool invokes them, use the **full absolute path** (e.g. `${SKILL}/scripts/run.sh`, never rely on `cd` + `./scripts/run.sh`).
- **`run.sh` internals:** always `exec` Python with **absolute** paths for `superpicky_cli.py`, `birdid_cli.py`, `ebird_region_query.py`, and the `--py` script (relative args become `${SKILL}/.upstream/...`).

Interactive (from `$SKILL`):

```bash
./scripts/run.sh process /photos
```

Automation (example):

```bash
SKILL="$(cd /path/to/superpicky-cli && pwd)"
"${SKILL}/scripts/run.sh" process /photos
"${SKILL}/scripts/run.sh" --py "${SKILL}/.upstream/scripts/download_models.py"
```

## Layout

**`$SKILL`** = skill root.

```
$SKILL/
├── SKILL.md
├── .gitignore              # .upstream/
├── reference/              # CLI help + small doc set (see table below)
└── scripts/
    ├── install.sh
    ├── run.sh              # ENTRY (+ --region-query → ebird_region_query.py)
    ├── ebird_region_query.py   # fuzzy eBird country/region code lookup
    ├── ebird_region_query_test.py
    ├── capture-cli-help.sh
    └── setup-upstream-venv.sh → install.sh

$SKILL/.upstream/           # clone (gitignored)
├── .venv/
├── superpicky_cli.py
├── birdid_cli.py
└── …
```

| Script | Role |
|--------|------|
| `scripts/install.sh` | Install into `.upstream/` + `.upstream/.venv/` |
| **`scripts/run.sh`** | **Three entries:** default → `superpicky_cli.py`; `--birdid` → `birdid_cli.py`; `--region-query` → `ebird_region_query.py`; helper `--py` |
| `scripts/ebird_region_query.py` | Fuzzy lookup (also via `run.sh --region-query`); tests: `ebird_region_query_test.py` |
| `scripts/capture-cli-help.sh` | Refresh `reference/cli-help-captured.txt` |

## Reference (minimal)

| File | Use |
|------|-----|
| [reference/cli-help-captured.txt](reference/cli-help-captured.txt) | **Flags** (`--help` dump) |
| [reference/docs/cli-reference.md](reference/docs/cli-reference.md) | Short bilingual CLI notes |
| [reference/docs/manifest机制说明.md](reference/docs/manifest机制说明.md) | Reset / manifest behavior |
| [reference/docs/BIRDID_OPTIMIZATION_GUIDE.md](reference/docs/BIRDID_OPTIMIZATION_GUIDE.md) | BirdID tuning |
| [reference/requirements*.txt](reference/requirements_base.txt) | Pip pins (mirror of upstream) |
| [reference/SOURCE.md](reference/SOURCE.md) | Capture metadata, pip quirks |
| [reference/README-INDEX.md](reference/README-INDEX.md) | Index of `reference/` |

## Install

From **`$SKILL`** (or call **`${SKILL}/scripts/install.sh`** by absolute path):

```bash
./scripts/install.sh
"${SKILL}/scripts/install.sh" --with-models
./scripts/install.sh --skip-verify
./scripts/install.sh --no-clone
PY=python3.12 "${SKILL}/scripts/install.sh"
```

1. Python **3.10–3.12** preferred; **`python -m venv`** must work.  
2. **`$SKILL/.upstream/`** + **`$SKILL/.upstream/.venv/`**.  
3. **Torch:** macOS → base + PyPI torch; **NVIDIA + `nvidia-smi`** → `requirements_cuda.txt`; else `requirements.txt` or fallback.  
4. **`verify_environment`** after pip unless `--skip-verify` / `SKIP_VERIFY=1` — failures → `[superpicky-cli verify] ERROR:` and **exit 1**.

## Entry details & examples

Wrapper meta-help: **`${SKILL}/scripts/run.sh --help`**. SuperPicky top-level: **`${SKILL}/scripts/run.sh -h`**.

```bash
"${SKILL}/scripts/run.sh" process /path/to/photos
"${SKILL}/scripts/run.sh" --birdid identify /path/to.jpg
"${SKILL}/scripts/run.sh" --py "${SKILL}/.upstream/scripts/download_models.py"
# Relative --py is OK: resolved against .upstream/, then executed as absolute path
"${SKILL}/scripts/run.sh" --py scripts/download_models.py
```

### `ebird_region_query.py` (entry 3) — `--region-query`

Resolves **country codes** (e.g. `AU`, `CN`) and **region codes** (e.g. `AU-SA`, `CN-31`) for `--birdid-country`, `--birdid-region`, `birdid_cli` `-c`/`-r`, and `process --birdid-*`.

- **Data:** `.upstream/birdid/data/ebird_regions.json` (EN + `name_cn`) + codes from `birdid/avonet_filter.py` **`REGION_BOUNDS`** (inline `#` labels for entries not in JSON).
- **Match:** case-insensitive substring on **code**, **English name**, **Chinese name**; **pinyin** if optional **`pypinyin`** is installed in `.venv` (`pip install pypinyin`). **Fuzzy:** `difflib` ratio on tokens / whole fields; tune with `--min-score` (default `0.5`).

```bash
"${SKILL}/scripts/run.sh" --region-query shanghai
"${SKILL}/scripts/run.sh" --region-query 广东 --limit 10
"${SKILL}/scripts/run.sh" --region-query guangdong
"${SKILL}/scripts/run.sh" --region-query AU-SA
"${SKILL}/scripts/run.sh" --region-query --list-countries --limit 60
"${SKILL}/scripts/run.sh" --region-query --list-all --limit 40
"${SKILL}/scripts/run.sh" --region-query texas --json
```

Direct: **`"${SKILL}/.upstream/.venv/bin/python" "${SKILL}/scripts/ebird_region_query.py" -h`**  
Tests: **`"${SKILL}/.upstream/.venv/bin/python" "${SKILL}/scripts/ebird_region_query_test.py"`**

Manual: **`source "${SKILL}/.upstream/.venv/bin/activate" && cd "${SKILL}/.upstream" && python "${SKILL}/.upstream/superpicky_cli.py" …`**

## Refresh `--help` capture

```bash
"${SKILL}/scripts/capture-cli-help.sh"
```

## Upstream-only install

```bash
git clone https://github.com/jamesphotography/SuperPicky.git && cd SuperPicky
pip install -r requirements.txt   # or requirements_cuda.txt
python scripts/download_models.py
```

Repo **cwd** = clone root. **Models** needed for real `process` / `identify`, not for `-h`. Pip quirks: [reference/SOURCE.md](reference/SOURCE.md).

---

## `superpicky_cli.py` (entry 1)

**Via skill:** **`"${SKILL}/scripts/run.sh" …`** (no `--birdid` / `--region-query` prefix)  
**Subcommands:** `process` | `reset` | `restar` | `info` | `burst` | `identify`  
**Flags:** [reference/cli-help-captured.txt](reference/cli-help-captured.txt)

`process`: `-s` sharpness, `-n` TOPIQ, `-c` confidence, `--flight`/`--no-flight`, `--burst`/`--no-burst`, `--xmp`/`--no-xmp`, `--no-organize`, `--no-cleanup`, `-q`, `-i` / `--auto-identify`, `--birdid-*`, `--keep-temp-files` / `--no-keep-temp-files`, `--cleanup-days`, `--save-crop`.  
`reset` / `restar`: `-y`; `restar` needs `.superpicky/report.db`.  
`burst`: preview unless `--execute`.  
`identify`: single image, `--top`, `--write-exif`, etc.

## `birdid_cli.py` (entry 2)

**Via skill:** **`"${SKILL}/scripts/run.sh" --birdid …`**  
Subcommands: `identify` | `organize` | `reset` | `list-countries` — details in **cli-help-captured.txt** (search `birdid_cli`).

---

## Agent checklist

1. Resolve **`$SKILL`** to an absolute directory; invoke **`"${SKILL}/scripts/run.sh"`** (and **`install.sh`**) by **full path**, not `./scripts/...`.  
2. **`"${SKILL}/scripts/install.sh"`** if `.upstream/.venv` missing.  
3. **`"${SKILL}/scripts/run.sh" --region-query …`** when the user gives a place name and you need an eBird **`-c` / `-r` / `--birdid-region`** code.  
4. **`-y`** on destructive `reset` / `restar` / birdid organize|reset when appropriate.  
5. **Pipeline:** `process` → optional `restar`; `reset` clears; `restar` needs `report.db`.  
6. Star folder names: English + Chinese variants in upstream.
