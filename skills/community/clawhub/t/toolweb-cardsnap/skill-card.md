## Description:

Digital Business Card Generator that creates, manages, and tracks shareable business cards with analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and business users use CardSnap to create, update, retrieve, delete, and analyze digital business cards through a documented API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Card data can contain personal contact and profile details, while the documented API does not declare authentication, ownership checks, or privacy controls.

Mitigation: Review before use with real card data and verify that the live service enforces authentication, ownership checks, consent and privacy handling, and rate limits.

Risk: Update and permanent deletion endpoints can modify or remove card records.

Mitigation: Verify authorization, ownership enforcement, confirmation steps, and a safe recovery path before enabling update or delete workflows.

Risk: Analytics access may expose engagement data for a card.

Mitigation: Confirm analytics endpoints restrict access to authorized users before using or sharing engagement reports.

## Reference(s):

- [CardSnap Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-cardsnap)
- [Kong Route](https://api.toolweb.in/tools/cardsnap)
- [API Docs](https://api.toolweb.in:8185/docs)
- [ToolWeb](https://toolweb.in)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)
- [RapidAPI Publisher Profile](https://rapidapi.com/user/mkrishna477)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON]

**Output Format:** [Markdown with HTTP endpoint descriptions and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include card profile data, analytics events, and endpoint-specific JSON payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
