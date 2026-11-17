## Description:

Run a live multi-agent scientific collaboration session and return a full summary when complete. Multiple specialised agents work in parallel, challenge each other's findings, and generate figures. Results and figures are saved to disk and a summary is returned to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwang108](https://clawhub.ai/user/fwang108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to run a parallel scientific investigation with multiple agents, then review the resulting findings, agreements, challenges, figures, and saved output paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory context may add sensitive or unapproved project details to the research topic.

Mitigation: Review or disable the memory.md context step unless the user explicitly approves the exact context being added.

Risk: Topic text used in shell command templates can be unsafe if raw user input is interpolated.

Mitigation: Pass the topic as a structured argument or safely escaped value, and use the skill only with trusted topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fwang108/skills/scienceclaw-watch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown summary with shell command guidance and saved result file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save session summaries and generated figures under a timestamped run_exports directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
