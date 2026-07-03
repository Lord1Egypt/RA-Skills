---
name: token-slim
description: >
  Guided token optimization for AI agent workspaces. Triggers on phrases like
  "save tokens", "optimize tokens", "context window too large", "memory files
  too big", "scan my workspace", "trim workspace", "find token waste", "再扫一下",
  "帮我省 Token", "优化 Token 使用", "上下文太长了", "内存文件太大", "还有哪里可以优化".
  Also handles brutal-mode toggle: "enable brutal mode", "disable brutal mode",
  "开启狂暴模式", "关闭狂暴模式". On first use walks the user step-by-step through
  workspace cleanup; supports on-demand re-scans at any time. Works on OpenClaw,
  Claude Code, and any agent runtime with a writable working directory.
---

# Token Saver (token-slim)

- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills
- **License**: MIT

Helps AI agents and their users reduce token consumption by auditing workspace
files, identifying bloat, and guiding targeted cleanup.

## Core Concept

Every project-context file (memory index, agent config, heartbeat, etc.) is
injected into **every single session**. Keeping them lean = direct,
compounding savings. The goal is a three-tier memory layout:

```
memory index        ← always loaded, < 150 lines — pointers + essentials only
memoryres/*.md      ← loaded on demand — reference tables, specs, backlogs
memory/YYYY-MM-DD.md ← raw daily log — rarely loaded
```

For full strategy details: see `references/strategies.md`

---

## Mode Routing

After matching a mode, **first `read` the corresponding reference file**, then
follow that flow. Do not rely on memory.

| User intent | Mode | Must read first |
|---|---|---|
| First-time setup / "save tokens" | **Mode A** | `references/mode-a-onboarding.md` |
| Re-scan / "scan again" / "what else can I optimize" | **Mode B** | `references/mode-b-rescan.md` |
| Toggle brutal mode | **Brutal Mode** | see section below |

---

## Execution Modes

### Confirm mode (default)
Show each proposed change, wait for user approval before modifying.

### Batch mode
Triggered when the user says "just do it" / "按你说的来" / "全部做". Execute all
changes without per-item confirmation; deliver a unified summary at the end.

### Dry-run mode
Preview without modifying any files:
```bash
SKILL_DIR="$(dirname "$(readlink -f "$0")")/skills/token-slim" 2>/dev/null \
  || SKILL_DIR=./skills/token-slim
python3 "$SKILL_DIR/scripts/scan_workspace.py" --workspace . --dry-run
```

Or simply, from the workspace root:
```bash
python3 <skill-install-path>/scripts/scan_workspace.py --workspace . --dry-run
```

---

## 🔥 Brutal Mode — Toggle

**Triggers:**
- Enable: "enable brutal mode" / "开启狂暴模式" / "打开狂暴模式"
- Disable: "disable brutal mode" / "关闭狂暴模式" / "退出狂暴模式"

**Enable flow:**
1. Check the workspace agent config file for `<!-- token-slim:token-habits-start -->` anchor
2. If absent → append the full template (incl. brutal mode section — see `references/mode-a-onboarding.md` Step 8)
3. If present → replace the whole block with the full template
4. Reply: "🔥 Brutal mode enabled — concise outputs, no preamble."

**Disable flow:**
1. Find the block `<!-- token-slim:token-habits-start -->` … `<!-- token-slim:token-habits-end -->` in the agent config
2. Replace the brutal-mode section with just a header placeholder:
   ```
   ### 🔥 Brutal Mode (max output efficiency) <!-- Brutal mode: disabled -->
   ```
3. Reply: "✅ Brutal mode disabled — back to normal."

**First-time use (after Mode A Step 8 completes):**
Proactively offer:
> "🔥 Want to enable **brutal mode**? When on, the agent gives results only — no
> step-by-step narration. Saves tokens and reading time. Say 'enable brutal mode'
> to toggle (can be turned off anytime)."

