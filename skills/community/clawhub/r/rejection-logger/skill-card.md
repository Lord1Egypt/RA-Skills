## Description:

Captures and logs choices, options, or prompts that an agent evaluated and decided not to execute, so skipped tasks, rejected approaches, or alternative methods can be documented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to record rejected tasks, skipped approaches, and chosen alternatives in a workspace audit log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive prompts, personal data, or internal decision details in plaintext audit logs.

Mitigation: Use only in workspaces where persistent audit logs are acceptable, keep .learnings/REJECTIONS.md out of version control unless intentionally shared, and record sanitized high-level summaries instead of raw sensitive details.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown log entries and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends entries to .learnings/REJECTIONS.md when used with the bundled shell script.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
