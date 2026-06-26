---
name: trading-card-specialist2
description: Trading card analysis, grading guidance, market comps, and eBay listing optimization for sports cards, Pokémon, and other collectible cards. Use when evaluating a card, estimating value, deciding whether grading is worth it, generating or improving eBay titles/descriptions, comparing recent comps, or planning a card-selling workflow. Supports a safe no-credential mode for copywriting and strategy; optionally enrich with eBay and PSA data when credentials are available.
---

# Trading Card Specialist v2.0.4

Provide trading card analysis and listing support with a conservative trust posture.

## Core workflow

1. Identify the card: year, brand, set, player/character, card number, variation, grading status, and visible condition.
2. Decide the operating mode:
   - **No-credential mode**: use user-provided details, attached images, and general heuristics.
   - **eBay mode**: use configured eBay credentials for market comps and listing research.
   - **PSA mode**: use configured PSA credentials for population or cert lookup.
3. Produce the smallest useful output:
   - value range
   - grading recommendation
   - optimized eBay title
   - concise sales description
   - notes on what still needs verification
4. Do not claim live market or population data unless those integrations are actually configured and queried.

## Operating modes

### 1) No-credential mode
Use this by default when credentials are unavailable.

Available tasks:
- card identification help
- listing title/description generation
- pricing heuristics based on user-supplied comps
- grading decision framework
- photo and presentation recommendations

### 2) Optional eBay enrichment
Use only when eBay credentials are configured **and the host environment provides a real eBay integration workflow**.

Supported use cases:
- sold listing comparisons
- active listing positioning
- title keyword refinement
- category and listing structure guidance

### 3) Optional PSA enrichment
Use only when `PSA_API_KEY` is configured **and the host environment provides a real PSA integration workflow**.

Supported use cases:
- certification verification workflows
- population-aware grading context
- scarcity framing for listings

## Credentials

Treat integrations as optional unless the task specifically requires live external data.

### Optional environment variables
- `EBAY_APP_ID`
- `EBAY_CERT_ID`
- `EBAY_DEV_ID`
- `EBAY_USER_TOKEN`
- `PSA_API_KEY`

Do not ask users to create home-directory credential files. Prefer runtime environment variables or the host's secret management.

Read [CREDENTIALS.md](CREDENTIALS.md) only when the user needs integration setup. This package does not include bundled live eBay or PSA client implementations.

## Output guidelines

### Card analysis
Return:
- card summary
- condition estimate with confidence qualifier
- estimated value range
- notable risks or missing information
- grading recommendation

### eBay listing output
Use the bundled template in [assets/ebay-listing-template.md](assets/ebay-listing-template.md) when generating listing copy.

Prefer:
- concise SEO title
- factual description
- no unverifiable hype
- clear disclosure of flaws, centering, edges, corners, and surface issues when known

### Grading guidance
Consider:
- raw vs graded spread
- likely grade band, not false precision
- grading fees, shipping, insurance, and turnaround time
- whether the card benefits from slab trust or liquidity

Read [references/GRADING-STRATEGY.md](references/GRADING-STRATEGY.md) when grading ROI is central.

## References

Load only as needed:
- [references/LISTING-OPTIMIZATION.md](references/LISTING-OPTIMIZATION.md) — title, description, and listing structure
- [references/MARKET-RESEARCH.md](references/MARKET-RESEARCH.md) — comp gathering and pricing workflow
- [references/GRADING-STRATEGY.md](references/GRADING-STRATEGY.md) — grading ROI and service selection
- [references/INTEGRATIONS.md](references/INTEGRATIONS.md) — optional eBay / PSA integration details
- [references/SECURITY.md](references/SECURITY.md) — credential handling and compliance notes

## Safety and trust rules

- Never imply credentials are required for basic use.
- Never store secrets inside the skill package.
- Never instruct users to put secrets in dotfiles under their home directory.
- Never claim automated posting, bidding, or other marketplace actions unless explicitly implemented and approved.
- Prefer official APIs over scraping.
- Keep outputs factual; avoid invented sales, ROI, or profit claims.
