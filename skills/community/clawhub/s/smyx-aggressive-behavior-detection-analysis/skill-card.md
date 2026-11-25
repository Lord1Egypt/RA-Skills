## Description:

Detects aggressive interactions in livestock and poultry from continuous barn videos — including fighting, biting, chasing and butting — and outputs behavior type, intensity level and alert level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock and poultry farm operators use the skill to screen barn images and videos for fighting, biting, chasing, and related aggressive behavior, then review event severity, alert levels, and historical reports. Results support visual monitoring and do not provide intervention advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Barn footage and identity or token data may be sent to a service or stored or transmitted, raising privacy and account-management concerns.

Mitigation: Review the service's data handling and account controls before sending footage or connecting an account; upload only footage you are authorized to share.

Risk: The security scan was partial because a referenced local path was missing, so it does not provide complete evidence about the artifact.

Mitigation: Review the complete artifact and its referenced paths before installation; treat the partial scan as incomplete.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-aggressive-behavior-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [Structured JSON analysis results; Markdown tables for historical report lists; optional saved result file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior type, event times, involved animal locations, intensity and alert levels, and report links.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata; SKILL.md frontmatter states 1.0.20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
