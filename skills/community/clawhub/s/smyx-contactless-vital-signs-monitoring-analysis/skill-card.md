## Description:

Non-contact detection of heart rate, respiration, blood oxygen, and heart rate variability. No wearable devices are required; monitoring is achieved solely through camera footage. | 无感生命体征监测分析技能，非接触检测心率、呼吸、血氧、心率变异性，无需穿戴设备，通过摄像头画面即可监测

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Users can submit camera footage for estimates of heart rate, respiration, blood oxygen, and heart rate variability, then review structured results or query past reports. The skill says its results are for health reference and do not replace medical measurement or diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing behavior that does not match the stated camera-based health-monitoring purpose and risks involving sensitive data, credentials, and user accounts. The scan was partial, so it does not establish that all behavior is understood.

Mitigation: Avoid installation until the publisher explains account and credential handling, external video processing and consent, and how the implementation supports its stated monitoring purpose.

## Reference(s):

- [API interface notes](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-contactless-vital-signs-monitoring-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured health analysis report and Markdown report list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vital-sign estimates, risk notes, suggestions, and report links. Historical report lists are presented as Markdown.]

## Skill Version(s):

1.0.23 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
