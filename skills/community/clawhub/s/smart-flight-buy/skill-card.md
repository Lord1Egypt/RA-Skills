## Description:

机票聪明买 helps users compare domestic flight prices across travel platforms, find low-fare dates, and decide whether to buy now or wait.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to compare China domestic flight options, identify cheaper travel dates, and generate purchase-timing guidance. It can also produce a monitor task request for a host agent to handle recurring checks and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search details such as cities and dates are sent to the skill's proxy service for price lookup.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering unnecessary sensitive information.

Risk: The skill provides price lookup and buy-or-wait guidance but does not purchase tickets or guarantee fare availability.

Mitigation: Treat results as decision support and verify final price, route, and terms on the booking platform before purchase.

Risk: Price monitoring depends on the host agent performing scheduled checks and notifications.

Mitigation: Configure the host agent's scheduling and notification workflow before relying on monitor output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/smart-flight-buy)
- [Skill homepage](https://rollinggo.store)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON with flight search results, low-fare calendar entries, purchase-timing advice, or monitor task details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped to 20 flights; calendar scans are capped at 30 days; monitor output is a task request for the host agent.]

## Skill Version(s):

1.0.19 (source: server release metadata; artifact frontmatter: 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
