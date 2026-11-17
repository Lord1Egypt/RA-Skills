## Description:

Combines frontal facial image capture with multimodal physiological feature analysis to provide early risk screening and alerts for chronic and acute conditions such as heart attack, stroke, hypertension, and hyperlipidemia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users and care providers use this skill to submit a frontal face image, video, or media URL for non-contact early health risk screening and to retrieve prior cloud-stored screening reports. Results are screening guidance and are not a substitute for professional medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends facial images or videos and health-related screening data to a remote service.

Mitigation: Do not use real biometric or health data unless the publisher documents consent, retention, remote processing, and account handling.

Risk: The package silently creates or reuses an identity, stores tokens locally, and can query cloud-stored report history.

Mitigation: Require clear user confirmation for analysis and history access, secure local credentials, and provide a documented way to rotate or delete stored tokens.

Risk: The security evidence reports insecure defaults and development HTTP endpoints.

Mitigation: Use HTTPS-only production endpoints and review configuration before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-contactless-health-risk-detection-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API interface documentation](references/api_doc.md)
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON text with structured screening results, risk notes, recommendations, history lists, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [History queries return cloud-stored reports; analysis may include report export links.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact frontmatter says 1.0.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
