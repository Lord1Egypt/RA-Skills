# Optional Integration Notes

This skill is designed to work without external integrations.

Use this reference only when a task specifically needs live external data and the host environment already provides the necessary integration code or approved workflow.

## eBay

Optional environment variables:
- `EBAY_APP_ID`
- `EBAY_CERT_ID`
- `EBAY_DEV_ID`
- `EBAY_USER_TOKEN`

Use eBay integration for:
- sold listing comparisons
- active listing research
- pricing context for a specific card
- title keyword refinement based on live marketplace language

Keep usage conservative:
- prefer read-only research flows
- respect API limits and marketplace terms
- do not imply automated posting or bidding unless separately implemented and approved

## PSA

Optional environment variable:
- `PSA_API_KEY`

Use PSA integration for:
- population lookup workflows
- cert verification workflows
- scarcity context in listing copy

## Guidance

- Treat all integrations as optional enrichments.
- If credentials are absent, fall back to no-credential analysis.
- State clearly when an answer is heuristic vs based on live external data.
