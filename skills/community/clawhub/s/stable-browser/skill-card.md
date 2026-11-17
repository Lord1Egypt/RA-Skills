## Description:

Set up reliable browser automation using Chrome DevTools Protocol (CDP) instead of the flaky browser extension relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure a dedicated Chrome DevTools Protocol browser profile for more stable browser automation, including scraping, form filling, social media posting, and headed or headless browser control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent CDP-controlled browser profile can expose logged-in browser sessions if sensitive accounts are stored in it.

Mitigation: Use a dedicated low-privilege browser account and avoid storing sensitive sessions in the CDP profile.

Risk: The documented headless server setup can use --no-sandbox, which reduces Chrome process isolation.

Mitigation: Remove --no-sandbox unless it is required in an isolated environment.

Risk: LaunchAgent or systemd auto-start can leave the automation browser available when it is not actively needed.

Mitigation: Disable any auto-start service when browser automation is not in use.

## Reference(s):

- [Manual Setup](references/manual-setup.md)
- [Stable Browser ClawHub Page](https://clawhub.ai/jarvis563/skills/stable-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Chrome CDP setup steps and OpenClaw browser configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
