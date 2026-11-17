## Description:

Habit Tracker Pro helps users define habits, record check-ins, view statistics, and track achievements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for habit-tracking commands and guidance for adding habits, recording check-ins, viewing statistics, and listing achievements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions use a mutable latest-version npx command.

Mitigation: Review the install command before use, prefer a pinned and reviewed ClawHub CLI version, and avoid running it as root or in environments containing unrelated secrets.

Risk: The artifact declares a curl dependency that is not explained by the visible instructions.

Mitigation: Confirm why curl is required before deployment and remove or constrain the dependency if it is unnecessary.

Risk: The documentation is mostly Chinese, which may limit reviewer understanding in multilingual release workflows.

Mitigation: Have a qualified reviewer confirm the visible instructions, pricing claims, and command behavior before publishing or recommending the skill.

## Reference(s):

- [Habit Tracker Pro on ClawHub](https://clawhub.ai/kaising-openclaw1/skills/xiaoming-habit-tracker-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
