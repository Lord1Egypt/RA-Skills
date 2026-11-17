## Description:

Automatically detects personnel in target areas based on computer vision, supports real-time video stream detection, and is suitable for monitoring personnel access in parks, offices, and restricted areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run cloud-backed human detection on uploaded or URL-based surveillance media, produce structured reports, and retrieve historical detection reports for monitored areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Surveillance media and report history are processed by a third-party cloud service.

Mitigation: Use only with clear disclosure, appropriate consent, and an approved data retention policy for uploaded media and generated reports.

Risk: The release includes identity, token, history, and development-network behavior that requires review before installation.

Mitigation: Require production HTTPS endpoints, approved account association behavior, and safer token storage before deploying in sensitive workplace or restricted-area monitoring contexts.

## Reference(s):

- [API Documentation](references/api_doc.md)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-human-detection-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report text or JSON structured analysis, with optional saved output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include person counts, appearance frequency, intrusion indicators, region-level details, warning messages, historical report listings, and report links.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
