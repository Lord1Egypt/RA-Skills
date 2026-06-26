# Shopify AI Toolkit Skill for OpenClaw

Open-source Shopify AI Toolkit skill for OpenClaw agents. Search Shopify docs and validate GraphQL, Liquid, Hydrogen, and more — directly from your agent.

## Skills

| Skill | Description |
|-------|-------------|
| `shopify-admin` | Admin GraphQL API — products, orders, customers, inventory |
| `shopify-storefront-graphql` | Storefront GraphQL API — carts, checkout, customer accounts |
| `shopify-liquid` | Liquid templating language — themes, sections, snippets, blocks |
| `shopify-hydrogen` | Shopify Hydrogen framework — React-based storefronts |
| `shopify-functions` | Shopify Functions — cart validation, discounts, fulfillment |
| `shopify-custom-data` | Custom data — metafields, storefront properties |
| `shopify-customer` | Customer accounts API |
| `shopify-polaris-extensions` | Polaris React components for admin extensions |

## Quick Start

### Prerequisites

- Node.js 18+ installed
- Environment variables (optional):

```bash
# Optional: opt out of Shopify telemetry
export OPT_OUT_INSTRUMENTATION=true

# Optional: use a custom Shopify dev base URL
export SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```

### Usage

The skill prompts the agent to follow a strict **search → code → validate** workflow:

1. **Search docs** before writing code:
   ```bash
   node scripts/search_docs.mjs "<query>" --model <model> --client-name openclaw --client-version 1.0
   ```

2. **Write code** using the search results

3. **Validate** before returning (GraphQL skills):
   ```bash
   node scripts/validate.mjs \
     --code '<graphql query/mutation>' \
     --model <model> \
     --client-name openclaw \
     --client-version 1.0 \
     --artifact-id <random-id> \
     --revision 1
   ```

4. **Validate** Liquid (theme) code:
   ```bash
   node scripts/liquid_validate.mjs \
     --filename <file.liquid> \
     --filetype <sections|snippets|blocks|templates|layout> \
     --code '<liquid content>' \
     --model <model> \
     --client-name openclaw \
     --client-version 1.0 \
     --artifact-id <random-id> \
     --revision 1
   ```

## Install via OpenClaw CLI

Any OpenClaw agent can install this skill with one command:

```bash
# Navigate to your skills directory
cd ~/.openclaw/agents/YOUR_AGENT/workspace/skills

# Install the skill
clawhub install shopify-ai-toolkit
```

This installs the skill to `skills/shopify-ai-toolkit/` in the agent's workspace.

**After installing, restart the gateway for the skill to load:**

```bash
openclaw gateway restart
```

That's it. The agent can now use Shopify skills — no manual setup required.

---


## Available Skills

### shopify-admin

Build Admin GraphQL API integrations — products, orders, customers, inventory, fulfillment, and more.

### shopify-storefront-graphql

Write Storefront GraphQL API queries for custom storefronts — carts, checkout, product search, customer accounts.

### shopify-liquid

Create Liquid theme components — sections, snippets, blocks, templates, and theme schemas.

### shopify-hydrogen

Build Shopify Hydrogen apps with React and Oxygen — components, hooks, routes, and server functions.

### shopify-functions

Write Shopify Functions for cart validation, discounts, delivery customization, and fulfillment constraints.

### shopify-custom-data

Work with metafields, attributes, and custom data on products, orders, and customers.

### shopify-customer

Integrate with the Customer Accounts API — authentication, profiles, and addresses.

### shopify-polaris-extensions

Build Polaris React admin extensions — app home cards, checkout UI, customer account sections.

## MCP Server Integration

You can also connect the **Shopify Dev MCP server** directly to Codex CLI:

```bash
# Add the Shopify Dev MCP server to Codex
codex mcp add shopify-dev -- npx -y @shopify/shopify.ai dev-server

# List MCP servers
codex mcp list

# Remove if needed
codex mcp remove shopify-dev
```

## License

MIT — see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
