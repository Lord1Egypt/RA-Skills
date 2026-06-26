---
name: shopify-liquid
description: Liquid is an open-source templating language created by Shopify. It is the backbone of Shopify themes and is used to load dynamic content on storefronts. Keywords: liquid, theme, shopify-theme, liquid-component, liquid-block, liquid-section, liquid-snippet, liquid-schemas, shopify-theme-schemas. NOT for Admin or Storefront GraphQL (use shopify-admin or shopify-storefront-graphql).
license: MIT
---

# Shopify Liquid Skill

Search Liquid documentation and validate Liquid/Theme code before returning it.

## Required Workflow

### Step 1 — Search the docs (mandatory, max 2 searches)
```bash
node skills/shopify-liquid/scripts/liquid_search_docs.mjs "<tag, filter, or object name>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

If both searches return `[]`, skip to Step 2 using built-in Liquid knowledge.

### Step 2 — Write the Liquid code
Use search results or built-in knowledge. Follow theme architecture (sections, snippets, blocks, templates, layout).

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-liquid/scripts/liquid_validate.mjs \
  --filename <file.liquid> \
  --filetype <sections|snippets|blocks|templates|layout> \
  --code '<liquid content>' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "$(openssl rand -hex 8)" \
  --revision 1
```

### Step 4 — If validation fails
1. Read the error
2. Search for correct values
3. Fix the error
4. Re-validate (max 3 retries)

### Step 5 — Return code only after validation passes

## Theme Architecture

```
.
├── assets          # Static assets (CSS, JS, images, fonts)
├── blocks          # Reusable, nestable, customizable components
├── config          # Global theme settings
├── layout          # Top-level page wrappers
├── locales         # Translation files
├── sections        # Modular full-width page components
├── snippets        # Reusable Liquid code or HTML fragments
└── templates       # Templates combining sections and blocks
```

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```

## Example

User asks: "Create a featured collection section"

**Search → Write → Validate → Return** (follow the required workflow above)
