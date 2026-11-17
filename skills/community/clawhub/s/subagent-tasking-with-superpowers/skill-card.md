## Description:

Guides agents to check using-superpowers, split complex work into focused subagent tasks, write task briefs, and verify completion traces before spawning subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilixiong](https://clawhub.ai/user/weilixiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route complex tasks through focused subagents with written task briefs and result checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires routing subagent work through another skill, which can override normal task judgment.

Mitigation: Review before installation and apply only in workspaces where mandatory superpowers checks are expected.

Risk: The skill directs agents to write task briefs under /tmp/tasks, which can persist task details locally.

Mitigation: Avoid sensitive data in task briefs and clear local task files according to workspace policy.

Risk: The skill asks agents to leave completion traces in an undefined forum, which could disclose workflow details.

Mitigation: Post traces only to approved destinations and review content before sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/weilixiong/skills/subagent-tasking-with-superpowers)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with task brief templates and inline shell-style command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct creation of local task brief files under /tmp/tasks and completion traces depending on the agent environment.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
