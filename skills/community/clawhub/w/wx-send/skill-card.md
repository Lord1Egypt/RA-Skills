## Description:

Automates WeChat on macOS to send a message to a specified contact, with an optional OCR helper for reading the current chat window before drafting a reply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libero1980](https://clawhub.ai/user/libero1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to automate sending requested WeChat messages on macOS and to inspect visible chat text for a potential reply workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real messages through a live WeChat desktop session.

Mitigation: Run it only for messages explicitly requested by the user, and require confirmation of both recipient and exact message before sending.

Risk: The OCR helper can capture sensitive screen content.

Mitigation: Close or hide unrelated sensitive content before OCR, capture only the intended chat region when possible, and delete temporary screenshots after use.

Risk: The automation uses clipboard and UI focus state, which can send content to the wrong destination if WeChat search or focus changes.

Mitigation: Verify the selected chat before execution, preserve and restore clipboard contents, and avoid interacting with the machine while the automation is running.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libero1980/skills/wx-send)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing automation guidance and command examples for macOS WeChat workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
