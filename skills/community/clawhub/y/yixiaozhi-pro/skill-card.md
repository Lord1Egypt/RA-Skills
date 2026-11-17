## Description:

医小智Pro诊断助手 collects medical history details, asks targeted follow-up questions, and generates structured diagnostic reports with medication guidance and high-risk warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantian888](https://clawhub.ai/user/lantian888)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to collect symptom context and produce initial medical guidance in a structured diagnostic report. Because the skill handles health information and medication advice, outputs should be treated as informational support rather than a substitute for professional medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect detailed health information and prior chat history.

Mitigation: Use only with clear consent, collect the minimum needed information, and avoid entering unnecessary identifiers.

Risk: The skill sends conversations to a configurable external model service.

Mitigation: Review and trust the endpoint configuration before deployment, and do not use untrusted token or model service settings.

Risk: The skill provides diagnosis and medication guidance.

Mitigation: Present outputs as informational support and require professional review for serious symptoms, vulnerable users, or medication decisions.

Risk: The skill can append a cancer-related referral or screening link to diagnostic reports.

Mitigation: Review the destination and disclose the referral or booking purpose before using the skill in a user-facing setting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lantian888/skills/yixiaozhi-pro)
- [Cancer screening appointment link](https://bmsapp.geneplus.org.cn/business/addOrder)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic intake questions and structured diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include high-risk medical warnings, medication guidance, and a cancer screening link when cancer-related terms are present.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
