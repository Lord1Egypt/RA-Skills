## Description:

Training Swarm helps agents manage training knowledge, generate quizzes, create study plans, track progress, and send proactive reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and training operators use this skill to structure knowledge bases, produce training quizzes, create learning plans, track learner progress, and prepare reminder workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create persistent training files in a user's home directory.

Mitigation: Require explicit confirmation before creating or updating training records, and review generated file paths before execution.

Risk: Reminder workflows may involve outbound networked channels and employee progress or assessment data.

Mitigation: Confirm recipients, channels, and data content before sending reminders, especially when personal or assessment data is involved.

Risk: Training content, quiz answers, and progress assessments may be incorrect or incomplete.

Mitigation: Review generated materials against the source knowledge base and require human confirmation for assessment results.

## Reference(s):

- [Training Swarm ClawHub skill page](https://clawhub.ai/gaoshung1981888/skills/training-swarm)
- [gaoshung1981888 ClawHub publisher profile](https://clawhub.ai/user/gaoshung1981888)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local training records, knowledge cards, progress reports, and reminder workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
