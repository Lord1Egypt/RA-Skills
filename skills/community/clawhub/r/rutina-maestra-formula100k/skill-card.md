## Description:

Configures the initial Autopilot F100K setup in an OpenClaw agent by collecting personalization details, saving them to a local configuration file, and scheduling selected Telegram-delivered content automation modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to onboard an OpenClaw agent for recurring F100K content automation, including content radar, calendar, trend alert, community digest, metrics, and Instagram pattern-analysis routines delivered through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store contact, profile, niche, schedule, and voice-profile data in cerebro/f100k-config.json.

Mitigation: Review the collected fields with the user before saving, document where the file is stored, and provide clear deletion or reconfiguration guidance.

Risk: The skill creates recurring automations that can continue sending content through Telegram.

Mitigation: Show the proposed automations, schedule, timezone, and delivery channel before activation and require explicit user confirmation.

Risk: The evidence security guidance reports contradictions between Telegram delivery, email collection, and scheduling instructions.

Mitigation: Resolve the Telegram-versus-email and schedule mechanism conflicts before routine installation or broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/rutina-maestra-formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command snippets and JSON configuration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update cerebro/f100k-config.json and request creation of recurring OpenClaw automations.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
