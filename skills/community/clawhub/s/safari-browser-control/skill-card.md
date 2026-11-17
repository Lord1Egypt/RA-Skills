## Description:

Controls the user's real Safari browser on macOS with AppleScript, JavaScript execution, and screenshots for reading pages, navigating tabs, clicking elements, and filling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdlll](https://clawhub.ai/user/sdlll)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users on macOS use this skill to operate an existing Safari session for browser tasks that require real cookies, logins, tabs, screenshots, or page interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over the user's logged-in Safari session, including visible page data, cookies, open tabs, form input, navigation, and clicks.

Mitigation: Use it only when intentional, preferably in a dedicated low-risk Safari profile or browser session, and avoid banking, admin consoles, private accounts, or sensitive open tabs.

Risk: The skill uses an unsafe temporary helper pattern for its screenshot window-id helper.

Mitigation: Fix the temporary helper pattern before routine use, and review generated helper files and commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdlll/skills/safari-browser-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with AppleScript, JavaScript, Swift, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and guidance for local Safari automation; does not create a standalone service.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
