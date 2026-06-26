# Contributing to QELT DEX Skill

This skill wraps the Uniswap v4 deployment on QELT Mainnet. Determine where the problem lies before reporting issues.

## Issue Reporting Guide

### Open an issue in this repository if

- The skill documentation is unclear or missing
- Examples in SKILL.md do not work as described
- Contract addresses in the skill are outdated
- The skill is missing a DEX operation or use-case

### Open an issue at the QELT team if

- A contract address has changed
- The DEX deployment has been upgraded
- An RPC call returns an unexpected error

## Before Opening an Issue

1. Verify the contract is still deployed at the documented address:
   ```bash
   curl -fsSL -X POST https://mainnet.qelt.ai \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_getCode","params":["0x11c23891d9f723c4f1c6560f892e4581d87b6d8a","latest"],"id":1}'
   ```
   Response should be non-empty (not `"0x"`).

2. Check the [contracts reference](references/contracts.md) for the latest addresses.

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
- **Contract:** [PoolManager / UniversalRouter / etc.]
- **curl Version:** [output of curl --version]
- **Operating System:** [e.g. macOS, Ubuntu 22.04]

### Additional Context
- [Full RPC response or revert reason]
- [Transaction hash if applicable]
```

## Updating Contract Addresses

If a contract address changes, update both `SKILL.md` and `references/contracts.md` in the same PR.
