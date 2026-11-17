## Description:

Detects climbing, playing with fire, touching power sources, and dangerous actions near windows, providing real-time alerts. It is suitable for child safety supervision in scenarios such as homes, kindergartens, and nurseries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Guardians and childcare staff use the skill to review video for possible hazardous child behaviors and receive a structured report. The results support supervision and should be reviewed by a person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads children’s videos, while provider handling, deletion, retention, and account isolation are unverified.

Mitigation: Confirm the provider’s footage handling and deletion practices and account enrollment before use; avoid sensitive or production footage until these are verified.

Risk: The skill may silently provision accounts, and the documented export-only and API destination overrides are ignored.

Mitigation: Do not supply production secrets until identity handling and the actual processing destination have been confirmed with the provider.

Risk: Remote detection accuracy and continuous alerting are unverified.

Mitigation: Keep direct human supervision in place, treat detections as prompts for review, and confirm any alert promptly.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-child-dangerous-behavior-recognition-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON or Markdown report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include detected behavior counts, alert status, suggestions, and report links; findings require human review.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
