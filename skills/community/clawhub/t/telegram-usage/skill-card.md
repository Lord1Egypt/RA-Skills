## Description:

Display session usage statistics including quota, session time, tokens, and context usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-drew](https://clawhub.ai/user/c-drew)

### License/Terms of Use:


## Use Case:

Clawdbot users and operators use this skill to view current Telegram-accessible usage status, including API quota, session reset timing, token counts, context usage, provider, and model details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local Clawdbot session files, which may contain sensitive conversation or usage data.

Mitigation: Review before installing in environments with sensitive sessions or shared accounts, and restrict access to only the intended local session files.

Risk: The skill uses local command execution and local state to collect quota information.

Mitigation: Run it only in a trusted Clawdbot environment and document expected local reads, writes, and commands before deployment.

Risk: Unescaped Telegram HTML or unvalidated session identifiers could expose confusing or unsafe output behavior.

Mitigation: Validate session and agent identifiers, and escape Telegram HTML before sending formatted output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c-drew/skills/telegram-usage)
- [Clawdbot skills documentation](https://docs.clawd.bot/tools/skills)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Telegram-safe HTML text or JSON statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Clawdbot session state; reads current session and quota data when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
