## Description:

Analyzes crib-camera images or video to identify infant sleep posture, mouth/nose occlusion, risk level, alerts, structured results, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to analyze infant crib-monitor footage for visual sleep-posture and mouth/nose-occlusion signals, then return risk levels and report links. It is an auxiliary monitoring aid and should not be treated as a medical diagnosis or a replacement for adult supervision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive infant video, report history, internal identifiers, and account tokens may be sent to and stored by the backend service.

Mitigation: Use only after confirming trust in the publisher and backend service, obtaining appropriate guardian consent, and understanding how uploaded footage and report history are handled.

Risk: Plaintext HTTP configuration and local plaintext token storage may expose credentials or child-monitoring data.

Mitigation: Require HTTPS-only production endpoints and protected token storage before using the skill with real child-monitoring footage.

Risk: Risk-level outputs are visual monitoring signals and may be mistaken for medical or emergency guidance.

Mitigation: Present results as auxiliary monitoring information only, keep adult supervision in place, and review urgent alerts directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-suffocation-risk-detection-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](artifact/references/api_doc.md)
- [Analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Markdown text with structured JSON-style analysis results, risk levels, alert text, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save the textual result to a caller-provided output file.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
