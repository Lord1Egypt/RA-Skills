## Description:

体检报告整体解读。输入完整体检报告文本，输出整体健康评级、主要发现（含严重程度）、优先行动清单和个性化生活方式建议（JSON + 通俗易懂的整体解读）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External health management teams and exam centers use this skill to turn complete health examination report text into an overall health rating, prioritized findings, follow-up actions, lifestyle guidance, and a plain-language explanation for the examined person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical report text may be sent to a remote model despite the skill documentation claiming de-identification before model calls.

Mitigation: Use only redacted or minimized reports until the implementation is fixed and reviewed for effective de-identification.

Risk: The API base URL can be overridden, which could route sensitive report content to an untrusted endpoint.

Mitigation: Do not override --base unless the endpoint is explicitly trusted and approved for the data being processed.

Risk: Health report interpretations can be incomplete or incorrect and are not a medical diagnosis.

Mitigation: Present the output as health-management support and require review by a qualified clinician for abnormal findings or medical decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-overall-report)
- [ClawHub publisher profile](https://clawhub.ai/user/unisound-llm)
- [Hivoice MAAS API base URL](https://maas-api.hivoice.cn/v1)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON followed by a plain-language Markdown-style narrative section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs an overall grade, summary, key findings, normal systems, priority actions, lifestyle advice, next-exam suggestion, and an explanatory narrative.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
