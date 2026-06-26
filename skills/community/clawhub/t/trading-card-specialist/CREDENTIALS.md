# Optional Credentials & Integration Setup

This skill works in a **no-credential mode** for card analysis, listing generation, and grading guidance.

Only configure external credentials if you need live integration data.

## Optional credentials

### eBay API
```bash
export EBAY_APP_ID="your_production_app_id"
export EBAY_CERT_ID="your_production_cert_id"
export EBAY_DEV_ID="your_production_dev_id"
export EBAY_USER_TOKEN="your_production_user_token"
```

Use for:
- sold listing research
- active listing comparison
- listing optimization based on live marketplace data

Registration: https://developer.ebay.com/

### PSA API
```bash
export PSA_API_KEY="your_psa_api_key"
```

Use for:
- population data
- certification verification workflows

## Recommended setup approach

Prefer environment variables provided by your shell, runtime, or secret manager.

Examples:
```bash
export EBAY_APP_ID="..."
export EBAY_CERT_ID="..."
export EBAY_DEV_ID="..."
export EBAY_USER_TOKEN="..."
export PSA_API_KEY="..."
```

Do **not** store credentials inside this skill package.
Do **not** use home-directory secret files as part of this skill's setup instructions.

## Functionality by setup level

### Level 1 — No credentials
Available:
- card description and identification help
- listing title and description generation
- pricing heuristics from user-supplied details
- grading decision support

### Level 2 — eBay enabled
Available:
- live comp research
- active listing positioning
- stronger pricing recommendations

### Level 3 — eBay + PSA enabled
Available:
- population-aware analysis
- cert / grading context enrichment

## Validation

Validate configured environment variables using your normal shell/runtime secret checks before enabling live integrations.

## Notes

- Treat all integrations as optional.
- Keep permissions minimal.
- Use read-only access patterns where possible.
- Review [references/SECURITY.md](references/SECURITY.md) when deploying this skill in a shared or production environment.
