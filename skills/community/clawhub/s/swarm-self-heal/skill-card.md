## Description:

Swarm reliability watchdog for OpenClaw — validates gateway/channel and every lane, performs bounded recovery, and emits auditable receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations engineers use this skill to check OpenClaw gateway, channel, and lane health, perform bounded restart-and-retry recovery, and collect receipts for incident timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can create persistent OpenClaw cron jobs.

Mitigation: Review the cron changes before running setup, keep only the watchdog lanes you intend to operate, and add an uninstall or rollback path for deployed jobs.

Risk: Diagnostic output may be sent to Telegram, including through a fallback recipient.

Mitigation: Configure a recipient you control before installation, remove the hardcoded fallback, and redact raw diagnostics before external delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tkuehnl/skills/swarm-self-heal)
- [ClawHub Publisher Profile](https://clawhub.ai/user/tkuehnl)
- [Project Homepage](https://github.com/cacheforge-ai/cacheforge-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and machine-parseable watchdog receipt fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Watchdog runs emit timestamp, targets, ok_agents, failed_agents, actions, VERDICT, and RECEIPT fields.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
