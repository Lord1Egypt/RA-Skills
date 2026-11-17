## Description:

Formats Telegram replies using Telegram's actual supported formatting - when to use bold, code, quotes, headings, and structure without overusing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pedram-naghib](https://clawhub.ai/user/pedram-naghib)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to format Telegram-channel replies with supported HTML and rich-message syntax while avoiding unsupported blocks and excessive formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On OpenClaw version mismatch, the skill may lead an agent to send a deliberate test Telegram message before relying on richer formatting.

Mitigation: Send tests only to a controlled recipient, such as a throwaway DM, before using richer formatting in a live reply.

Risk: Some Telegram clients may not support Bot API 10.2 rich messages and may show rich messages incorrectly or as unsupported.

Mitigation: Ask which Telegram client the user is using and fall back to standard HTML formatting when compatibility is uncertain.

Risk: Combining images with rich message blocks can downshift the message to a photo caption, removing rich blocks and applying caption limits.

Mitigation: Send images and rich structured text as separate messages when both are needed.

## Reference(s):

- [Telegram Bot Rich Messages](https://core.telegram.org/bots/features#rich-messages)
- [OpenClaw outbound media-group support issue](https://github.com/openclaw/openclaw/issues/14027)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline HTML, Markdown examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes version-gated rich-message guidance and recommends live testing when OpenClaw behavior is unverified.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
