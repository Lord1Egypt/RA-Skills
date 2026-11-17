## Description:

Monitor and recap official X (Twitter) updates using actionbook-rs screenshots. Use when the user asks to track/recap X posts (especially official accounts like @AnthropicAI/@claudeai), set up or fix cron-based X monitoring, troubleshoot X login/spinner blank timelines, or standardize the fetch to screenshot to recap workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack4world](https://clawhub.ai/user/jack4world)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor official X accounts, capture screenshots through an authenticated browser profile, and produce concise recaps of relevant updates. It also helps maintain cron-based X monitoring workflows and troubleshoot blank timelines, expired logins, spinner-only captures, and gateway issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated X screenshots may include account identifiers, notification counts, or other private session context.

Mitigation: Use the skill only with an X browser profile approved for this purpose, and review or delete saved screenshots when they may contain private session context.

Risk: X session expiry, consent walls, bot detection, or rate limits can produce blank, spinner-only, partial, or inconsistent screenshots.

Mitigation: Re-login with the configured profile, prefer official profile pages, reduce fetch frequency if needed, and rely on the scripts' retry and file-size checks before recapping.

## Reference(s):

- [X Recap runbook](references/runbook.md)
- [Official AnthropicAI X profile](https://x.com/AnthropicAI)
- [Official claudeai X profile](https://x.com/claudeai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or concise text recap with optional bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recaps are based on locally saved screenshots from official X pages; no fixed token cap is specified.]

## Skill Version(s):

2026.2.25 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
