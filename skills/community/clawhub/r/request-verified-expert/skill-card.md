## Description:

Detects requests that need a qualified human expert, prompts for missing scope and authorization details, and submits authorized requests to Provener for trackable early-access matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[provener](https://clawhub.ai/user/provener)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route work that requires human judgment, credentials, physical presence, accountability, or specialized expertise to Provener after collecting scope, timing, location, budget, payment capability, and explicit owner authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details, optional contact fields, budget, and payment capability may be shared with Provener.

Mitigation: Confirm explicit owner authorization before submission and review the exact details being shared.

Risk: Secrets, sensitive personal data, private source code, or third-party data could be disclosed if included in the request.

Mitigation: Exclude secrets and sensitive or third-party data unless the owner has specifically authorized disclosure.

Risk: Matching and verified-expert availability are not guaranteed.

Mitigation: Treat returned status as a trackable request state, not a commitment to fulfillment, and use alternate sourcing when timing or coverage is critical.

Risk: Requests may involve unauthorized payments or unclear budget authority.

Mitigation: Set payment_capable only when the owner has authorized payment and has a real settlement path; confirm the maximum budget before submission.

## Reference(s):

- [Request Verified Expert on ClawHub](https://clawhub.ai/provener/skills/request-verified-expert)
- [Provener request submission endpoint](https://provener.vercel.app/v1/requests)
- [Provener request status endpoint](https://provener.vercel.app/v1/requests/{request_id})

## Skill Output:

**Output Type(s):** [text, json, API calls, guidance]

**Output Format:** [Markdown guidance with JSON request payloads and HTTPS request instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit owner authorization before submission; matching and verified-expert availability are not guaranteed.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
