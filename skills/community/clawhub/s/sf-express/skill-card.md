## Description:

Use SF Express (顺丰速运) for shipment tracking, delivery anomaly triage, e-commerce seller/customer handoffs, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, support agents, merchants, and operations staff use this skill to understand SF Express shipments, compare service options, estimate delivery time or fees, and triage delivery anomalies. Developers may also use the bundled CLI for live endpoint-backed tracking, explicit mock demos, history, subscriptions, and privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipment identifiers and tracking details may be sent to the user-configured tracking endpoint.

Mitigation: Use only trusted HTTPS endpoints and confirm the endpoint destination before running live tracking.

Risk: Tracking history and subscription data may be retained locally in plaintext SQLite storage.

Mitigation: Use the skill on trusted machines, avoid unnecessary persistence, and run the privacy clear workflow when history is no longer needed.

Risk: Demo tracking data could be mistaken for live carrier information.

Mitigation: Require explicit mock mode for demos and preserve the non-real data label in user-facing responses.

Risk: Pinned dependencies may become stale before use with sensitive shipments.

Mitigation: Review and update pinned dependencies before deployment in higher-sensitivity environments.

## Reference(s):

- [ClawHub Sf Express skill page](https://clawhub.ai/harrylabsj/skills/sf-express)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text with tracking summaries, anomaly triage, estimates, service comparisons, and privacy-control guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live tracking depends on a user-configured HTTPS endpoint; mock results are explicitly labeled as demonstration data.]

## Skill Version(s):

1.1.2 (source: frontmatter, artifact version file, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
