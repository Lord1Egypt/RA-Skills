## Description:

Self-healing monitor for OpenClaw gateways, crons, agent sessions, auth, budgets, and token costs that sends Telegram alerts and can auto-fix supported failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relayplane](https://clawhub.ai/user/relayplane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams running OpenClaw in production use this skill to monitor gateway, cron, session, auth, budget, and token-cost health, receive Telegram alerts, and run or configure supported remedial actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram approval callbacks can trigger disruptive administrative actions without verifying who pressed the button.

Mitigation: Keep approvals in a private/admin-only chat, avoid callback buttons in shared groups until sender and chat authorization is fixed, and prefer dry-run or manual CLI review for sensitive actions.

Risk: Heal-tier operation can restart services, run or disable crons, refresh auth, and kill sessions.

Mitigation: Start with `clawdoctor start --dry-run`, review configuration before enabling auto-fix, and rely on snapshots and audit logs when taking healing actions.

Risk: License activation sends the license key to clawdoctor.dev, and systemd installation adds persistence.

Mitigation: Activate licenses only when that external validation is acceptable, and enable the systemd service only when persistent monitoring is intended.

## Reference(s):

- [ClawDoctor homepage](https://clawdoctor.dev)
- [ClawDoctor documentation](https://clawdoctor.dev/docs)
- [ClawDoctor npm package](https://www.npmjs.com/package/clawdoctor)
- [ClawDoctor GitHub project link from artifact](https://github.com/turleydesigns/clawdoctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw-specific operational commands; dry-run and approval review are recommended before enabling healing actions.]

## Skill Version(s):

0.4.13 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
