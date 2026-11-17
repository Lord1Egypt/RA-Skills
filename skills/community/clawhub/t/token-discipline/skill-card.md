## Description:

Helps agents reduce context spent on tool output and repetition by filtering command results and summarizing findings concisely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill while running diagnostics, reading files, and reporting results to limit transcript context while retaining relevant information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly aggressive output filtering may hide details needed to diagnose an issue.

Mitigation: Choose filters that preserve task-relevant evidence, and inspect the needed details before relying on a conclusion.

## Reference(s):

- [token-discipline on ClawHub](https://clawhub.ai/147258xuan/skills/token-discipline)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Markdown]

**Output Format:** [Concise Markdown or plain text, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends filtering command output to about 30 lines by default.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
