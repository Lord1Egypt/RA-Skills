## Description:

Queries SPX Express and supported CAINIAO Malaysia tracking numbers and returns shipment status, timeline, delivery estimates, location route, and delay analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiziscool](https://clawhub.ai/user/wiziscool)

### License/Terms of Use:

MIT-0

## Use Case:

External users, support agents, and delivery operations teams use this skill to check SPX Express or CAINIAO Malaysia package status from a tracking number and summarize delivery progress, estimated delivery, route, and delays.

### Deployment Geography for Use:

Global for users tracking SPX Express Malaysia shipments.

## Known Risks and Mitigations:

Risk: The optional cookie argument can expose browser session data when passed on the command line.

Mitigation: Avoid using --cookie unless required; if authentication is needed, prefer a credential store, protected file, or stdin-based secret handling and never log or echo the cookie.

Risk: Tracking results may include recipient names, full addresses, GPS coordinates, and detailed shipment timelines.

Mitigation: Return only the fields needed for the user's request, avoid raw API dumps, and treat output as sensitive delivery information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wiziscool/skills/spx-tracking)
- [Publisher profile](https://clawhub.ai/user/wiziscool)
- [SPX Express website](https://spx.com.my/)
- [SPX tracking API endpoint](https://spx.com.my/shipment/order/open/order/get_order_info)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON, human-readable text, or one-line summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shipment status, timestamps, estimated delivery windows, recipient names, addresses, GPS coordinates, and delay analysis.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
