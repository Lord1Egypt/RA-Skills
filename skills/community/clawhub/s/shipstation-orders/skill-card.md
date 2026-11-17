## Description:

Monitor ShipStation orders, detect issues, and send alerts for e-commerce businesses using ShipStation for order fulfillment across multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cprice70](https://clawhub.ai/user/cprice70)

### License/Terms of Use:

MIT

## Use Case:

External e-commerce operators and developers use this skill to monitor ShipStation orders, detect new or delayed orders, identify orders on hold, and surface expedited shipping items for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires ShipStation API credentials to query order data.

Mitigation: Keep credentials in a local .env file or environment variables, avoid committing secrets, and install only where sharing ShipStation API access is acceptable.

Risk: The scripts create local state files containing processed order IDs and check timestamps.

Mitigation: Store the skill in a trusted workspace and review local state retention before using it with sensitive operational data.

Risk: Recurring heartbeat or cron use can repeatedly access ShipStation and trigger external notifications.

Mitigation: Review scheduled execution and notification wrappers before enabling recurring checks.

## Reference(s):

- [ShipStation API V1 documentation](https://www.shipstation.com/docs/api/)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/cprice70/skills/shipstation-orders)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ShipStation API credentials and creates local state files to track processed orders and check timestamps.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
