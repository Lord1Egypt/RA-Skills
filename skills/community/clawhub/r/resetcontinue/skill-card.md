## Description:

Generate a concise copy-paste session handoff for continuing the current task in a fresh chat after /new or /reset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kisssam6886](https://clawhub.ai/user/kisssam6886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve the current task state, blockers, confirmed facts, and immediate next action when moving work into a fresh chat after /new or /reset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated handoff summaries may include sensitive context already present in the chat, such as credentials or private operational details.

Mitigation: Ask the agent to redact passwords, API keys, tokens, and private credentials before pasting the handoff into a new session.

Risk: A concise handoff can omit context that later turns out to matter for continuing the task accurately.

Mitigation: Review the summary before reuse and add any missing blocker, file path, environment, or next action that is still relevant.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kisssam6886/skills/resetcontinue)
- [Publisher profile](https://clawhub.ai/user/kisssam6886)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown-style handoff summary in Simplified Chinese unless the user asks otherwise]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight items or fewer; ends with the required final handoff line.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