---

## Undo (rollback)

`scan_workspace.py` itself does not modify files and does not auto-backup.

**Before any file modification the agent must:**
1. Tell the user which files will be modified
2. Ask "Do you want me to back these up first?"
3. On confirmation, copy the soon-to-be-modified files to a timestamped dir:
   ```
   <workspace>/.token-slim/undo-<YYYYMMDD-HHMMSS>/
   ```
4. Report the backup path so the user can restore later.

See `references/mode-a-onboarding.md` Step 3 for the canonical recipe.

---

## tiktoken installation

token-slim uses **tiktoken** for accurate token counting (vs ~40-60% heuristic
error). Install attempts run in this order with automatic fallback:

```bash
python3 <skill-install-path>/scripts/install_tiktoken.py --workspace .
```

| Step | Source | Notes |
|------|--------|-------|
| 1 | PyPI official (pypi.org) | 2 retries |
| 2 | Tsinghua mirror | China-region acceleration |
| 3 | Aliyun mirror | China-region acceleration |
| 4 | Heuristic fallback | CJK/ASCII split, ~40-60% error |

**BPE vocabulary cache** is fetched automatically by tiktoken on first encode
from the OpenAI public blob (`openaipublic.blob.core.windows.net`) and stored
under `<workspace>/.cache/tiktoken/` (CWD-anchored — survives `$HOME` wipes on
container/VM environments where only the working directory is persistent).

**Check current state:**
```bash
python3 <skill-install-path>/scripts/install_tiktoken.py --check --workspace .
```

`scan_workspace.py` auto-detects tiktoken at runtime; no manual setup needed
after installation.

---

## Dependencies

**Required:**
- Python 3.8+ (`python3` available on PATH)

**Optional:**
- `tiktoken` for precise token counting (install via the script above). Without
  it, the scanner uses a CJK/ASCII heuristic with ~40-60% error.

Everything else uses the Python standard library.

---

## What NOT to move

Never suggest moving:
- Behavioural rules, safety constraints, must/never guidelines
- Cron job configurations and failure protocols
- Active heartbeat tasks and retry queues
- Identity / persona core (soul/identity config content)
- Anything with ⚠️ or explicit "always loaded" markers

When in doubt, ask the user.

---

## Key files

| File | Purpose |
|------|---------|
| `scripts/scan_workspace.py` | Scanner — detects bloat, scores findings, supports `--dry-run` |
| `scripts/install_tiktoken.py` | tiktoken installer (PyPI → Tsinghua → Aliyun → heuristic) |
| `references/strategies.md` | Full strategy reference (7 strategies + scoring rubric) |
| `references/mode-a-onboarding.md` | Mode A: first-time setup workflow |
| `references/mode-b-rescan.md` | Mode B: on-demand re-scan workflow |

---

## CLI reference

### `scan_workspace.py`

```
python3 scan_workspace.py [--workspace <path>] [--json] [--dry-run]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--workspace` | `$TOKEN_SLIM_WORKSPACE` or current directory | Workspace root to scan |
| `--json` | off | Output raw JSON instead of human-readable report |
| `--dry-run` | off | Preview mode: show what would change, modify nothing |

### `install_tiktoken.py`

```
python3 install_tiktoken.py [--check] [--workspace <path>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--check` | off | Only report install/cache status; do not install |
| `--workspace` | current directory | Cache goes to `<workspace>/.cache/tiktoken`. Honoured only if `TIKTOKEN_CACHE_DIR` is unset |

---

## ⚠️ Skills vs workspace-file tokens

**Skills (SKILL.md)**: each skill injects only its `name + description + location`
per session — around **24 tokens**. The full body is only loaded when the agent
explicitly `read`s it. Large SKILL.md files affect call latency, not per-session
baseline.

**Workspace files (memory index, agent config, etc.)**: injected verbatim every
session — these are the real optimisation target.
