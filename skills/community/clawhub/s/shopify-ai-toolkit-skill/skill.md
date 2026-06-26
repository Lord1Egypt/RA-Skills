---
name: shopify-ai-toolkit
description: OpenClaw skill for the Shopify AI Toolkit — search Shopify docs and validate GraphQL, Liquid, Hydrogen, and more. Use for any Shopify app, theme, or storefront development task. Skills: shopify-admin, shopify-storefront-graphql, shopify-liquid, shopify-hydrogen, shopify-functions, shopify-custom-data, shopify-customer, shopify-polaris-extensions.
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - SHOPIFY_DEV_INSTRUMENTATION_URL
        - OPT_OUT_INSTRUMENTATION
---

# Shopify AI Toolkit for OpenClaw

Search Shopify developer documentation and validate code before returning it to the user.

## Available Sub-Skills

| Sub-skill | Use when the user asks about... |
|-----------|----------------------------------|
| `shopify-admin` | Admin API, GraphQL mutations/queries for store management |
| `shopify-storefront-graphql` | Storefront API, cart/checkout/customer data fetching |
| `shopify-liquid` | Theme development, Liquid templates, sections, snippets |
| `shopify-hydrogen` | Hydrogen framework, React storefronts on Oxygen |
| `shopify-functions` | Cart validation, discounts, delivery customization |
| `shopify-custom-data` | Metafields, custom data on products/orders/customers |
| `shopify-customer` | Customer accounts API, authentication, profiles |
| `shopify-polaris-extensions` | Polaris React UI components for admin apps |

## How This Skill Works

Each sub-skill enforces a **search → validate → return** workflow using Node.js scripts from the `scripts/` directory.

**You must load the relevant sub-skill's SKILL.md for your task.** The sub-skill instructions override this master skill when loaded.

## Setup

```bash
# Optional: opt out of Shopify telemetry
export OPT_OUT_INSTRUMENTATION=true

# Optional: custom Shopify dev URL
export SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```

## Choosing the Right Skill

| User wants to... | Use this skill |
|-----------------|----------------|
| Manage products, orders, customers via API | `shopify-admin` |
| Build a custom storefront with GraphQL | `shopify-storefront-graphql` |
| Create or modify Shopify themes | `shopify-liquid` |
| Build a Hydrogen/React storefront | `shopify-hydrogen` |
| Write cart validators, discounts, or fulfillment functions | `shopify-functions` |
| Work with metafields or custom data | `shopify-custom-data` |
| Integrate customer accounts | `shopify-customer` |
| Build admin UI with Polaris components | `shopify-polaris-extensions` |

## MCP Server Alternative

Instead of the scripts, you can connect the **Shopify Dev MCP server** to Codex CLI:

```bash
codex mcp add shopify-dev -- npx -y @shopify/shopify.ai dev-server
```

This gives Codex direct access to Shopify tools via MCP. The scripts approach (above) works without any MCP connection.
