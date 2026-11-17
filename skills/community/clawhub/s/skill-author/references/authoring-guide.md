# ClawHub Skill Authoring Conventions

Verified against the ClawHub CLI source and live registry (2026-09). Use this when authoring a skill from scratch or bringing an existing folder up to standard.

## Structure

```
<skill-folder>/            # folder name = default slug
├── SKILL.md               # REQUIRED. The procedure. Keep it short (<10k chars)
├── README.md              # Human-facing: capabilities, file table, quick start, install
├── LICENSE                # Declared license (e.g. BSD-3-Clause)
├── VERSION                # One line: the version, mirroring frontmatter
└── references/            # Details, templates, checklists — anything longer than a step
```

- `SKILL.md` must be present (case-insensitive match; `skills.md` also works).
- The upload includes **text files only** — allowed extensions: md, mdx, txt, json, json5, yaml, yml, toml, js, cjs, mjs, ts, tsx, jsx, py, sh, rb, go, rs, swift, kt, java, cs, cpp, c, h, hpp, sql, csv, ini, cfg, env, xml, html, css, scss, sass, svg. PNG/JPG/PDF etc. are silently dropped — use SVG or describe visuals in text.
- Never ship `__pycache__/`, `test_output/`, `.DS_Store`, or other build/test artifacts.
- Never add a `skill-card.md` — the registry generates one automatically at publish time.

## Frontmatter field reference

| Field | Required | Purpose / notes |
|---|---|---|
| `name` | yes | Skill key. Keep it matching the slug; lowercase-kebab |
| `description` | yes | The only field matching engines really use. Trigger situations first ("Use when …"), one trigger per distinct branch, then what it produces. The first ~60 characters should already carry the main triggers |
| `description_zh` / `description_en` | recommended | Bilingual display on the registry; doubles discoverability for each language |
| `version` | recommended | semver string; must equal the `--version` you publish with |
| `license` | optional | Declared license (e.g. `BSD-3-Clause`). The registry listing always shows the platform's default `MIT-0` regardless — the in-package `LICENSE` file is what installers actually get |
| `homepage` | optional | Stable URL, e.g. the clawhub.ai skill page |
| `compatibility` | optional | One-line runtime requirements prose |
| `allowed-tools` | optional | Comma list of tools the skill needs (Read, Write, Edit, Exec, …) |
| `metadata.openclaw.emoji` | optional | One-emoji UI badge |
| `metadata.openclaw.requires.anyBins` | optional | Array of required executables, e.g. `["python3"]` |
| `metadata.openclaw.config.path` | optional | Config file shipped with the skill (e.g. `config.json`) |

## Naming (slug & display name)

- Default `slug` = `sanitizeSlug(basename(folder))`; default display name = `titleCase(basename(folder))`. Override with `--slug` / `--name` at publish if the folder name is ugly.
- Slugs are stable forever — pick once, keep it. Check availability first:
  ```bash
  clawhub search "<keywords>"        # look for collisions / near-duplicates
  clawhub inspect <slug>             # not found => free
  ```

## Versioning & tags

- Publish always needs a valid semver: `--version X.Y.Z`. It must be newer than the published latest.
- The changelog is shown on the registry — write it for two audiences: the reviewer and the installer. Itemize what changed, including security fixes.
- Default tag: `latest`. Extra tags (`--tags creative-writing,novel`) are cosmetic categories.
- Forks: `--fork-of <slug[@version>]` records provenance.

## Description writing (the highest-leverage field)

Good:
```
description: 'Render Mermaid diagrams as SVG/PNG/ASCII — use when asked for flowcharts,
sequence diagrams, or any Mermaid diagram. 6 chart types, 16 themes, interactive preview.'
```
- Trigger phrases first, then output.
- One description per *class of work*; don't cram five skills into one string.
- Negative scope when it prevents misfires: "Not for simple non-generation image tweaks."
- If behavior depends on a specific locale or user pattern, say so explicitly instead of implying it.

## SKILL.md body conventions

- Structure: purpose (1-2 lines) → when to use → numbered workflow steps → references table.
- Steps end with a checkable completion criterion ("…then verify the file parses").
- Long material (templates, full checklists, case studies) goes to `references/*.md`; cite from the step that needs it so the reader knows *when* to open it.
- If the skill does anything with files/network/shell, include an explicit "Rules" or "Safety" section near the top — auditors look for it.
- Language: write docs in the audience's language, but if you restrict language anywhere (triggers, output format), say why and that alternatives are supported.

## Security by design (write it in, don't bolt it on)

- Config defaults must be loopback-only; any remote endpoint is opt-in via env var and disclosed at runtime.
- Shell examples in docs: quote every expansion; sanitize user-controlled names with an allowlist before interpolation.
- Third-party install instructions: pinned commits + lock files + venv/non-root notes; the skill itself never executes `git clone`.
- No secrets, private IPs, or personal data in any shipped file.
- State the data flow (what is sent, where it goes, what is written to disk) in the README.

## Minimal working frontmatter template

```yaml
---
name: my-skill
description: '<trigger situations> — what the skill produces. Use when …'
version: 1.0.0
license: BSD-3-Clause
description_zh: "<same, in Chinese, optional>"
homepage: https://clawhub.ai/sunshinejnjn/my-skill
metadata:
  openclaw:
    emoji: "🧩"
compatibility: <one-line runtime requirements>
allowed-tools: Read, Write, Edit, Exec
---
```
