## Description:

Audit Shopify tracking integrity across UTM, pixel, CAPI, and checkout events to detect attribution leaks.

This skill is for research and development only.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Performance marketers, ecommerce operators, and analytics teams use this skill to review Shopify event samples, pixel or CAPI configuration notes, UTM examples, and checkout flow maps for attribution leaks and tracking gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event samples and configuration notes can include sensitive customer, order, advertising, or tracking data.

Mitigation: Provide sanitized samples and omit credentials, customer identifiers, raw order data, and other unnecessary sensitive fields.

Risk: Incomplete event logs or checkout flow information can lead to unsupported conclusions about attribution leaks.

Mitigation: Tie findings to concrete event evidence and mark assumptions when full logs are unavailable.

Risk: The artifact states non-commercial license terms that may affect business use.

Mitigation: Review the license terms and obtain separate commercial permission before business deployment when required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/shopify-tracking-auditor)
- [Output template](references/output-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown audit report with prioritized actions, evidence table, and 7-day execution plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should be tied to concrete event evidence and assumptions should be marked when full logs are unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
