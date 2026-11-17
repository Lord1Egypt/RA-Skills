## Description:

Track shipments and manage trackers using Ship24's universal tracking API -- 2,500+ couriers and eCommerce platforms worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ship24](https://clawhub.ai/user/ship24)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to track orders, create and manage shipment trackers, retrieve delivery status, and replay webhook events through Ship24.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers, client tracker IDs, destination details, and tracker actions may be sent to Ship24.

Mitigation: Use an appropriate Ship24 API key and avoid sending shipment or order data that should not be shared with Ship24.

Risk: Tracker creation, bulk tracker creation, and webhook replay actions may affect the user's Ship24 account or billing.

Mitigation: Confirm account-impacting operations before execution, especially bulk tracker creation and webhook replay requests.

Risk: Some Ship24 operations are rate-limited, including courier lookup and webhook replay.

Mitigation: Throttle repeated calls and follow the documented one-request-per-second limits for the affected operations.

## Reference(s):

- [Ship24 Documentation](https://docs.ship24.com)
- [Ship24 Skill on ClawHub](https://clawhub.ai/ship24/skills/ship24-tracking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Ship24 API key supplied through SHIP24_API_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
