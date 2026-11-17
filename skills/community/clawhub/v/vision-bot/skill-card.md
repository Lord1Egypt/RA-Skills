## Description:

Analyzes public images through AIProx to describe scenes, identify objects, extract visible text, and count objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use Vision Bot to get descriptions, object counts, and OCR text from a public image URL. The caller should confirm the 50-sat charge before each paid analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The task text and image URL are sent to AIProx, and a page URL may also be sent to microlink.io for a screenshot.

Mitigation: Use only non-sensitive public images and do not send secrets or personal data; review the providers’ privacy terms.

Risk: Each paid analysis costs 50 sats, and the optional spend token is a bearer credential.

Mitigation: Get approval for the stated charge before calling, keep the token out of logs, and use a minimally funded token or per-call L402 payment.

## Reference(s):

- [AIProx documentation](https://aiprox.dev/docs.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Structured JSON containing an image description, detected objects, extracted text, and an optional count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One image-analysis result per request; object counts are included when requested.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
