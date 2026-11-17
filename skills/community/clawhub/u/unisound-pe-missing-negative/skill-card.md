## Description:

门诊病历内涵质控：体格检查缺少与诊断相关的体征。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality-control teams and healthcare workflow developers use this skill to check whether outpatient medical records include physical-exam findings relevant to the diagnosis. It produces a clinician-review-required defect status and reason for a specific physical-exam completeness rule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive clinical record text and sends it to an LLM endpoint.

Mitigation: Use only de-identified records and run the skill only with an approved HTTPS LLM service.

Risk: The LLM base URL is externally configurable.

Mitigation: Pin the base URL to an approved service before deployment and review configuration changes.

Risk: The app key is required for API access.

Mitigation: Provide the app key through a protected runtime secret path and do not commit it to the skill or logs.

Risk: The multi-format entry point can save prepared plaintext input when requested.

Mitigation: Avoid --save-prepared in clinical workflows unless retaining a plaintext copy is intentional and governed.

Risk: Outputs are medical quality-control assistance rather than authoritative clinical conclusions.

Mitigation: Require clinician review before using the result in a real clinical workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-pe-missing-negative)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Analysis, Files]

**Output Format:** [UTF-8 text status with an optional reason line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns either 无缺陷 or 有缺陷 followed by a reason; the CLI also writes the result to an output text file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
