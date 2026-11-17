## Description:

Screen any agent skill or MCP server BEFORE it lands in the fleet: compare the declared manifest against actual behavior, flag injection and credential patterns, and emit a pass/fail verdict with evidence. Use when installing skills from a marketplace, vendoring an MCP server, or when a fleet rule requires a pre-install security gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcircuitbreaker](https://clawhub.ai/user/0xcircuitbreaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and fleet operators use this skill to review agent skills and MCP servers before installation, compare declared behavior with package contents, and record a security verdict with evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted scans send package contents to an external provider; the material may include live secrets or content you are not authorized to share.

Mitigation: Remove live secrets and submit only package contents you are authorized to share with the named provider. Review the evidence yourself; a clean scan does not guarantee safety.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/0xcircuitbreaker/skills/skill-install-firewall)
- [Skill Safety Scan service](https://agents.daedalusdevelopmentgroup.com)
- [Skill Safety Scan endpoint](https://agents.daedalusdevelopmentgroup.com/v1/ai-skill-safety-scan)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Markdown guidance and JSON findings report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package findings, scan identifier, verdict, and evidence URL.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
