## Description:

PublishGuard helps agents verify that published posts are actually reachable, check platform-specific posting rules, track rate limits, and manage platform credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill before and after publishing content to verify public post URLs, validate platform requirements, observe rate limits, and keep reusable credential guidance across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist real account credentials, and the security review does not consider the current credential path safe for real platform tokens.

Mitigation: Use a proper secret store or independently audited encryption before storing production tokens; otherwise use only test credentials.

Risk: URL verification can request arbitrary URLs from the agent host.

Mitigation: Restrict verification to expected public post URLs on intended platforms and review target URLs before execution.

Risk: Audit logs may retain full URLs, titles, post IDs, diagnoses, and error details.

Mitigation: Clear or rotate audit logs and avoid including sensitive content in post titles, URLs, or error fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/publish-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python API results, JSONL audit records, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write encrypted credential vault files and local audit logs when used by an agent.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
