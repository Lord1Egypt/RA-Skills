# Contributing to QELT Indexer Skill

This skill wraps the QELT Mainnet Indexer REST API. Determine where the problem lies before reporting issues.

## Issue Reporting Guide

### Open an issue in this repository if

- The skill documentation is unclear or missing
- Examples in SKILL.md do not work as described
- The API response shape has changed
- The skill is missing an endpoint or use-case

### Open an issue at the QELT team if

- The indexer API is down or returning unexpected errors
- Data returned is inconsistent with on-chain state
- The indexer has persistent lag issues

## Before Opening an Issue

1. Test the API is reachable and synced:
   ```bash
   curl -fsSL "https://mnindexer.qelt.ai/v1/health/ready"
   ```

2. Check the `lag` field — if `lag > 100`, data may be stale and this is an indexer issue, not a skill issue.

## Issue Report Template

```markdown
### Description
[Provide a clear and concise description of the problem]

### Reproduction Steps
1. [First Step]
2. [Second Step]
3. [Observe error]

### Expected Behavior
[Describe what you expected to happen]

### Environment Details
- **Skill Version:** [from _meta.json]
- **Network:** [mainnet / testnet]
- **Endpoint:** [e.g. /v1/transactions/{hash}]
- **curl Version:** [output of curl --version]
- **Operating System:** [e.g. macOS, Ubuntu 22.04]

### Additional Context
- [Full API response or error output]
- [Block number or transaction hash if relevant]
- [Indexer lag value from /v1/health/ready]
```

## Adding New Endpoints

Update SKILL.md when new indexer endpoints are added.
- Keep the response shape examples accurate
- Add new endpoints in the correct category with working curl examples
- Update the rate limits table if new tiers are introduced
