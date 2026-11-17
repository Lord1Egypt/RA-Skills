## Description:

Automates Telegram Web bot check-ins with agent-browser, including persistent Chrome profile setup for retaining Telegram login cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanbeizizi-max](https://clawhub.ai/user/lanbeizizi-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to guide Telegram Web check-in automation for bots such as OKEmbyBot, including persistent login setup and result verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a startup watchdog that can keep an authenticated Telegram Web browser session running and relaunch it after closure.

Mitigation: Review the watchdog section before use, avoid enabling the LaunchAgent unless continuous relaunch is intentional, and prefer user-invoked runs for normal check-ins.

Risk: Persistent Chrome profiles and profile backups can retain Telegram cookies and account sessions.

Mitigation: Use a dedicated browser profile, restrict local access to profile backups, and delete or rotate the profile when the session should no longer persist.

Risk: The watchdog setup references a hard-coded local script path.

Mitigation: Confirm the script path and contents before loading any LaunchAgent or startup service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanbeizizi-max/skills/telegram-checkin)
- [Telegram Web](https://web.telegram.org)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and a shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation instructions and optional local service configuration; screenshots may be generated for check-in verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
