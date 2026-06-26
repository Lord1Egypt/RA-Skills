# Shopware Expert (OpenClaw skill)

**Bundle version:** 1.0.5

**Skill id / folder / ClawHub slug:** `shopware-expert`  
**ClawHub listing title:** use **`clawhub publish --name "Shopware Expert"`** (see [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)). Maintainer checklist, pre-flight, and CLI example: **`docs/openclaw-shopware/CLAWHUB_PUBLISH.md`** in this monorepo.

This bundle includes **`SKILL.md`**, hand-written OpenClaw guides under **`references/`**, and **generated** excerpts from the Shopware Developer Documentation (plus an **ADR index**). For **merchant Admin usage**, see **`references/MERCHANT_USER_DOCS.md`** (links to **docs.shopware.com**).

## Local development (monorepo)

- Skill source: **`openclaw-shopware-skill/`** in this repository.
- Symlink into OpenClaw workspace:

  ```bash
  ./scripts/sync-openclaw-shopware.sh
  ```

- Package for ClawHub (text-only folder; drops `.gitignore` and `.env.example` per script):

  ```bash
  ./scripts/package-shopware-expert-for-clawhub.sh
  ```

  Output: **`build/clawhub-publish/shopware-expert`**. Validation runs **`skills-ref validate`** on that folder.

## Regenerating references (maintainers)

From the monorepo root (requires the Shopware LLM dump path configured in the scripts):

```bash
./scripts/regenerate-shopware-skill-references.sh
```

Details: **`docs/openclaw-shopware/README.md`**.

## Configuration

- **`metadata.openclaw.requires`**: `SHOPWARE_BASE_URL` and **`curl`** (see **`SKILL.md`** and **`.env.example`**).
- Optional OAuth variables for the Admin API are documented in **`references/AUTH.md`** (not required for skill eligibility).

## Layout

| Path | Role |
| ---- | ---- |
| `SKILL.md` | Agent-facing skill + YAML frontmatter |
| `references/OVERVIEW.md` | Index of all reference files |
| `references/*.md` | OpenClaw + Shopware material (hand-written and generated) |
| `.env.example` | Commented env placeholders (not uploaded to ClawHub by package script) |
