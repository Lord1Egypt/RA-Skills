## Description:

Work Progress monitors OpenClaw work sessions and daily todos, reports stalled or failed activity, and records local recovery notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor OpenClaw session progress, detect stalled or failed work, inspect outstanding daily todos, and surface recovery recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill periodically inspects local OpenClaw session metadata and todo files and stores task labels and statuses locally.

Mitigation: Install it only in trusted local workspaces where this monitoring and local status storage are acceptable.

Risk: The release describes automatic recovery, but the security evidence indicates current behavior is notification and recommendation rather than actual task restart.

Mitigation: Treat recovery output as guidance for human or agent review before taking restart actions.

## Reference(s):

- [Work Progress ClawHub release page](https://clawhub.ai/amd5/skills/work-progress)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Console text or JSON monitoring reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return NO_REPLY when no issues are found.]

## Skill Version(s):

4.0.6 (source: SKILL.md frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
