## Description:

Monitors value drift, boundary violations, low-energy alerts, and user-pattern signals, then produces guard reports or progressive interventions through a CLI or proactive-engine signal mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to monitor stated values, interaction boundaries, energy signals, and value drift, and to receive CLI reports, signal handling, or progressive intervention guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists sensitive behavioral, boundary, value, intervention, and signal records locally.

Mitigation: Review or disable persistence before use, avoid sensitive health, financial, relationship, identity, or work-profile data unless storage is intentional, and inspect or delete local records regularly.

Risk: The skill supports silent monitoring and progressive interventions without clear user-facing consent, retention, or deletion controls.

Mitigation: Require explicit user consent before monitoring or intervention, keep intervention thresholds conservative, and manually verify retention and deletion behavior before deployment.

## Reference(s):

- [Boundary Detection Rules](references/boundary-detection-rules.md)
- [Intervention Levels](references/intervention-levels.md)
- [Value Drift Formula](references/value-drift-formula.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with inline shell commands and JSON-like status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and write local guard state, value, intervention, and signal files under the OpenClaw workspace.]

## Skill Version(s):

0.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
