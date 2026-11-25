## Description:

Analyzes adult facial images or short videos for visual fatigue-related features and returns a 0–100 fatigue/stress index with directional suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and workplace health teams can use the skill to review visual fatigue indicators from adult face images or short clips. The score is a nonclinical personal state reference, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags unclear consent and handling for facial media, identity data, remote processing, and credential storage.

Mitigation: Use facial media only with the subject’s informed consent, and verify the service’s data, identity, and credential handling before use.

Risk: The security assessment is incomplete because a referenced local path was missing.

Mitigation: Review the missing component and complete a security assessment before relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-adult-facial-fatigue-stress-index-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis results and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a 0–100 score, feature metrics, a fatigue/stress level, directional suggestions, and report links; visual conditions can affect a single score.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
