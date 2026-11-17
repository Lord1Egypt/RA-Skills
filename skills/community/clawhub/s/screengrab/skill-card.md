## Description:

Screengrab captures the current macOS screen without opening a browser, saving images to /tmp or a custom path with support for multiple displays and periodic watch mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture the visible state of a macOS desktop for debugging, visual verification, app-state checks, or remote awareness. It is also useful for listing connected displays and capturing a selected display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture sensitive information visible on the current Mac screen.

Mitigation: Use it only when screen capture is intentional, and close or hide sensitive windows before running it.

Risk: Watch mode can keep saving screenshots to disk over time.

Mitigation: Prefer one-shot captures, or set an explicit count and output directory when periodic capture is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wrentheai/skills/screengrab)
- [Publisher profile](https://clawhub.ai/user/wrentheai)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PNG screenshot files on macOS and can print the saved path for downstream image analysis.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
