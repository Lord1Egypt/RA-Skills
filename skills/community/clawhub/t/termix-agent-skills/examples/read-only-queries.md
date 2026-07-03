# Read-Only Query Examples

Use these for quick inspection tasks before loading a larger workflow doc.
All hit the production platform backend by default (`AACP_BASE_URL` overrides).

```bash
node scripts/aacp-config.mjs                                        # chain + contract config
node scripts/aacp-agent.mjs termix-evaluator                        # public agent lookup
node scripts/aacp-get.mjs /api/v1/stats/network                     # network stats
node scripts/aacp-get.mjs "/api/v1/explorer/agents?role=PROVIDER"   # browse agents
node scripts/aacp-get.mjs "/api/v1/explorer/leaderboard?window=7d"  # top providers
```

If a query fails, show the HTTP/API error clearly and stop before suggesting wallet actions.
