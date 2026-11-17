## Description:

Automate real Chrome browser sessions on macOS through a CLI, Chrome extension, WebSocket session, and macOS control helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tahcia](https://clawhub.ai/user/tahcia)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Tahcia Console to operate a real Chrome browser on macOS for UI tasks that need screenshots, OCR, accessibility-tree inspection, and physical mouse or keyboard actions. It is intended for browser and desktop automation workflows where headless browser automation is not suitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue real desktop-level browser, mouse, keyboard, screenshot, and OCR actions on macOS.

Mitigation: Review proposed command sequences before execution and require explicit confirmation for actions outside the requested browser tab.

Risk: The workflow may process screen contents through external services.

Mitigation: Confirm before sending screenshots or screen-derived content to third-party APIs and avoid capturing sensitive information.

Risk: The skill may rely on local secrets or API keys.

Mitigation: Use environment variables or protected local configuration and avoid storing raw API keys in broadly readable files.

Risk: The artifact describes writing learned behavior back into the skill file.

Mitigation: Review and approve any file modifications before persistence, especially changes to skill instructions or automation rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tahcia/skills/tahcia-console)
- [Tahcia Console](https://www.tahcia.com/console)
- [Tahcia commands](https://www.tahcia.com/commands)
- [Tahcia API server](https://api.tahcia.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include CLI commands for real browser and macOS control; users should review commands before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
