---
name: x402-discovery
version: 1.0.0
description: "Discover x402-enabled services across multiple catalogs — Bazaar, Agentic Market, x402-list.com, .well-known/x402 manifests. Find the best service for a task by scanning machine-readable discovery surfaces."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["curl"]
    homepage: "https://www.x402.org"
---

# x402 Discovery

Find x402-enabled services across the ecosystem. Scan Bazaar, Agentic Market, x402-list.com, and individual service manifests to discover available endpoints, prices, and schemas.

## What Is x402 Discovery?

x402 services publish machine-readable manifests so agents can discover them without a central registry. This skill shows you how to find them.

## Discovery Sources

### 1. x402 Bazaar (Official Index)

The x402 Foundation's discovery layer. Facilitators publish `/discovery/resources` endpoints:

```bash
curl -s https://api.cdp.coinbase.com/x402/discovery/resources
```

Returns all x402-compatible services registered through the facilitator, with full pricing, schemas, and metadata.

### 2. Agentic Market (Frontend)

The Coinbase-operated marketplace frontend. Services indexed on the Bazaar appear here:

```bash
# Search via the Bazaar API
curl -s "https://api.cdp.coinbase.com/x402/discovery/resources?type=http"
```

### 3. x402-list.com (Curated Directory)

Community-curated listing of x402 services:

```bash
curl -s https://x402-list.com/api/services
```

### 4. .well-known/x402 (Service Manifests)

Individual services publish their own discovery manifest. Check any service origin:

```bash
curl -s https://service.example/.well-known/x402
curl -s https://service.example/.well-known/x402.json  # same payload
```

The manifest includes: x402Version, serviceName, claim, description, facilitator, catalog URL, demo URL, and a `resources` array with every endpoint's URL, price, payTo, asset, network, and inputSchema.

### 5. llms.txt (Agent Discovery Index)

Many x402 services publish an llms.txt at their origin root:

```bash
curl -s https://service.example/llms.txt
```

### 6. Promo/Catalog JSON

Services often expose a full catalog:

```bash
curl -s https://service.example/promo/catalog.json
```

## Discovery by Task

To find a service for a specific task, combine the sources:

```bash
# 1. Check the Bazaar
# 2. Check x402-list.com  
# 3. Check known .well-known manifests
# 4. Search for task-specific keywords in service descriptions
```

The `.well-known/x402` manifest includes `inputSchema` for each resource — so you can match by input type.

## Example: Find Cheap Compliance Services

```bash
# Check the Herman Commerce DACH manifest
curl -s https://agent.kihustle.tech/.well-known/x402
```

## Pro Tips

- Check `amount` in atomic units (6 decimals USDC) — `"50000"` = $0.05
- Look at `extensions.bazaar.info` in 402 responses for full Bazaar metadata
- Cross-reference prices: the same endpoint may differ between catalogs
- Prefer services with `discoverable: true` in their Bazaar extension