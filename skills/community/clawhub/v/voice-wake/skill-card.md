## Description:

Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe-evolver](https://clawhub.ai/user/pe-evolver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent speak responses aloud on macOS only when a Voice Wake trigger is present, while keeping normal typed interactions text-only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spoken responses may be overheard by people nearby, especially if the trigger is used during sensitive conversations.

Mitigation: Use the Voice Wake trigger only in private environments for sensitive content; otherwise rely on the text response.

Risk: The skill depends on the local macOS `say` command and cannot provide speech output when that command is unavailable or fails.

Mitigation: Continue with the text response and note the speech failure so the user still receives the answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pe-evolver/skills/voice-wake)
- [Publisher profile](https://clawhub.ai/user/pe-evolver)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger local macOS speech output with `say` when the required Voice Wake phrase starts the user message.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
