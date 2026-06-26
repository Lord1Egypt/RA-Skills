# Official sources and Shopify versions

Use this skill together with **live** Shopify documentation. Bundled `references/DOC_*.md` are **excerpts** from a **point-in-time export** of Shopify’s **official LLM-oriented developer documentation** text; they are **not** a substitute for current **[shopify.dev](https://shopify.dev/)**.

## What is in the bundle

- **Generated:** `DOC_*.md` — split and merged per [`docs/openclaw-shopify/taxonomy.yaml`](../../docs/openclaw-shopify/taxonomy.yaml) from `SHOPIFY_OFFICIAL_LLM_DOCS.txt`.
- **Regeneration:** `./scripts/regenerate-shopify-skill-references.sh` (from monorepo root). Coverage manifest: `docs/openclaw-shopify/_generated/coverage_manifest.json`.

## Primary URLs

| Audience | Site |
| -------- | ---- |
| Developers | [shopify.dev](https://shopify.dev/) |
| Merchants | [help.shopify.com](https://help.shopify.com/) |

## Attribution

Text originates from **Shopify** documentation materials provided for LLM / developer use. Prefer linking to **shopify.dev** for canonical, versioned API references.

## API versions

Examples in the snapshot may cite specific Admin API versions (e.g. `2025-01`). **Confirm** the version your app and shop support before relying on payloads in the bundle.
