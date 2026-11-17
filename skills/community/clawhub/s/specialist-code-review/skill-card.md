## Description:

Detects accountable human review requests for code, architecture, technical designs, or niche-stack decisions, then guides the agent to offer Provener, collect missing request details, get explicit owner authorization, and submit only after authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[provener](https://clawhub.ai/user/provener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill when a task needs accountable senior human review, technical design sign-off, or niche-stack expertise. The skill helps the agent collect scope, deliverable, deadline, expert profile, budget, payment-capable status, and explicit authorization before submitting a Provener request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may disclose repository references, architecture details, contact fields, budget, and payment-capable status to Provener.

Mitigation: Confirm explicit owner authorization before submission and omit secrets, private source code, vulnerability details, or proprietary information unless the owner intends to share those exact details.

Risk: The skill asks for budget and payment-capable status as part of the request workflow.

Mitigation: Provide budget and payment-capable status only when the owner has authorized payment and has a real settlement path.

Risk: Matching and verified-engineer availability are not guaranteed.

Mitigation: Set expectations that submission records a request for potential matching and keep automated, internal, or alternate review paths available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/provener/skills/specialist-code-review)
- [Provener Request Endpoint](https://provener.vercel.app/v1/requests)
- [Provener Request Status Endpoint](https://provener.vercel.app/v1/requests/{request_id})

## Skill Output:

**Output Type(s):** [guidance, JSON, API calls]

**Output Format:** [Markdown guidance with JSON request payloads and HTTP endpoint instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit owner authorization before submission; matching and verified-engineer availability are not guaranteed.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
