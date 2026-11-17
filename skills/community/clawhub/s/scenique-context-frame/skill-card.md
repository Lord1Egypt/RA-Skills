## Description:

Detects topic switches in conversations and creates or manages context frames to preserve work-related context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shewingong](https://clawhub.ai/user/shewingong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can use this skill to detect conversation topic changes, create context frames, and demonstrate frame creation through a simulated conversation flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can execute a file outside the reviewed package.

Mitigation: Before production use, resolve and execute only packaged files from the reviewed artifact.

Risk: The demo can retain conversation snippets in a fixed workspace path without user notice.

Mitigation: Disclose persistence, disable it by default where practical, and use a user-scoped configurable storage path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shewingong/skills/scenique-context-frame)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain-text status summaries with simulated conversation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report context-switch decisions, frame titles, frame summaries, and demonstration run output.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
