# OpenClaw Skill Classification & Statistics

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.6-orange.svg)](CHANGELOG.md)
[![CI](https://github.com/kuntao2011/openclaw-skill-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/kuntao2011/openclaw-skill-manager/actions/workflows/ci.yml)

**English** | [简体中文](README.zh-CN.md)

> Enhanced OpenClaw skill inventory generator with a modular architecture, multiple export formats, and advanced features.

## ✨ Features

### Core
- ✅ **Multi-format export**: Markdown / JSON / HTML
- ✅ **Classification stats**: auto-classification into 10 categories / 48 subcategories, with user-defined overlay
- ✅ **Status icons**: ✅ Ready / ⚠️ NeedSetup / ❌ Disabled
- ✅ **Metadata**: version, author, emoji, source, homepage link
- ✅ **Interactive HTML report**: sortable/filterable static page (no server required)

### Advanced
- 🔄 **Incremental update**: compare against the last snapshot and export only what changed
- 🤖 **Auto-classification**: rule-based categorization for new skills
- 🔍 **Duplicate detection**: name patterns + description similarity (SequenceMatcher)
- 🎯 **Flexible filters**: by status, keyword, and category
- 📦 **Status detection**: detects missing dependencies (incl. `anyBins` groups) from the OpenClaw CLI
- 🌍 **Description Sinicization**: built-in glossary replaces common English phrases, with an untranslated-words report
- 📊 **Usage stats**: dual data source — `skill_usage` table / curator (`--usage`)
- 🔗 **Dependency graph**: missing-dependency edges as mermaid (md) and SVG bipartite chart (html) (`--deps`)
- 🔁 **Batch enable/disable**: writes `skills.entries.<name>.enabled` with auto-backup and post-write verification
- ⬆️ **Update check**: git track vs remote HEAD, ClawHub track hint — report only, never auto-upgrades (`--check-updates`)
- 📤 **Remote push**: opt-in push of exported Markdown to Feishu Docs / Notion pages (`--push`; prints a privacy notice before sending)

## 🏗️ Architecture

```
openclaw-skill-manager/
├── data/                      # data layer (CLI wrapper, stats, deps, updates, toggle)
├── classifier/                # classification layer (category map, overlay, duplicates)
├── exporter/                  # export layer (Markdown/JSON/HTML/Feishu/Notion)
├── utils/                     # utilities (config, glossary, diff, HTTP client)
├── tests/                     # pytest unit tests
├── generate_skill_list.py     # main entry
└── __init__.py                # package definition
```

## 🚀 Quick Start

### Requirements
- Python 3.8+
- OpenClaw installed and configured

### Install

1. Via the OpenClaw skill installer (recommended):
```bash
openclaw skills install git:https://github.com/kuntao2011/openclaw-skill-manager
```

2. Or clone manually into the OpenClaw skills directory:
```bash
git clone https://github.com/kuntao2011/openclaw-skill-manager
cp -r openclaw-skill-manager ~/.openclaw/workspace/skills/
```

### Usage

#### Basics
```bash
cd ~/.openclaw/workspace/skills/openclaw-skill-manager
python3 generate_skill_list.py
```

#### Output formats
```bash
# Markdown (default)
python3 generate_skill_list.py -f markdown

# JSON
python3 generate_skill_list.py -f json

# HTML (interactive UI)
python3 generate_skill_list.py -f html

# All formats
python3 generate_skill_list.py -f all
```

#### Filters
```bash
# Activated skills only
python3 generate_skill_list.py -F activated

# Not-activated skills only
python3 generate_skill_list.py -F not_activated

# Search by keyword
python3 generate_skill_list.py -s "tavily"

# Filter by category
python3 generate_skill_list.py -c "开发工具"
```

#### Advanced options
```bash
# Incremental update (only changes)
python3 generate_skill_list.py -i

# Detect duplicate skills
python3 generate_skill_list.py --check-duplicates

# Custom output directory (created automatically)
python3 generate_skill_list.py -o /path/to/output

# Quiet mode
python3 generate_skill_list.py -q

# Usage-count column
python3 generate_skill_list.py --usage

# Missing-dependency graph
python3 generate_skill_list.py --deps

# Untranslated-words report
python3 generate_skill_list.py --i18n-report

# Update check (report only, never upgrades)
python3 generate_skill_list.py --check-updates

# Batch enable/disable (auto-backup + CLI verification)
python3 generate_skill_list.py --disable skill-a,skill-b
python3 generate_skill_list.py --enable skill-a

# Push exported Markdown to Feishu / Notion
python3 generate_skill_list.py -f all --push feishu,notion
```

## 🔐 Remote-push credentials (environment variables only)

| Target | Required | Optional |
|--------|----------|----------|
| Feishu | `FEISHU_APP_ID`, `FEISHU_APP_SECRET` | `FEISHU_FOLDER_TOKEN` (defaults to the root of My Space) |
| Notion | `NOTION_TOKEN`, `NOTION_PAGE_ID` | — |

Credentials are read exclusively from environment variables; no credential literals may ever be committed to this repository.

> ⚠️ **Privacy notice**: pushing transmits your skill inventory (names, descriptions, sources, usage counts) to the third-party service you choose. It only runs when `--push` is passed explicitly and prints a warning first; avoid it in sensitive environments. Network scope: Feishu/Notion APIs (code-level host allowlist, HTTPS enforced) plus `git ls-remote` against the git remote recorded in each skill's install metadata for `--check-updates`.

## ⚙️ Configuration

### Output directory

Edit `utils/config.py`:

```python
# Default output directory
OUTPUT_DIR = os.path.join(USER_PROFILE, 'openclaw_out')

# Or another directory
# OUTPUT_DIR = '/your/custom/path'
```

Or pass it on the command line:
```bash
python3 generate_skill_list.py -o ~/my_skills
```

### Custom category overlay

Create `~/.openclaw/skill_categories.json` (takes precedence over the built-in map):

```json
{
  "my-skill": ["开发工具", "编码与开发"]
}
```

## 📊 Output example

> Excerpt from a real run (2026-09-25, 64 skills on this machine: 31 ✅ / 5 ⚠️ / 28 ❌). Long descriptions are whitespace-flattened and truncated at 120 chars in the table; full text lives in JSON/HTML.

```
| # | Status | Skill | Version | Source | Calls | Description |
|---|--------|-------|---------|--------|-------|-------------|
| 1 | ✅ | [☔ weather](https://wttr.in/:help) | | bundled | - | Current weather and forecasts with web_fetch, falling back to wttr.in curl for locations, rain, temperature, travel plan… |
| 2 | ✅ | healthcheck | | bundled | - | Audit/harden OpenClaw hosts: SSH, firewall, updates, exposure, backups, disk encryption, gateway security. |
| 3 | ❌ | [🔐 1password](https://developer.1password.com/docs/cli/get-started/) | | bundled | - | 设置和使用 1Password CLI for sign-in, desktop integration, and reading or injecting secrets. |
```

### HTML UI
- 🔍 Live search over names and descriptions
- 📂 Category filter + status filter
- 🔃 Click-to-sort headers (name/version/source/calls/category)
- 🔗 Missing-dependency SVG bipartite chart
- 📈 Live stats panel
- 🎨 Responsive layout for desktop and mobile

## 📁 Output files

- `activated-skills.md` — Markdown list of activated skills (`已激活技能列表.md`)
- `not-activated-skills.md` — Markdown list of not-activated skills (`未激活技能列表.md`)
- `技能列表.json` — full structured JSON (incl. usage / dependency_edges)
- `已激活技能列表.html` — interactive HTML page
- `未激活技能列表.html` — interactive HTML page
- `未汉化词表.txt` — generated with `--i18n-report`

## 🧪 Development & testing

```bash
python3 -m pytest -q          # 47 unit tests
python3 -m compileall -q classifier data exporter utils generate_skill_list.py __init__.py
```

GitHub Actions runs compile checks + pytest (Python 3.9 / 3.12) on every push.

## 📝 Notes

1. First run creates the output directory and the cache directory `~/.openclaw/cache/skill_list/`
2. Incremental update (`-i`) relies on the snapshot saved by the previous run; `--no-snapshot` skips saving
3. The classification rules are tailored to the author's personal skill library; third-party skills mostly fall into "Other" — extend via the overlay file or `classifier/category_map.py`
4. Batch enable/disable modifies `~/.openclaw/openclaw.json`; a timestamped backup is created before every change
5. Usage stats depend on OpenClaw's `skill_usage` records; a `-` placeholder is shown when no data exists
6. No persistence mechanisms: no cron jobs, no startup hooks — snapshots and the category overlay are plain data files
7. CLI output and category labels are in Chinese by design (see `metadata.language: zh-CN`)

## 🤝 Contributing

Issues and pull requests are welcome!

## 👤 Author

**kuntao2011** ([GitHub @kuntao2011](https://github.com/kuntao2011))

## 📄 License

MIT — see [LICENSE](LICENSE).

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md).
