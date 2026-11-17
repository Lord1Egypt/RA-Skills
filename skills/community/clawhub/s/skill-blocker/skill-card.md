## Description:

Blocks risky commands, unsafe file operations, suspicious network requests, credential access, code injection, and unauthorized system changes before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squallfire](https://clawhub.ai/user/squallfire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a security gatekeeper to review proposed agent actions and block behavior associated with destructive deletion, credential access, code injection, data exfiltration, or unauthorized system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to disable installed skills or alter global blocklists, which could interrupt normal workflows or change persistent skill state.

Mitigation: Install only when strict blocking is desired, and require user confirmation before quarantine, disablement, or blocklist changes.

Risk: Strict blocking rules may over-block legitimate shell, browser, or file operations.

Mitigation: Review blocked actions with the user and maintain a narrow allowlist for approved read-only or routine commands.

Risk: Audit log examples include operation details that may contain sensitive context.

Mitigation: Store audit logs outside agent memory where possible and redact credentials, personal data, and secret paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squallfire/skills/skill-blocker)
- [ClawHub publisher profile](https://clawhub.ai/user/squallfire)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline command examples and JSON audit-log examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend blocking or disabling risky operations and skills; no executable implementation is bundled in the artifact.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
