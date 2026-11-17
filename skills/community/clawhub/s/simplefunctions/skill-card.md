## Description:

SimpleFunctions is an AI-native prediction market runtime for Kalshi and Polymarket that supports thesis tracking, edge scanning, position monitoring, trade execution through a CLI, and Telegram alerts for human users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrickliu0077](https://clawhub.ai/user/patrickliu0077)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to install and operate the SimpleFunctions CLI for prediction-market thesis management, market scanning, portfolio monitoring, and trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unaudited global CLI and connect live financial credentials.

Mitigation: Verify the npm package and publisher before installation, and use read-only or least-privilege credentials where available.

Risk: Trading workflows can affect real financial positions.

Mitigation: Require explicit human confirmation before allowing an agent to place trades or run natural-language trading workflows.

Risk: Telegram alerts can disclose trading-related context to a third-party channel.

Mitigation: Use Telegram alerts only for information the user is comfortable sharing through Telegram, and avoid routing sensitive trading context there unless the publisher documents suitable privacy controls.

## Reference(s):

- [SimpleFunctions Skill on ClawHub](https://clawhub.ai/patrickliu0077/skills/simplefunctions)
- [SimpleFunctions Homepage](https://simplefunctions.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI commands and environment variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing command guidance; CLI commands support JSON output where documented.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
