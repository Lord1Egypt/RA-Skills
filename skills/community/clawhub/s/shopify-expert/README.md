# Shopify Expert (OpenClaw skill)

**Bundle version:** 1.1.0

**Skill id / folder / ClawHub slug:** `shopify-expert`  
**ClawHub listing title:** use **`clawhub publish --name "Shopify Expert"`** (see [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)). Maintainer flow: **`docs/openclaw-shopify/CLAWHUB_PUBLISH.md`**.

This bundle includes **`SKILL.md`**, hand-written OpenClaw guides under **`references/`**, **generated** excerpts from Shopify’s LLM documentation snapshot as **`references/DOC_*.md`**, and the hand-curated **Admin REST** reference **`references/ADMIN_REST_API.md`** (not produced by the LLM generator). For **merchant** help, see **`references/MERCHANT_USER_DOCS.md`**.

## Package for ClawHub

```bash
./scripts/package-shopify-expert-for-clawhub.sh
```

Output: **`build/clawhub-publish/shopify-expert`**. Runs **`skills-ref validate`**.

## Regenerating references (maintainers)

```bash
./scripts/regenerate-shopify-skill-references.sh
```

Input default: **`agents/mohami/memories/systems/Shopify/SHOPIFY_OFFICIAL_LLM_DOCS.txt`**. Taxonomy: **`docs/openclaw-shopify/taxonomy.yaml`**.

## Layout

| Path | Role |
| ---- | ---- |
| `SKILL.md` | Agent-facing skill + YAML frontmatter |
| `references/OVERVIEW.md` | Index |
| `references/DOC_*.md` | Generated from Shopify LLM txt |
| `references/ADMIN_REST_API.md` | Admin REST API (curated; maintenance = manual) |
| `references/*.md` | Hand-authored guides |
| `.env.example` | Commented placeholders (stripped by package script for ClawHub) |
