## Description:

Release-day coordination helpers for cutover, verification, and rollback readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiarani](https://clawhub.ai/user/jiarani)

### License/Terms of Use:


## Use Case:

Developers, release managers, and operations teams use this skill during deploy windows to plan rollout steps, check gates, prepare rollback readiness, and produce handoff artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced release commands may not exist in the installing environment.

Mitigation: Verify the local release and workflow commands before relying on the skill during a deploy window.

Risk: The healthcheck script reports a different skill name, which may confuse version or audit checks.

Mitigation: Confirm artifact identity against SKILL.md, server release metadata, or the echo-version script when validating the release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiarani/skills/release-coordination-toolkit)
- [Publisher Profile](https://clawhub.ai/user/jiarani)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown templates, inline shell command examples, and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
