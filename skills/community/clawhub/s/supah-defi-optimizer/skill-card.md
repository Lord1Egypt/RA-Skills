## Description:

DeFi yield optimization, impermanent loss tracking, and portfolio management for Base blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query SUPAH's Base DeFi API for wallet position scans, APY comparisons, impermanent loss calculations, and optimization or rebalance suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends wallet or position identifiers to SUPAH's remote DeFi API.

Mitigation: Use only wallet or position identifiers appropriate for sharing with that service and review outbound network access before installing.

Risk: Automatic x402 USDC payments on Base can incur charges, and the published per-action pricing is inconsistent across the evidence.

Mitigation: Run in an environment where spending can be confirmed or capped, and verify current prices before use.

Risk: The authoritative security verdict is suspicious because the paid API calls have weak runtime controls.

Mitigation: Review the skill and execution environment before installing, especially API access and payment configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supah-based/skills/supah-defi-optimizer)
- [SUPAH website](https://supah.ai)
- [SUPAH API endpoint](https://api.supah.ai)
- [x402 documentation](https://www.x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, curl, SUPAH_API_BASE when overriding the default API endpoint, outbound access to api.supah.ai, and an x402-compatible payment environment for USDC payments on Base.]

## Skill Version(s):

1.3.0 (source: server release evidence; artifact package.json reports 1.0.0 and runtime help reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
