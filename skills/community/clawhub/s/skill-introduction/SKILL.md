---
name: skill-introduction
description: >
  Generate a beautiful, deployable HTML introduction page for any AgentSkill.
  Reads USAGE.md (preferred) or SKILL.md, parses name, description, and feature
  sections, then renders a polished page with a hero section, feature cards,
  quick start, command examples, collapsible doc cards, side navigation, and a
  floating install button. Supports 4 themes: light (default), aurora (dark
  glass), techblue (debug-tool style), finance (dark blue + gold). Optionally
  deploys via a pluggable hook so re-runs update the same URL. Use when the
  user says "generate a skill intro page", "make a doc page for this skill",
  "publish this skill's docs", "skill-introduction". If the user does not
  specify a target skill, ask them for the skill name or directory path.
---

# skill-introduction

- **Version**: 1.0.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/skill-introduction

Auto-generate a polished HTML introduction page from a skill's `USAGE.md` or `SKILL.md`. Four themes, optional deploy hook, re-runs update the same URL.

## Quick Start

### Generate only (no deploy)

```bash
python3 scripts/generate_html.py --skill-dir <path-to-skill> --no-deploy
```

Outputs to `./output/<slug>-intro.html` (override with `--output`).

### Specify author

```bash
python3 scripts/generate_html.py --skill-dir <path> --author "Jane Doe"
```

Author resolution order: `--author` → `SKILL_INTRO_AUTHOR` env → `git config --global user.name` → `$USER`.

### Pick a theme

```bash
python3 scripts/generate_html.py --skill-dir <path> --theme aurora
```

Themes: `light` (default), `aurora` (dark glass), `techblue` (debug-tool), `finance` (dark blue + gold).

### Use a specific source file

```bash
python3 scripts/generate_html.py --skill-dir <path> --source USAGE.md
```

Default resolution: `--source` > `USAGE.md` > `SKILL.md` (fallback with notice).

### Custom subtitle (recommended)

```bash
python3 scripts/generate_html.py --skill-dir <path> \
  --subtitle "Beautiful, deployable HTML docs for your skill"
```

Without `--subtitle`, the page truncates the long `description` field — usually ugly. Always pass a one-liner.

## Generated Page Layout

| Region | Content |
|--------|---------|
| Hero | Skill name, subtitle, trigger tags, install/docs buttons |
| Highlights | Auto-extracted from `##` sections, up to 6 cards (hidden if none) |
| Features | Colored top-border cards, 3-col grid, up to 6 (hidden if none) |
| Quick Start | Tabs: user steps + terminal commands |
| Detailed Docs | Tabs: collapsible doc cards grouped by `h2` |
| Roadmap | Shown only if source has "roadmap/plan/future/todo" sections |
| Known Issues | Extracted from "notes/issues/limitations/known" sections |
| Footer | Skill name · maintainer · last updated |
| Side nav | Right-fixed, scroll-spy highlight |
| Floating install | Bottom-right, links to install URL |

## Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `--skill-dir` | Target skill directory (required) | — |
| `--output` | Output HTML path | `./output/<name>-intro.html` |
| `--no-deploy` | Generate only, skip deploy | deploy if hook configured |
| `--hub-url` | Install button URL | `https://clawhub.com/skill/<slug>` |
| `--author` | Maintainer name | resolved from env/git/$USER |
| `--update-id` | Force-update specific dashboard id | from cache |
| `--theme` | `light` / `aurora` / `techblue` / `finance` | `light` |
| `--source` | Source md file (relative or absolute) | auto USAGE.md > SKILL.md |
| `--subtitle` | Hero subtitle one-liner | truncates `description` |

## Source Selection (important)

Selection order:

1. `--source` (explicit)
2. `USAGE.md` in skill dir (**recommended**, user-facing)
3. `SKILL.md` (fallback)

> ⚠️ `SKILL.md` is written for **AI trigger matching** (contains technical triggers, "when the user says…" phrasing). Rendering it directly to humans looks technical.
> If falling back to `SKILL.md`, the page shows a notice at the top and the terminal prints `[WARN]`. Add a `USAGE.md` for a polished user-facing page.
> Never soften `SKILL.md`'s description to make it pretty — that breaks AI trigger matching.

## Subtitle (agents: do this)

The hero subtitle should be a **one-liner pitch**, not raw `description`. Descriptions are long (contain triggers + technical detail); truncating to 130 chars + `...` looks bad.

**Agents: read the skill, craft a concise pitch, pass it via `--subtitle`.**

Examples:
- ❌ Truncated: `Generate a beautiful, deployable HTML introduction page for any AgentSkill. Reads USAGE.md (preferred) or SKILL.md, parses name...`
- ✅ One-liner: `Beautiful, deployable HTML docs for your skill in one command`

## Rendering Engine

Block-level markdown (tables / nested lists / blockquotes / hr) is rendered by vendored `mistune` (BSD-3-Clause, in `vendor/mistune/`, ships with the skill, pure Python). If `vendor/` is missing the script falls back to a built-in regex renderer — no crash, just simpler output.

## Cache

After successful deploy, the dashboard id is cached so subsequent runs auto-update the same URL.

| Setting | Default | Override |
|---------|---------|----------|
| Cache file | `~/.cache/skill-introduction/cache.json` | `SKILL_INTRO_CACHE` env |
| Author | env > git > $USER | `SKILL_INTRO_AUTHOR` env |
| Deploy hook | none | `SKILL_INTRO_DEPLOY_CMD` env (see below) |

## Deploy Hook (optional)

The skill does not bind to any hosting platform. To enable deploy, set `SKILL_INTRO_DEPLOY_CMD` to a script/command that:

1. Accepts the HTML file path as `$1`
2. (Optional) reads `SKILL_INTRO_UPDATE_ID` env when updating an existing page
3. Prints the deployed URL (containing `dashboardId=<32hex>`) on stdout to enable cache-based updates

```bash
export SKILL_INTRO_DEPLOY_CMD="/path/to/my-deploy.sh"
python3 scripts/generate_html.py --skill-dir <path>
```

If no hook is configured, the skill prints `[INFO] No deploy hook configured` and leaves the local HTML untouched.

## Notes

- Target skill must have `USAGE.md` or `SKILL.md` or the script exits with an error.
- Generated page quality depends on source structure: clearer sections → prettier page.
- Empty sections (highlights / features / roadmap) are hidden — no fake content.
- If the user does not provide a skill path, ask them; do not auto-guess.

## Third-party Notice

- `vendor/mistune/` — [mistune](https://github.com/lepture/mistune) v3.x, BSD-3-Clause License, © Hsiaoming Yang. Vendored unmodified for offline rendering.
