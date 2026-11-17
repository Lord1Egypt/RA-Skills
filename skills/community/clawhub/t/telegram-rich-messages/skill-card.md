## Description:

Comprehensive guide for Telegram Rich UI features (Inline buttons, formatting, media, reactions, and message management). Use this skill to provide a low-friction, interactive experience for Telegram users, prioritizing buttons over typing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shingo0620](https://clawhub.ai/user/shingo0620)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to help OpenClaw agents compose Telegram messages with inline buttons, formatting, reactions, media uploads, and message management patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable examples include a fixed Telegram recipient and could send content to the wrong chat if copied directly.

Mitigation: Replace fixed Telegram targets with the authenticated active chat before sending messages or media.

Risk: The skill includes local file upload patterns that could expose unintended or sensitive files.

Mitigation: Send only files intentionally created or selected for the current task, and require confirmation before uploads or deletions involving sensitive content.

## Reference(s):

- [Telegram UI Decision Matrix](references/decision-matrix.md)
- [Telegram Formatting Guide](references/formatting.md)
- [Telegram Interactive UI](references/interactive-ui.md)
- [Telegram Media & Message Actions](references/media-and-actions.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with JSON examples and Telegram message patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Telegram plugin declared in OpenClaw metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
