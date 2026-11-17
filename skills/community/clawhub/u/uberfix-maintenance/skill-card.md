## Description:

Create and follow maintenance requests in UberFix using authorized tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alazabdev](https://clawhub.ai/user/alazabdev)

### License/Terms of Use:

MIT-0

## Use Case:

UberFix users can create, check, and update maintenance requests, cancel requests, and request quotations through an authorized connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An overbroad connector key could expose requests outside the intended company.

Mitigation: Use a connector key restricted to the intended company; do not treat a customer phone number as proof of ownership.

Risk: Quotation requests and cancellations create real business-side effects.

Mitigation: Obtain the user's explicit approval before requesting a quotation or canceling a request.

## Reference(s):

- [UberFix Maintenance on ClawHub](https://clawhub.ai/alazabdev/skills/uberfix-maintenance)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports results from authorized UberFix tools; requires a separately configured connector.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
