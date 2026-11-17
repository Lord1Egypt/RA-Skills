## Description:

Smart contract escrow for agent-to-agent payments with delivery confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create, fund, monitor, and release smart contract escrow agreements for agent-to-agent services after delivery confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live escrow workflows can fund, release, refund, dispute, or configure auto-release for real-value payments without clear approval gates or safety limits.

Mitigation: Use a tightly scoped Sardis API key, spending limits, known wallet allowlists, and explicit human approval before every fund, release, refund, dispute, milestone, or auto-release setting.

Risk: The npm dependency is listed without pinning or justification in the release evidence.

Mitigation: Treat the dependency as unnecessary unless the publisher pins and justifies it.

## Reference(s):

- [Sardis Homepage](https://sardis.sh)
- [Sardis Escrow Documentation](https://sardis.sh/docs/escrow)
- [Sardis API Reference](https://api.sardis.sh/v2/docs)
- [Sardis Smart Contracts](https://github.com/sardis-sh/contracts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SARDIS_API_KEY, curl, and jq.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
