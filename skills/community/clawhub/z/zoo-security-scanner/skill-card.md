## Description:

Scan URLs, skills, and infrastructure for security vulnerabilities using the paid ZOO Security Scanner API with x402 USDC payments and no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazycompanyinc](https://clawhub.ai/user/crazycompanyinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to request vulnerability scans for authorized URLs, skills, or infrastructure and interpret the returned score, findings, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to spend USDC through x402 payments.

Mitigation: Require explicit user confirmation for every payment and verify the amount, Base network, recipient address, and scan target before approval.

Risk: Scan targets are submitted to an outside hosted API.

Mitigation: Use the skill only for targets the user owns or is authorized to test, and avoid confidential internal hosts unless disclosure to the provider is acceptable.

Risk: The security review marked the release suspicious because the skill lacks enough user-control safeguards.

Mitigation: Review before installing and disable unattended wallet signing or autonomous scan execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crazycompanyinc/skills/zoo-security-scanner)
- [ZOO Technologies](https://zootechnologies.com)
- [ZOO Security Scanner API](https://api.zootechnologies.com/scan)
- [x402 Discovery](https://xgate.run)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results include status, score, findings, and recommendations when the hosted service returns a response.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
