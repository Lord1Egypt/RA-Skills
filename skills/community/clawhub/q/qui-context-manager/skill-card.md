## Description:

AI-powered context management for OpenClaw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect session context usage, generate AI summaries, and compress long sessions by backing up, resetting, and reinjecting summarized context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compression can back up full OpenClaw session files and store generated summaries on disk, which may preserve sensitive conversation content.

Mitigation: Use it only on sessions whose backup storage is protected, avoid sessions containing secrets, and clean up stored backups and summaries according to local retention needs.

Risk: Replacement mode deletes the active session JSONL after making a backup, so an incorrect target or failed restore path can disrupt the current session.

Mitigation: Run read-only summarization first, confirm the target session key, and keep the generated backup available before relying on replacement mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-context-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated summary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create AI summary, session backup, transcript, and legacy summary files under memory/compressed/ when compression runs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
