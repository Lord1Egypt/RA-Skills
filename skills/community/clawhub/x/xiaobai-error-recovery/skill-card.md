## Description:

4R error recovery framework. Recognize, Rescue, Report, Remember. Never lose work silently. Trigger on: 'error', 'failed', 'crash', 'something went wrong', 'retry'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recognize task failures, attempt bounded recovery, report unresolved errors, and preserve recovery notes so work is not silently lost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent error logs may capture sensitive task details, credentials, or other confidential context.

Mitigation: Record only necessary error details, redact secrets, and require approval before writing persistent memory or error logs.

Risk: Updating AGENTS.md, skill files, or workflow guidance can change future agent behavior beyond the current task.

Mitigation: Require human review before modifying agent guidance, skill instructions, or workflow files.

Risk: Recovery steps may involve alternate authentication paths, elevated permissions, package installs, or repeated operations.

Mitigation: Require explicit approval before using credentials, requesting elevated permissions, installing packages, or retrying destructive operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown/text guidance with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic categories, bounded retry steps, human escalation notes, and persistent error-log guidance.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
