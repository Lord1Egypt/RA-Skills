# AI Gateway — Installation & Setup

## Prerequisites

You need `curl` and `jq` available in your environment:

```bash
curl --version
jq --version
```

If missing:
- macOS: `brew install curl jq`
- Ubuntu/Debian: `apt install curl jq`

## Create the Site Registry

The skill uses a `sites.json` file to store credentials for each Statamic site you manage. Create it at the default location:

```bash
mkdir -p ~/.config/ai-gateway
```

```bash
cat > ~/.config/ai-gateway/sites.json << 'EOF'
{
  "sites": {
    "marketing": {
      "base_url": "https://marketing.example.com",
      "token": "your-marketing-site-token"
    }
  }
}
EOF
```

Protect the file since it contains secrets:

```bash
chmod 600 ~/.config/ai-gateway/sites.json
```

To use a different path, set the `AI_GATEWAY_SITES_CONFIG` environment variable:

```bash
export AI_GATEWAY_SITES_CONFIG="/path/to/your/sites.json"
```

## Site Registry Format

```json
{
  "sites": {
    "site-name": {
      "base_url": "https://your-site.com",
      "token": "the-AI_GATEWAY_TOKEN-for-this-site"
    }
  }
}
```

| Field      | Description                                    | Example                              |
|------------|------------------------------------------------|--------------------------------------|
| key        | Short name you'll use to reference this site   | `marketing`, `docs`, `portal`        |
| `base_url` | The site's URL, no trailing slash              | `https://marketing.example.com`      |
| `token`    | The `AI_GATEWAY_TOKEN` configured on that site | `a1b2c3d4e5f6...`                    |

The site operator provides both the base URL and token. Each Statamic site has its own unique token.

If you're also the site operator and need to generate a token:

```bash
openssl rand -hex 32
```

Set the output as `AI_GATEWAY_TOKEN` in the site's `.env` and as the `token` value in your `sites.json`.

## Adding Multiple Sites

Add as many sites as you need:

```json
{
  "sites": {
    "marketing": {
      "base_url": "https://marketing.example.com",
      "token": "token-aaa..."
    },
    "docs": {
      "base_url": "https://docs.example.com",
      "token": "token-bbb..."
    },
    "portal": {
      "base_url": "https://portal.example.com",
      "token": "token-ccc..."
    }
  }
}
```

Each site is fully independent — its own token, its own enabled tools, its own allowlists, its own rate limits. A `403 forbidden` on one site doesn't mean the same target is forbidden on another.

## First-Run Smoke Test

Pick a site and verify the connection:

```bash
# Read credentials for the "marketing" site
SITE_URL=$(jq -r '.sites.marketing.base_url' ~/.config/ai-gateway/sites.json)
SITE_TOKEN=$(jq -r '.sites.marketing.token' ~/.config/ai-gateway/sites.json)

# Check capabilities
curl -s -H "Authorization: Bearer $SITE_TOKEN" \
  $SITE_URL/ai-gateway/capabilities | jq .
```

### Expected: success

A JSON response with `ok: true` listing each tool's `enabled` state, `target_type`, and `requires_confirmation` flag. The exact tools vary per site.

### Troubleshooting

| Response           | Meaning                              | Fix                                                  |
|--------------------|--------------------------------------|------------------------------------------------------|
| `401 unauthorized` | Token is wrong or missing            | Check the `token` in `sites.json` matches the site's `.env` |
| `404` (HTML)       | Addon is not enabled on the site     | Site operator needs `AI_GATEWAY_ENABLED=true`        |
| Connection refused | Site is unreachable                  | Check `base_url` in `sites.json`                     |
| `429 rate_limited` | Too many requests                    | Wait a minute and retry                              |

### Test each site

Repeat the smoke test for every site in your registry. Each site may have different capabilities:

```bash
for site in $(jq -r '.sites | keys[]' ~/.config/ai-gateway/sites.json); do
  url=$(jq -r ".sites.$site.base_url" ~/.config/ai-gateway/sites.json)
  tok=$(jq -r ".sites.$site.token" ~/.config/ai-gateway/sites.json)
  echo "--- $site ($url) ---"
  curl -s -H "Authorization: Bearer $tok" $url/ai-gateway/capabilities | jq '.result.capabilities | to_entries[] | select(.value.enabled) | .key'
done
```

## Test a Write Operation

Once capabilities look good, test a simple upsert on one site:

```bash
SITE_URL=$(jq -r '.sites.marketing.base_url' ~/.config/ai-gateway/sites.json)
SITE_TOKEN=$(jq -r '.sites.marketing.token' ~/.config/ai-gateway/sites.json)

curl -s -X POST \
  -H "Authorization: Bearer $SITE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "entry.upsert",
    "arguments": {
      "collection": "pages",
      "slug": "setup-test",
      "data": { "title": "Setup Test" }
    },
    "request_id": "marketing:install-smoke-test"
  }' \
  $SITE_URL/ai-gateway/execute | jq .
```

Expected: `ok: true` with `status: "created"` or `status: "updated"`.

If you get `403 forbidden`, the collection isn't in that site's allowlist — ask the site operator to add it.

## Token Rotation

To rotate a token for a single site, update the `token` value in `sites.json` and update the corresponding `AI_GATEWAY_TOKEN` in that site's `.env`. Other sites are unaffected.

## You're Ready

Once the smoke tests pass, the skill is operational. Refer to [SKILL.md](./SKILL.md) for the quick reference and [references/api.md](./references/api.md) for full endpoint documentation.
