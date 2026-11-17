## Description:

检后随访管理。根据体检报告，生成结构化随访计划（时间节点/随访内容/健康指导），支撑体检闭环服务（JSON + 面向受检者的随访通知）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Health exam centers and health management organizations use this skill to turn a patient's exam report into a structured follow-up schedule, coaching points, alert conditions, and a recipient-facing follow-up notice. The generated plan supports post-exam tracking and should be reviewed within appropriate clinical and privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full health reports to a remote model provider.

Mitigation: Use only de-identified reports unless explicit authorization and privacy controls are in place.

Risk: A custom model base URL could route reports and API credentials to an untrusted service.

Mitigation: Use trusted HTTPS endpoints only and provide a dedicated, scoped appkey.

Risk: Generated follow-up guidance may be incomplete or clinically inappropriate for a specific patient.

Mitigation: Require review by qualified staff before using the plan for patient communication or care coordination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-followup-mgmt)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON followed by a plain-text follow-up notice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write the generated follow-up plan to a caller-specified output file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
