## Description:

yan-learning-engine schedules hourly self-learning, contribution, planning, and self-check tasks for an agent persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eightroad](https://clawhub.ai/user/eightroad)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators can use this skill to drive recurring learning, contribution, planning, and progress-tracking routines. It is best treated as a scheduler and workflow prompt that requires review before any autonomous external action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill repeatedly tells the agent to publish, submit, modify repositories, and post externally without asking first.

Mitigation: Before use, remove no-confirmation language and require explicit approval for publishing, repository changes, pull requests, issue filing, comments, and public posts.

Risk: The skill provides an hourly cron workflow that can trigger unattended recurring actions.

Mitigation: Disable or avoid the cron entry unless the execution environment has clear human approval gates and scoped permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eightroad/skills/yan-learning-engine)
- [Publisher profile](https://clawhub.ai/user/eightroad)
- [SKILL.md](artifact/SKILL.md)
- [EXECUTION_RULES.md](artifact/EXECUTION_RULES.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON progress files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill includes hourly scheduling guidance, a shell runner, and JSON files for plans, progress, and self-check reports.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
