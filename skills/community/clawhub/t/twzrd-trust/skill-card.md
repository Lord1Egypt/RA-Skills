## Description:

Helps agents discover x402 services and assess a seller's payment risk before signing or paying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twzrd-sol](https://clawhub.ai/user/twzrd-sol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use the skill to discover x402 callables, check seller wallets and listings, and gate payments based on preflight and merchant risk assessments. Optional paid checks provide additional trust and merchant history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service responses may suggest commands or tooling that affect a wallet payment flow.

Mitigation: Run only fixed, reviewed commands and never execute command strings returned by TWZRD responses.

Risk: Changing payment-tool versions or skill updates may alter pre-signing behavior.

Mitigation: Use reviewed, pinned package versions and update the skill only through a trusted installation channel.

Risk: A mistaken payment network, recipient, or amount can lead to unintended spending.

Mitigation: Confirm the network, recipient, and amount before any signing step.

## Reference(s):

- [TWZRD Trust skill documentation](https://intel.twzrd.xyz/skill.md)
- [TWZRD MCP endpoint](https://intel.twzrd.xyz/mcp)
- [TWZRD OpenAPI reference](https://intel.twzrd.xyz/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free risk assessments and optional paid x402 trust checks.]

## Skill Version(s):

1.13.34 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
