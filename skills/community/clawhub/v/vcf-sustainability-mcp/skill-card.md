## Description:

An MCP server that interfaces with VMware Aria Operations to extract Green IT metrics, carbon footprint data, and the organizational Green Score for ESG reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasture-rohit](https://clawhub.ai/user/kasture-rohit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform teams use this skill to expose VMware Aria Operations sustainability metrics through an MCP tool for ESG and Green IT reporting. It helps agents retrieve Green Score, carbon footprint, power consumption, and related sustainability report data from a configured Aria Operations environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an Aria Operations API token over HTTPS while certificate checks are disabled.

Mitigation: Use a least-privilege, read-only token and require proper TLS certificate validation or a trusted CA bundle before production use.

Risk: The skill can return simulated-looking sustainability metrics after live API failures.

Mitigation: Treat fallback metrics as unsafe for ESG reporting unless mock mode is explicitly controlled and clearly labeled.

Risk: Dependencies are not pinned in the artifact requirements.

Mitigation: Pin and review dependency versions before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kasture-rohit/skills/vcf-sustainability-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report text or error string returned by an MCP tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARIA_OPS_HOST and ARIA_OPS_API_TOKEN environment variables. Security evidence notes that fallback report data may be simulated after live API failures.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
