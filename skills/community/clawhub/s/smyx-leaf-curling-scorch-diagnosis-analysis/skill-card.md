## Description:

Analyzes plant leaf images or video to identify curling direction and margin scorch patterns, optionally combining soil moisture data to rank likely causes such as drought stress, disease, pesticide damage, fertilizer burn, or cold stress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Farmers, agronomy advisors, and agricultural IoT operators use this skill to analyze plant leaf media for curling and margin scorch symptoms, then receive a structured diagnosis with likely causes and directional remediation guidance. It can also query cloud-hosted historical diagnosis reports associated with the internally resolved user identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant images, videos, URLs, and report history are sent to a remote cloud service and associated with an internally resolved identity.

Mitigation: Review the publisher and service endpoint before installation, obtain clear user consent for cloud analysis and history lookup, and confirm data retention and deletion expectations.

Risk: The authoritative security summary flags silent identity and token management with insecure token storage or transport.

Mitigation: Prefer a release that defaults to HTTPS production endpoints, avoids plaintext token storage, and documents token handling; rotate credentials if exposure is suspected.

Risk: Visual plant-stress diagnosis can be uncertain because drought, disease, pesticide damage, fertilizer burn, and cold stress may share symptoms.

Mitigation: Treat results as advisory, use clear images and optional soil-moisture context, and confirm severe or ambiguous cases through field inspection or professional plant-health consultation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-leaf-curling-scorch-diagnosis-analysis)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [API Interface Documentation](references/api_doc.md)
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown text with structured JSON-style diagnosis details, ranked likely causes, recommendations, and report links; optional saved file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud report history tables and report export links when history lookup is requested.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter states 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
