---
name: radxa-local-docs
description: "Use when one Radxa skill should cover the full offline documentation workflow: detect the current board model, map it to the correct product series, deploy or update the local MDMaker documentation mirror under ~/.openclaw/MDMaker, and query board-specific offline docs before coding, debugging, or hardware operations."
---

# Radxa Local Docs

## Purpose

Combine the previous `device-info`, `mdmaker-deploy`, and `radxa-doc` capabilities into one publishable skill.

## Use Bundled Resources

- Run `scripts/detect_device.sh` to detect the current device model with Device Tree, DMI, hostname, and `/proc/cpuinfo` fallbacks.
- Read `references/device-series-map.md` when a detected or user-provided model must be mapped to a Radxa product series.

## Workflow

1. Detect the current board model first.
2. If detection fails or the host is not a Radxa board, fall back to the user-provided model name instead of guessing.
3. Map the board model to a Radxa series with `references/device-series-map.md`.
4. Check whether the local documentation mirror already exists under `~/.openclaw/MDMaker/dist/zh/` or `~/.openclaw/MDMaker/dist/en/`.
5. If the user asks to deploy or update docs, use the MDMaker workflow below.
6. If the user asks a documentation question, locate the right language directory, product series, model directory, and topic-specific markdown file before answering.

## MDMaker Workflow

### Deploy

```bash
cd ~/.openclaw
git clone -b agent https://github.com/ZIFENG278/MDMaker.git
cd ~/.openclaw/MDMaker
python3 -m venv venv
source venv/bin/activate
pip install requests tqdm
python build_md_docs.py
```

### Raw Docs Source

Prefer the upstream GitHub source first. Only fall back to the domestic GitCode mirror if GitHub clone or pull fails.

Primary source:

```bash
git clone https://github.com/radxa-docs/docs.git ~/.openclaw/MDMaker/radxa-docs
```

Fallback source:

```bash
git clone https://gitcode.com/radxa-docs/docs.git ~/.openclaw/MDMaker/radxa-docs
```

If `~/.openclaw/MDMaker/radxa-docs/` already exists and GitHub access fails, switch the existing repo to GitCode and retry:

```bash
cd ~/.openclaw/MDMaker/radxa-docs
git remote set-url origin https://gitcode.com/radxa-docs/docs.git
git pull
```

### Update

```bash
cd ~/.openclaw/MDMaker
source venv/bin/activate
python update_md_docs.py
```

### Expected Paths

- Project root: `~/.openclaw/MDMaker/`
- Source repo: `~/.openclaw/MDMaker/radxa-docs/`
- Primary upstream: `https://github.com/radxa-docs/docs.git`
- Domestic upstream mirror: `https://gitcode.com/radxa-docs/docs.git`
- Chinese docs: `~/.openclaw/MDMaker/dist/zh/`
- English docs: `~/.openclaw/MDMaker/dist/en/`

If the mirror is missing and the user did not ask to deploy it, report that the prerequisite is missing instead of fabricating documentation answers.

## Offline Query Workflow

### Directory Selection

- Choose `zh/` or `en/` first.
- Then enter `dist/<lang>/<series>/<model>/`.
- Common sections include `getting-started`, `hardware-design`, `low-level-dev`, `os-config`, `radxa-os`, `other-os`, `app-development`, and `apps-deployment`.

### Search Strategy

Prefer targeted file discovery over broad scans:

```bash
find ~/.openclaw/MDMaker/dist/<lang>/<series>/<model> -name "*<keyword>*.md"
rg -n "<keyword>" ~/.openclaw/MDMaker/dist/<lang>/<series>/<model>
```

Use `hardware-design` for pinouts, interfaces, power, and schematic-adjacent questions.
Use `getting-started` and `os-config` for installation, boot, networking, and system setup.
Use `low-level-dev` for bootloader, Device Tree, and low-level platform details.
Use `app-development` and `apps-deployment` for software stacks and deployment topics.

## Relative Link Handling

When a document contains relative `.md` links with `../`, normalize the link against the current document path, then open the resolved file under the same `dist/<lang>/` tree.

## Output Rules

- Quote concrete file paths when citing local documentation.
- State clearly when the answer is confirmed from local docs versus inferred from model mapping.
- If multiple boards fit the same series, ask or infer only from explicit evidence such as detection output or the user’s board name.

## Safety

- Do not assume a board model without evidence.
- Do not perform flashing, partitioning, bootloader overwrite, or EEPROM changes as part of this skill.
- Keep commands low-risk unless the user explicitly asks for deployment or update actions.
