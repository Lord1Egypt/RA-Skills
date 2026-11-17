## Description:

Provides an agent-facing wrapper for running authorized commands with superuser or alternate-user privileges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill when an agent must inspect sudo permissions or run explicitly authorized system administration commands that require elevated privileges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad root command execution can make system-wide changes or expose protected data when invoked by an agent.

Mitigation: Constrain sudoers permissions to the smallest required command set and require explicit human approval before elevated commands run.

Risk: Commands copied from web pages, documents, tool output, or other untrusted text may be executed with elevated privileges.

Mitigation: Treat untrusted command text as input requiring human review, and avoid passing it directly to this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires host sudo authorization and sudoers configuration outside the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
