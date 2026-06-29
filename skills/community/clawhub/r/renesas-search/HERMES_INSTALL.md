# Hermes Install — Cross-Platform Adapter

The `renesas-search` skill is written for **OpenClaw** but is also compatible with **Hermes Agent** (and the broader [agentskills.io](https://agentskills.io/specification) open standard). This file documents the small differences and how to install on each platform.

## Compatibility

| Platform | Skill format | Status |
|----------|--------------|--------|
| **OpenClaw** | `~/.openclaw/workspace/skills/renesas-search/SKILL.md` | ✅ Native |
| **ClawHub** | (any OpenClaw user) | ✅ Published as `renesas-search` v3.0.4 |
| **Hermes Agent** | `~/.hermes/skills/<category>/<name>/SKILL.md` | ✅ Adapter below |
| **agentskills.io** (Anthropic, NVIDIA, …) | local install of SKILL.md | ✅ Compatible |

## SKILL.md Frontmatter

The same `SKILL.md` is used everywhere. The frontmatter has fields for both ecosystems:

```yaml
---
name: renesas-search
description: >
  Search and recommend Renesas semiconductor solutions...
  # OpenClaw reads this

version: 3.0.4           # Hermes / agentskills.io
author: Peter (wangp-gh) # Hermes / agentskills.io
license: MIT             # Hermes / agentskills.io
platforms: [linux, macos, windows]  # Hermes (top-level)
metadata:
  hermes:
    category: research   # Hermes — only field required for Hub browsing
    tags: [Renesas, semiconductor, datasheet, BLE, MCU, ...]
    related_skills: []
  # OpenClaw ignores everything below 'metadata'
  # Hermes ignores everything above 'metadata'
```

### Field-by-field

| Field | OpenClaw | Hermes | agentskills.io |
|-------|----------|--------|----------------|
| `name` | required | required | required |
| `description` | required | required | required |
| `version` | ignored | required | recommended |
| `author` | ignored | recommended | recommended |
| `license` | ignored | recommended | recommended |
| `platforms` (top-level) | ignored | respected | respected |
| `metadata.hermes.category` | ignored | **required for Hub** | n/a |
| `metadata.hermes.tags` | ignored | respected | n/a |
| `metadata.hermes.related_skills` | ignored | respected | n/a |
| `metadata.openclaw` (optional) | respected | ignored | n/a |

A future `metadata.agentskills_io` block would let you add `version`, `license`, and other spec-required fields once that spec stabilizes.

## Hermes — Two install paths

### Path A: From a git URL (single command)

Hermes' `hermes skills install` accepts HTTPS URLs to a SKILL.md file. Because the file lives at `skills/<category>/<name>/SKILL.md`, point Hermes at the GitHub raw URL:

```bash
# Note: category 'research' must match the frontmatter.
hermes skills install https://raw.githubusercontent.com/wangp-gh/renesas-search/main/SKILL.md --category research
```

This downloads `SKILL.md` and places it at `~/.hermes/skills/research/renesas-search/SKILL.md`.

### Path B: Manual clone (preserves references/)

The skill ships with `references/product_families.md` and `TEST_SCENARIOS.md`. The manual path keeps them intact:

```bash
git clone https://github.com/wangp-gh/renesas-search.git /tmp/renesas-search
mkdir -p ~/.hermes/skills/hardware
cp -r /tmp/renesas-search ~/.hermes/skills/hardware/renesas-search
# Copy only the skill files you want:
cp ~/.hermes/skills/hardware/renesas-search/SKILL.md ~/.hermes/skills/hardware/renesas-search/SKILL.md
cp -r ~/.hermes/skills/hardware/renesas-search/references ~/.hermes/skills/hardware/renesas-search/

# Optional: include test scenarios for verification
cp ~/.hermes/skills/hardware/renesas-search/TEST_SCENARIOS.md ~/.hermes/skills/hardware/renesas-search/
```

Then start a new Hermes session; the skill should appear in `/skills list` under the **research** category.

### Path C: From the agentskills.io directory (when listed)

Once the skill is published on agentskills.io, install with:

```bash
hermes skills install official/hardware/renesas-search
```

(Path C requires a separate submission to the agentskills.io directory; not yet done as of v3.0.4.)

## Verifying on Hermes

After install:

```bash
hermes skills list | grep renesas
# Expected: renesas-search    Search and recommend Renesas semiconductor solutions...

hermes skills info renesas-search
# Should show: category: research, version: 3.0.4, platforms: linux,macos,windows
```

In chat:

```
/renesas-search What is the supply current of ISL88013?
```

The skill should activate (because ISL88013 is a Renesas product family) and download the datasheet, then answer with a Typ-only, page-cited response.

## If the Category Is Wrong

Hermes uses `metadata.hermes.category` (or the path under `skills/<category>/`) to decide which "official/<category>/..." path to install to. To change the category:

1. Edit `SKILL.md` and update `metadata.hermes.category`.
2. Re-run `hermes skills install <url> --category <new-category>`.

Valid categories observed in the Hermes bundled catalog: `apple`, `autonomous-ai-agents`, `creative`, `devops`, `media`, `mlops`, `productivity`, `research`, `software-development`. If your skill does not fit any, leave it unset and Hermes will install it as a top-level skill without a category.

For renesas-search, **hardware** is the closest fit — it is a hardware selection / datasheet-driven engineering skill, not a content-creation or DevOps tool. If your local Hermes catalog does not yet list `hardware` as a valid category, the installer will fall back to a top-level install (the skill still works, it just won't appear under a category bucket).

## Notes on the Hermes Security Scan

Hermes' `Curator` system sandboxes skills installed from external sources (Hub, GitHub, etc.) for safety. `renesas-search` is a read-only documentation skill — it only fetches datasheets and renders tables — so it should pass the scan without issues. The skill does **not** execute arbitrary code, write outside `embedded_dev/`, or modify the agent's core behavior.
