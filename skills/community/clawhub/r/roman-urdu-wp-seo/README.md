# Roman Urdu WordPress SEO Optimizer

**Roman Urdu WordPress SEO Optimizer** is an OpenClaw/ClawHub skill for WordPress SEO workflows targeting readers who search in English, Roman Urdu, or Hinglish. It keeps the English keyword core visible while adding natural South Asian phrasing to keyword research, metadata, alt-text suggestions, and technical SEO reviews.

The skill reflects the practical context of **Byte Wave, Lahore, Pakistan**. It is an editorial aid: it does not fetch keyword volume, guarantee rankings, call external APIs, or publish changes to a WordPress site.

## What it includes

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent-facing workflow, activation rules, safeguards, resource routing, and tests. |
| `references/roman-urdu-keyword-patterns.md` | 25 reusable English-to-Roman Urdu/Hinglish search patterns and spelling guidance. |
| `references/wordpress-seo-checklist.md` | WordPress metadata, permalink, schema, sitemap, plugin, performance, and accessibility checks. |
| `references/code-mixing-guide.md` | Editorial rules for natural English and Roman Urdu code-mixing. |
| `scripts/keyword_expander.py` | Offline keyword variant generator using the Python standard library. |
| `scripts/meta_tag_generator.py` | Offline blended SEO title, meta description, and slug draft generator. |
| `examples/sample-optimized-post.md` | End-to-end functional example for a budget-smartphone post. |

## Installation

### ClawHub / OpenClaw

Publish or install the complete `roman-urdu-wp-seo/` directory as a skill package through your normal ClawHub workflow. The required entry point is `SKILL.md`; keep the `references/`, `scripts/`, and `examples/` paths beside it so the agent can route to the bundled resources.

### Local inspection

No third-party Python packages are required. From this directory, run:

```bash
python scripts/keyword_expander.py "best mobile under 30000" --location Pakistan
python scripts/meta_tag_generator.py \
  --keyword "best mobile under 30000" \
  --topic "budget smartphones" \
  --audience "Pakistan ke buyers" \
  --benefit "30 hazar ke andar sahi phone choose karein"
```

Pass `--json` to either script for machine-readable output. Both scripts are offline and do not require credentials, environment variables, network access, WordPress authentication, or API keys.

## Example workflow

A typical request is:

> “Meri WordPress post `best mobile under 30000` ko Pakistan audience ke liye Roman Urdu SEO mein optimize karo.”

The agent should identify the audience and intent, suggest two to three mixed-language variants, draft blended metadata, recommend a short slug, audit the active Yoast SEO or Rank Math setup, review headings and alt-text, check schema and sitemap behavior, and return a pre-publish checklist. It should not translate the complete English post unless the user explicitly asks for a full translation.

See `examples/sample-optimized-post.md` for the complete test input and approved output.

## Editorial limitations

Roman Urdu spelling varies by speaker and region. Generated variants are suggestions rather than search-volume evidence. A native or experienced editor should review phrasing, especially for health, financial, legal, safety, and culturally sensitive content. Local modifiers such as Pakistan, Lahore, currency, and dates should appear only when the page genuinely supports them.

## Security and publishing policy

The package contains no credentials or hardcoded local paths. The scripts do not scrape search engines, call an external service, or mutate a WordPress site. Any actual WordPress update or publication requires explicit user authorization and the appropriate authenticated workflow.

ClawHub skills are distributed under the platform's automatic MIT-0 terms. This package intentionally contains no separate license terms, pricing, paywall metadata, or attribution requirement.

## Final folder tree

```text
roman-urdu-wp-seo/
├── SKILL.md
├── README.md
├── references/
│   ├── roman-urdu-keyword-patterns.md
│   ├── wordpress-seo-checklist.md
│   └── code-mixing-guide.md
├── scripts/
│   ├── keyword_expander.py
│   └── meta_tag_generator.py
└── examples/
    └── sample-optimized-post.md
```
