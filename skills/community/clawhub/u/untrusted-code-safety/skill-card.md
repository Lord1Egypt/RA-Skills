## Description:

Guides agents through static review, controlled sandbox testing, and escalation when handling code from unknown sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to assess unfamiliar repositories, packages, scripts, and executable configuration before deciding whether to run them. It provides static triage, containment, stop-and-alert, and cleanup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested global Git and npm settings can persist and affect unrelated work.

Mitigation: Use per-command, repository-local, or temporary-HOME settings instead; explicitly restore any persistent settings changed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a stop-and-alert procedure and cleanup guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
