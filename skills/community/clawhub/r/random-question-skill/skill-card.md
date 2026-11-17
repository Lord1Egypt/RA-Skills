## Description:

A reflective prompting skill that randomly selects questions across eight personal-awareness dimensions and can trigger them manually, on a heartbeat schedule, or through integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiajun4433](https://clawhub.ai/user/wujiajun4433)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to add randomized self-reflection prompts to an agent workflow, including manual check-ins, scheduled heartbeat prompts, and configurable topic coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-prompt users through heartbeat scheduling.

Mitigation: Enable scheduled prompting only with reviewed active hours, trigger probability, and minimum interval settings that fit the user's workflow.

Risk: The skill can use personal context and retain reflective answers.

Mitigation: Before enabling personal context, answer history, backups, or auto-load behavior, confirm where data is stored, how long it is retained, and how to disable or delete it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiajun4433/skills/random-question-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text prompts with YAML, JSON, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduled reflective prompts and configuration guidance for heartbeat behavior, topic selection, statistics, retention, and backups.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
