---
name: self-improving-to-expertpack
description: "Convert Self-Improving Agent learnings into a structured ExpertPack. Migrates the .learnings/ directory (LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md) and any promoted content from workspace files into ExpertPack's portable format with multi-layer retrieval, context tiers, and EK measurement. Output is Obsidian-compatible — includes YAML frontmatter on all content files and can be opened as an Obsidian vault. Use when: upgrading from Self-Improving Agent to ExpertPack, backing up agent learnings, exporting accumulated knowledge, or migrating to a new platform. Triggers on: 'self-improving to expertpack', 'convert self-improving', 'export learnings', 'migrate self-improving', 'learnings to expertpack', 'convert learnings to pack'."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# Self-Improving Agent → ExpertPack

Converts a **Self-Improving Agent** skill's `.learnings/` directory (3.8K ClawHub installs) into a properly structured **ExpertPack**.

**Supported sources:**

- **LEARNINGS.md** — corrections, knowledge gaps, best practices, simplify-and-harden patterns
- **ERRORS.md** — command failures, exceptions, integration issues
- **FEATURE_REQUESTS.md** — user-requested capabilities and implementation notes
- **Promoted content** — entries already promoted to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md (detected and cross-referenced)

## Usage

```bash
cd /root/.openclaw/workspace/ExpertPack/skills/self-improving-to-expertpack
python3 scripts/convert.py \
  --workspace /path/to/your/workspace \
  --output ~/expertpacks/my-learnings-pack \
  [--name "My Agent's Learnings"] \
  [--type auto|person|agent|process]
```

Override `.learnings/` location with `--learnings /path/to/.learnings`.

## What It Produces

A complete ExpertPack conforming to schema 2.3:

- `manifest.yaml` (with context tiers, EK stub)
- `overview.md` summarizing conversion (entry counts, categories, priority breakdown)
- Structured directories mapped from learning types:
  - `mind/` — best practices, conventions, behavioral patterns, promoted rules
  - `facts/` — knowledge gaps filled, project-specific facts
  - `operational/` — error resolutions, tool gotchas, integration fixes
  - `summaries/` — pattern analyses, recurring issue summaries
  - `relationships/` — cross-references between related entries
- `_index.md` files, lead summaries, `glossary.md` (if terms/tags found)
- `relations.yaml` (from See Also links and shared tags)
- Clean deduplication preferring promoted > resolved > pending entries

**Secrets are automatically stripped** (sk-*, ghp_*, tokens, passwords). Warnings emitted for any found.

## Post-Conversion Steps

1. `cd ~/expertpacks/my-learnings-pack`
2. Verify content files are 400–800 tokens each (Schema 2.5 — retrieval-ready by design)
3. Measure EK ratio: `python3 /path/to/expertpack/tools/eval-ek.py .`
4. Review `overview.md` and `manifest.yaml`
5. Commit to git and publish to ClawHub

**Learn more:** https://expertpack.ai • ClawHub [expertpack skill](https://clawhub.com/skills/expertpack)

**See also:** Self-Improving Agent skill on ClawHub.
