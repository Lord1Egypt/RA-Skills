# Contributing to QELT Blockchain Skill

This skill wraps the QELT JSON-RPC API. Determine where the problem lies before reporting issues.

## Issue Reporting Guide

### Open an issue in this repository if

- The skill documentation is unclear or missing
- Examples in SKILL.md do not work as described
- You need help using the JSON-RPC API with this skill
- The skill is missing a method or use-case example

### Open an issue at the QELT documentation repository if

- The JSON-RPC endpoint is down or returning unexpected errors
- A method behaves differently from the Ethereum specification
- You need a new RPC method supported

## Before Opening an Issue

1. Test the JSON-RPC call directly in your terminal to isolate the issue:
   ```bash
   curl -fsSL -X POST https://mainnet.qelt.ai \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
   ```

2. Check the [QELT Network Reference](references/network.md) for current endpoint URLs.

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
- **curl Version:** [output of curl --version]
- **Operating System:** [e.g. macOS, Ubuntu 22.04]

### Additional Context
- [Full RPC response or error output]
- [Transaction hash if applicable]
```

## Adding New Examples to the Skill

Update SKILL.md when new use-cases arise.
- Keep the Safety section accurate
- Add new JSON-RPC methods in the correct category
- Include working curl examples with realistic placeholders
