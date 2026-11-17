## Description:

Analyzes a frontal-face photo with RageHealth's skin-pro service and returns skin scores, skin characteristics, concern severity and counts, and result imagery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoguaishou-sc](https://clawhub.ai/user/xiaoguaishou-sc)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request an informational analysis of a frontal-face photo, including visible skin characteristics and concerns. Results are not a substitute for medical evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facial photos and authentication headers may be sent outside the advertised service if the upload destination or redirects are not constrained.

Mitigation: Restrict uploads to the advertised HTTPS gateway and disable or validate redirects before using real credentials or photos.

Risk: Facial images and optional face-ID processing involve sensitive personal data.

Mitigation: Upload only photos the user has authorized for analysis, enable face-ID detection only with explicit authorization, and protect saved reports.

Risk: Unreviewed dependency versions can increase exposure when handling images and credentials.

Mitigation: Install reviewed dependency versions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xiaoguaishou-sc/skills/skin-analysis)
- [RageHealth skin-pro API gateway](https://gateway.ragehealth.cn/openapi-prod)
- [Response schema](references/response_schema.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured skin-analysis response with a human-readable summary and optional result imagery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are informational and should not be treated as medical diagnosis.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
