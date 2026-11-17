## Description:

Query Fuku Sportsbook data, manage a betting agent, receive pick notifications, and access predictions for CBB, NBA, NHL, and Soccer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptopunk2070](https://clawhub.ai/user/cryptopunk2070)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query sports predictions, odds, team and player stats, and manage Fuku Sportsbook betting agents, subscriptions, webhooks, and notifications through natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit and store betting-agent credentials and can support automated bet posting.

Mitigation: Use only with a trusted publisher and service, keep credentials in a dedicated configuration location, and require explicit user approval before enabling automated bet posting.

Risk: The skill may expose wallet recovery material and betting account details in agent output.

Mitigation: Treat wallet seed phrases and account identifiers as secrets, avoid logging or sharing outputs that contain them, and move funds only after independently verifying the wallet and service flow.

Risk: The skill polls a remote service on each run and can register webhooks for notifications.

Mitigation: Review the configured API base and webhook URLs before installation, use HTTPS endpoints, and disable notification polling or webhooks when they are not required.

## Reference(s):

- [ClawHub Sportsbook Skill](https://clawhub.ai/cryptopunk2070/skills/sportsbook)
- [Artifact README](artifact/README.md)
- [Fuku Sportsbook API](https://cbb-predictions-api-nzpk.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown text with shell commands and JSON/API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include betting-agent status, picks, odds, notification summaries, webhook setup details, and credential handling guidance.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
