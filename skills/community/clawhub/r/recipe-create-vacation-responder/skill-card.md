## Description:

Enable a Gmail out-of-office auto-reply with a custom message and date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace administrators use this skill to enable, verify, and later disable a Gmail vacation responder with a custom out-of-office message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vacation responder messages can disclose travel status, return dates, or internal escalation contacts to a broader audience than intended.

Mitigation: Review the message before enabling it, avoid sensitive travel or internal escalation details, and restrict replies to contacts or the user's domain when appropriate.

Risk: An example or incomplete date range can leave an out-of-office reply active longer than intended.

Mitigation: Set and verify the actual start and end dates supported by the Gmail tooling, and run the disable command when the responder is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-create-vacation-responder)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the gws command-line tool and the gws-gmail prerequisite skill.]

## Skill Version(s):

1.0.12 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
