## Description:

Combines livestock behavior in continuous barn videos with environmental sensor data (temperature, humidity, ammonia, etc.) to identify group stress responses caused by abnormal in-barn conditions. | 结合畜禽行为与环境传感器，识别温湿度异常时的群体应激反应。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock environment managers use the skill to correlate barn video with environmental sensor readings and identify possible group stress responses during abnormal conditions. The reports support monitoring and inspection; the skill documentation says they are for reference and do not provide equipment or environmental control instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious for account and credential handling, broad or unintended actions, and a mismatch with its stated livestock analysis purpose.

Mitigation: Review the skill and its permissions before use; avoid providing API secrets or private video and sensor data until it has been vetted.

Risk: The available security evidence is incomplete because Skillspector reports an unresolved local path-like reference.

Mitigation: Resolve the referenced path and complete the security review before relying on the scan results.

## Reference(s):

- [API reference](artifact/references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-environmental-anomaly-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis results and reports, with Markdown tables for historical report lists and report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis findings and stress levels are advisory and based on supplied media and sensor data.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
