## Description:

Agent安全审计免费版 helps developers run local AI agent security self-checks for code risks, prompt injection patterns, configuration gaps, and tool-permission issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and small teams use this skill to perform pre-release safety checks on single-agent projects, including local code scanning, prompt-injection review, configuration auditing, and tool-permission checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository files and runs shell searches over the selected workspace.

Mitigation: Install and run it only in repositories you intend to audit, and review proposed shell commands before approval.

Risk: Security evidence notes an undocumented external API-integration statement in the artifact.

Mitigation: Treat that line as boilerplate unless the publisher clarifies it, and do not approve unexpected network calls or writes beyond local audit commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/security-audit-agent-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python code examples and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audit findings and remediation guidance that should be reviewed before action.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
