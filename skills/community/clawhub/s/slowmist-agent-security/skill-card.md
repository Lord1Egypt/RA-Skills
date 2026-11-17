## Description:

SlowMist Agent Security provides a comprehensive security review framework for AI agents covering skill and MCP installation, repositories, URLs and documents, on-chain addresses, products and services, and social shares.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slowmist](https://clawhub.ai/user/slowmist)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to route external inputs through standardized security review workflows and produce risk-rated Markdown reports before installation, execution, transactions, or adoption decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes dangerous command and attack-pattern examples as teaching material, which can be mistaken for executable recommendations if read without context.

Mitigation: Treat artifact files as reference evidence only, do not execute example commands, and require explicit human approval before acting on external code or instructions.

Risk: The framework intentionally favors caution and may over-flag benign content during security review.

Mitigation: Use the standardized report templates, documented false-positive guidance, and human decision authority for HIGH or REJECT ratings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/slowmist/skills/slowmist-agent-security)
- [SlowMist Agent Security Homepage](https://github.com/slowmist/slowmist-agent-security)
- [OpenClaw Security Practice Guide](https://github.com/slowmist/openclaw-security-practice-guide)
- [SlowMist](https://slowmist.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown security review reports and concise risk-rated recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template-driven reports with four-level LOW, MEDIUM, HIGH, and REJECT ratings.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
