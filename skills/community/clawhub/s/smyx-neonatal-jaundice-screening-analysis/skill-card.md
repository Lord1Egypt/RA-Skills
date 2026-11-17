## Description:

Analyzes newborn facial images or short videos to provide a visual jaundice risk screening hint and suggested next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and neonatal care staff use the skill to request preliminary visual screening of a newborn's facial image and to review screening reports. The results are screening guidance and should be confirmed through appropriate clinical testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account and credential handling are unclear.

Mitigation: Clarify how identities and credentials are created, stored, transmitted, and protected before use.

Risk: Newborn facial images may be processed remotely without clear consent.

Mitigation: Confirm remote processing and data retention terms, and obtain guardian consent before submitting images.

Risk: Expected behavior may depend on the deployment environment.

Mitigation: Confirm the required environment settings and expected behavior in the target deployment before enabling the skill.

Risk: The security scan was partial because a referenced local path was missing.

Mitigation: Resolve the missing reference and review it before relying on the skill.

## Reference(s):

- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-neonatal-jaundice-screening-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured screening reports and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a visual risk level, confidence, observations, report links, and suggested next steps; not a clinical diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
