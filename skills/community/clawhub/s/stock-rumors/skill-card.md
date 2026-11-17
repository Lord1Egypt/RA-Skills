## Description:

Stock Rumors scans for early market signals including M&A rumors, insider activity, analyst changes, social whispers, and regulatory activity via the AIsa API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request early market-signal scans and receive ranked rumor, insider, analyst, social, and regulatory summaries for informational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_API_KEY is required and authenticated requests may be sent to a configured AIsa endpoint.

Mitigation: Keep the API key scoped and revocable, and set AISA_BASE_URL only for trusted endpoints.

Risk: Market rumors and early signals are unconfirmed and may be incomplete, stale, or misleading.

Mitigation: Treat outputs as informational analysis, verify signals against primary sources, and do not use the report as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/stock-rumors)
- [AIsa homepage](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown report by default, with optional JSON summary when --output json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; optional AISA_BASE_URL and AISA_MODEL change the endpoint and model used.]

## Skill Version(s):

1.0.1 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
