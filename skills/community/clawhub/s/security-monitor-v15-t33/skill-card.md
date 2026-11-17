## Description:

Provides Linux/Unix server security auditing for processes, network connections, open ports, file permissions, sensitive information exposure, logs, and process trees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t33-coder](https://clawhub.ai/user/t33-coder)

### License/Terms of Use:

MIT-0

## Use Case:

System administrators and security-minded developers use this skill to audit Linux/Unix servers, investigate suspicious activity, review exposed services, and produce findings that support follow-up remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad host inspection can expose sensitive operational data in reports or scheduled logs.

Mitigation: Run the skill only on systems you administer, prefer targeted unprivileged checks first, and protect any report or cron log output.

Risk: Some checks require elevated privileges to inspect complete process, network, log, and file-permission state.

Mitigation: Use sudo only for checks that require it and review generated findings before taking remediation action.

Risk: Findings for non-standard ports, high-resource processes, or secret-like strings can require human confirmation.

Mitigation: Compare findings against expected services and rotate credentials only after confirming an exposure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/t33-coder/skills/security-monitor-v15-t33)
- [Server Security Checklist](artifact/references/security-checklist.md)
- [Common Service Port Reference](artifact/references/common-ports.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and Python snippets; the monitor script emits human-readable reports and JSON-formatted scan results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include process arguments, usernames, internal paths, log excerpts, and locations of suspected secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact docs describe the monitor tool as v1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
