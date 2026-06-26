# SEO Expert (OpenClaw skill)

**Bundle version:** 1.3.1 (see `SKILL.md` `metadata.version`).

**Skill id / folder / ClawHub slug:** `seo-expert-pro`  
**ClawHub listing title:** e.g. **`clawhub publish --name "SEO Expert"`** (see [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)). Maintainer flow: **`docs/openclaw-seo/`** (see below).

## Content

- **`01_seo_grundlagen.md`**, **`02_crawling_indexierung.md`**, **`04_monitoring_fehlerbehebung.md`** — German excerpts (sources in file header); sync from `____ablage/` when updated.
- **`03_ranking_darstellung.md`** — hub (TOC only) + **seven** parts `03.1`–`03.7`. Regenerate via `python3 scripts/seo_skill/split_ranking_darstellung.py` (`--verify`).
- **`05_webspezifische_leitfaeden.md`** — hub + **eight** parts `05.1`–`05.8`. Regenerate via `python3 scripts/seo_skill/split_webspezifische_leitfaeden.py` (`--verify`).

## Package for ClawHub

From monorepo root:

```bash
./scripts/package-seo-expert-for-clawhub.sh
```

Output: **`build/clawhub-publish/seo-expert-pro`**. Runs **`npx skills-ref validate`**.

## Layout

| Path | Role |
| ---- | ---- |
| `SKILL.md` | Agent-facing skill + YAML frontmatter |
| `references/OVERVIEW.md` | Index |
| `references/AUTH.md` | Env / keine Secrets im Chat |
| `references/01_seo_grundlagen.md` | SEO-Grundlagen |
| `references/02_crawling_indexierung.md` | Crawling & Indexierung |
| `references/04_monitoring_fehlerbehebung.md` | Monitoring & Fehlerbehebung |
| `references/03_ranking_darstellung.md` | Hub + links to `03.1`–`03.7` |
| `references/03.*_ranking_darstellung_*.md` | Ranking/Darstellung parts |
| `references/05_webspezifische_leitfaeden.md` | Hub + links to `05.1`–`05.8` |
| `references/05.*_webspezifische_leitfaeden_*.md` | Webspezifische Leitfäden parts |
| `.env.example` | Commented placeholders (stripped by package script for ClawHub) |

## Local symlink (optional)

```bash
./scripts/sync-openclaw-seo.sh
```

## Maintainer docs

- **[docs/openclaw-seo/README.md](../docs/openclaw-seo/README.md)** — regenerate notes, ClawHub checklist (when expanded).

Compatible with [AgentSkills](https://agentskills.io/specification) layout and [OpenClaw Skills](https://docs.openclaw.ai/tools/skills).
