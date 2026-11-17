## Description:

Track Qantas Freight shipments by air waybill number and get origin, destination, shipper, consignee, pieces, weight, ETD, and latest shipment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sicl](https://clawhub.ai/user/sicl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to format Qantas Freight air waybill tracking results, including shipment summary fields, shipment history events, and multiple-AWB output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Air waybill tracking can display shipment details such as route, status, shipper, and consignee.

Mitigation: Use the skill only where users are permitted to retrieve and view those shipment details.

Risk: Tracking responses can be empty or lack a latest event.

Mitigation: Return "AWB not found" for empty responses and fall back to the last shipment history item when no latest event is available.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and expandable detail blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles up to 10 air waybill numbers and formats shipment summaries, chronological events, and not-found cases.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
