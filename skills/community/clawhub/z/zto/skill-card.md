## Description:

Use ZTO Express for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check ZTO shipment status, estimate shipping fees or delivery timing, compare services, find outlets, and troubleshoot delayed or problematic deliveries. The skill also guides users through local privacy controls when runtime features store shipment history or related records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local runtime features may store shipment history, subscription records, and possibly saved address records on the user's machine.

Mitigation: Disclose the local storage paths when privacy is relevant and use the privacy clear or export controls for shared devices or users who do not want retained data.

Risk: Shipping fees, delivery timing, and outlet availability can be inaccurate when live ZTO tools or exact pricing data are unavailable.

Mitigation: State assumptions, provide cautious ranges, and avoid claiming that real shipping actions were completed unless live tools are available and confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/zto)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance with shipment status summaries, estimates, assumptions, and next-step recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cautious estimates when exact pricing or timing cannot be confirmed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
