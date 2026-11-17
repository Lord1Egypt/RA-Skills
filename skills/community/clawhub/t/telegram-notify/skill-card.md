## Description:

Send Telegram direct message alerts for trade entry, exit, and self-heal events with rate limiting and customizable templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[motivationationdaily](https://clawhub.ai/user/motivationationdaily)

### License/Terms of Use:


## Use Case:

Developers and trading automation operators use this skill to have an agent prepare concise Telegram DM alert behavior for trade entry, trade exit, and self-heal or restart events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading alert details may be sent through Telegram.

Mitigation: Confirm that Telegram is acceptable for the alert content and keep bot tokens and chat IDs scoped and private.

Risk: Frequent event alerts can create message spam.

Mitigation: Use the documented cooldown or rate-limit behavior for high-volume trading events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/motivationationdaily/skills/telegram-notify)

## Skill Output:

**Output Type(s):** [guidance, configuration, markdown]

**Output Format:** [Markdown guidance for Telegram alert behavior, templates, and notification settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe DM-only defaults and cooldown or rate-limit behavior for alerts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
