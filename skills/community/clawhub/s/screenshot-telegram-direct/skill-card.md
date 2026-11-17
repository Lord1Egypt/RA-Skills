## Description:

Capture website screenshots and send to Telegram via direct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niccoreyes](https://clawhub.ai/user/niccoreyes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to capture screenshots of web pages through the Snap API and deliver them to a Telegram chat using direct Telegram Bot API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and screenshots are sent through the Snap API and Telegram.

Mitigation: Use the skill only for pages and screenshots that are acceptable to share with those services.

Risk: Shell-profile environment loading and broad .env sourcing can expose or import unintended secret values.

Mitigation: Avoid persistent shell-profile loading, keep .env files trusted and permission-restricted, and parse only the expected credential keys.

Risk: Temporary screenshot files may remain on disk if execution fails before cleanup.

Mitigation: Use a safer implementation with mktemp and cleanup on all exits before deploying in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niccoreyes/skills/screenshot-telegram-direct)
- [Publisher profile](https://clawhub.ai/user/niccoreyes)
- [Telegram BotFather](https://t.me/BotFather)
- [Telegram userinfobot](https://t.me/userinfobot)
- [Telegram RawDataBot](https://t.me/RawDataBot)
- [Snap API registration endpoint](https://snap.llm.kaveenk.com/api/register)
- [Snap API screenshot endpoint](https://snap.llm.kaveenk.com/api/screenshot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus Telegram bot, Telegram chat, and Snap API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
