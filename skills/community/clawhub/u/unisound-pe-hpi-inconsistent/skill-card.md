## Description:

门诊病历内涵质控：体格检查结果与现病史不符。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality reviewers and healthcare developers use this skill to check outpatient EMR text for mismatches between physical examination findings and the history of present illness. It returns a concise no-defect or defect-with-reason result for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive outpatient medical record text.

Mitigation: Use only in an environment approved for medical data and de-identify records before submitting them to any model endpoint.

Risk: API credentials may be exposed when passed directly on the command line.

Mitigation: Avoid passing real keys on the command line where possible and follow the platform's approved secret-handling process.

Risk: Custom model endpoints can send medical text to unapproved services.

Mitigation: Use the default HiVoice MaaS endpoint or only explicitly approved HTTPS endpoints for the --base parameter.

Risk: Generated results and optional prepared files may contain patient data.

Mitigation: Treat output files as sensitive medical data and apply the same access, retention, and deletion controls used for the source records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-pe-hpi-inconsistent)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [HiVoice MaaS OpenAI-compatible chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [UTF-8 plain text result with optional shell command examples in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs either 无缺陷 or 有缺陷 followed by a reason.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
