## Description:

AI-powered pet vomiting and regurgitation detection from indoor fixed-camera video, identifying characteristic actions and vomitus on the floor while recording event times, frequency, and vomitus characteristics for early digestive issue discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, caregivers, and animal hospital staff can use the skill to review indoor camera video for possible vomiting or regurgitation events and receive a structured behavior report. Results are visual observations, not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags account and credential handling concerns.

Mitigation: Verify the publisher and account handling, and review credential use before connecting an account or providing credentials.

Risk: Video analysis involves remote-service and video-upload behavior that may expose private household footage.

Mitigation: Review the remote service and its video-upload behavior; submit only footage appropriate to share with that service.

Risk: The security evidence raises concerns about configuration-only execution control.

Mitigation: Review the available configuration and execution controls before use, and supervise initial runs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-vomiting-regurgitation-detection-analysis)
- [API reference](artifact/references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured behavior report with event observations, timestamps, frequency, vomitus characteristics, and report links; JSON or Markdown presentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual behavior observations only; not a veterinary diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
