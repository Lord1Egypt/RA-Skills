## Description:

Automatically onboard new Telegram groups so the bot responds immediately, with project setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose Telegram groups where an OpenClaw bot is present but not responding, then add the group to configuration and create project records for that group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says this skill recommends and defaults to broad Telegram group access where any group member can trigger the bot and every message may be processed.

Mitigation: Install only when broad Telegram group onboarding is intended; prefer allowlist mode, verify the group and administrator, and use requireMention=true unless full-channel listening is explicitly approved.

Risk: Onboarded groups and project records can persist after the immediate setup task.

Mitigation: Document how to remove the group configuration and associated project records during offboarding.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/moltbotmolty-del/skills/telegram-group-onboard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose configuration changes, project files, and operational verification steps.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
