# Contributing to QELT Contracts Skill

This skill wraps the QELT Mainnet Indexer contract verification API. Determine where the problem lies before reporting issues.

## Issue Reporting Guide

### Open an issue in this repository if

- The skill documentation is unclear or missing
- Examples in SKILL.md do not work as described
- The EVM version mapping table needs updating
- The skill is missing a verification workflow

### Open an issue at the QELT team if

- The verification API is down or returning unexpected errors
- A supported compiler version is missing from the list
- Verification results are consistently incorrect

## Before Opening an Issue

1. Test the API is reachable:
   ```bash
   curl -fsSL "https://mnindexer.qelt.ai/api/v2/verification/compiler-versions" | head -c 200
   ```

2. Check the [verification guide](references/verification-guide.md) for the EVM version table and ensure your `compilerVersion` + `evmVersion` pair matches.

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
- **Solidity Version:** [e.g. 0.8.20]
- **EVM Version:** [e.g. shanghai]
- **curl Version:** [output of curl --version]
- **Operating System:** [e.g. macOS, Ubuntu 22.04]

### Additional Context
- [Job ID if verification was submitted]
- [Full API response or error output]
- [Whether viaIR was used]
```

## Updating the EVM Version Table

If QELT adds support for a new EVM version, update the table in both `SKILL.md` and `references/verification-guide.md` in the same PR.
