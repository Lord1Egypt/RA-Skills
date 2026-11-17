## Description:

Scans OpenClaw skill instructions for suspicious patterns and reports findings for manual review before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anikrahman0](https://clawhub.ai/user/anikrahman0)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users assess prospective or installed skills for suspicious instructions and review reported risks before deciding whether to install or retain them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scan may incorrectly classify a dangerous skill as safe.

Mitigation: Manually inspect every skill before installation; do not use a SAFE result as proof of safety or the current whitelist logic as a security gate.

Risk: Scanning an overly broad path may read files outside the skill package under review.

Mitigation: Limit scan paths to the intended skill package.

Risk: Pattern matches may flag harmless skill instructions.

Mitigation: Review each finding in context before acting on it.

## Reference(s):

- [Security Skill Scanner on ClawHub](https://clawhub.ai/anikrahman0/skills/security-skill-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown assessment or plain-text scan report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pattern findings and risk levels are advisory, not a safety guarantee.]

## Skill Version(s):

2.0.0 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
