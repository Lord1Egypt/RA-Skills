# Runtime Contract

This skill exposes the repo's current runtime through one script:

- `scripts/seller-runtime.mjs`

The skill is designed to be portable as a whole folder. Keep the `lib/`, `references/`, and `scripts/` subdirectories together when you copy it into another workspace.

## Runtime Input

The runtime reads connection details from environment variables:

- `SHOPIFY_STORE_DOMAIN`
- `SHOPIFY_CLIENT_ID`
- `SHOPIFY_CLIENT_SECRET`
- optional `SHOPIFY_API_VERSION`

For OpenClaw-native setup, prefer:

- `skills.entries."shopify-runtime".apiKey`
- `skills.entries."shopify-runtime".env.SHOPIFY_STORE_DOMAIN`
- `skills.entries."shopify-runtime".env.SHOPIFY_CLIENT_ID`
- `skills.entries."shopify-runtime".env.SHOPIFY_API_VERSION`

The skill declares `primaryEnv: "SHOPIFY_CLIENT_SECRET"`, so OpenClaw maps the configured `apiKey` into that environment variable for each agent run.

## Status Output

`seller-runtime.mjs status` returns:

- `provider`
- `status`: `ready` or `missing_config`
- `connection`
- `configured`
- `text`

Important fields:

- `connection.storeDomain`
- `connection.clientId`
- `connection.apiVersion`
- `configured.storeDomain`
- `configured.clientId`
- `configured.apiKey`
- `configured.apiVersion`

## Documentation Search Output

`seller-runtime.mjs search` returns:

- `provider`
- `query`
- `limit`
- `refresh`
- `results`

Each result includes:

- `title`
- `url`
- `heading`
- `excerpt`
- `sourceKind`: `provider_note` or `official_doc`
- `lastFetchedAt`
- `score`

Notes are ranked ahead of official docs. Official docs are fetched live and cached in-process for one hour.

## Execution Output

`seller-runtime.mjs execute` returns:

- `provider`
- `connection`
- `runtime`
- `mode`
- `script`
- `result`
- `logs`
- `warnings`
- `requestSummary`
- `rawResponses`
- `error`

Use `requestSummary` and `rawResponses` to explain what happened. Avoid copying large payloads into your final answer when a concise summary will do.

## Command Examples

```bash
node skills/shopify-runtime/scripts/seller-runtime.mjs status
```

```bash
node skills/shopify-runtime/scripts/seller-runtime.mjs search --query "inventory item sku"
```

```bash
cat <<'EOF' | node skills/shopify-runtime/scripts/seller-runtime.mjs execute --mode read
return await provider.graphql(`
  query {
    shop {
      name
    }
  }
`)
EOF
```

`execute` accepts the script from `stdin`, `--script`, or `--script-file`. Prefer `stdin` for multi-line snippets so the caller does not need to create temporary files.
