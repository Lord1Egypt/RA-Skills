## Description:

根据住院病历生成标准出院记录。输入入院记录、病程记录等，调用内部医疗大模型，输出结构化出院记录（含主诉、入院情况、入院诊断、诊疗经过、出院诊断、出院情况、出院医嘱七个字段）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical documentation teams and healthcare developers can use this skill to convert de-identified inpatient records into a structured discharge record draft. The generated record covers chief complaint, admission status, admission diagnosis, treatment course, discharge diagnosis, discharge status, and discharge instructions for clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical records and an API key are sent to a configurable remote model endpoint.

Mitigation: Use only a trusted deployment environment, restrict the endpoint to the intended internal HTTPS service, and de-identify records before invoking the skill.

Risk: Prepared medical text can be persisted when debug saving is enabled.

Mitigation: Do not use --save-prepared with real patient data; if debugging is required, use synthetic or fully de-identified records and remove generated files after review.

Risk: Generated discharge records may contain omissions or clinical inaccuracies.

Mitigation: Treat every output as a draft and require review by a licensed clinician before it is used for care, billing, transfer, or archival workflows.

Risk: Arbitrary prompt files can change the medical generation instructions.

Mitigation: Accept prompt or input files only from trusted sources and review custom prompts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-discharge-record)
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm)
- [Configured internal medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, API calls, shell commands, guidance]

**Output Format:** [UTF-8 discharge-record text with optional JSON or text file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts that should be reviewed by a licensed clinician before use in medical workflows.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
