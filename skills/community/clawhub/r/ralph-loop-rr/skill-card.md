## Description:

Ralph Loop guides an AI agent to run multi-step tasks autonomously using a persistent plan, progress updates, and Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roboticresults](https://clawhub.ai/user/roboticresults)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep an AI agent moving through a multi-step task with a persistent checklist, bounded retries, progress logging, and concise Telegram status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages autonomous multi-step execution with reduced interruptions for user control.

Mitigation: Use it only for approved tasks where autonomy is desired, and avoid confidential, financial, account, destructive, or externally visible work unless explicit controls are in place.

Risk: The skill stores task text in a persistent task-state file.

Mitigation: Do not include secrets or full prompts verbatim in the state file, and confirm the file is removed when the task is complete.

Risk: The skill sends task updates through Telegram by default.

Mitigation: Send only redacted updates to an approved destination, and make Telegram notifications optional or disabled for sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roboticresults/skills/ralph-loop-rr)
- [ClawHub publisher profile](https://clawhub.ai/user/roboticresults)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with task-state notes, progress updates, and command or code output as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a temporary task-state file and send Telegram progress notifications when the protocol is followed.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
