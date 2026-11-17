## Description:

门诊病历内涵质控：主诉不应使用疾病和操作。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality-control teams and developers use this skill to check whether an outpatient record's chief complaint improperly uses a disease name or procedure instead of a symptom. The skill parses record fields, queries a configured medical LLM, and returns a concise pass/fail result with a reason when a defect is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical record text and a bearer key are sent to a configured LLM endpoint.

Mitigation: Use only de-identified records in an approved environment, keep the base URL fixed to the trusted HiVoice HTTPS endpoint, and protect the app key.

Risk: The quality-control result may be incomplete or incorrect for clinical use.

Mitigation: Require review by a qualified clinician before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-chief-complaint-disease-op)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [UTF-8 text result and optional command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs either 无缺陷 or 有缺陷 followed by a reason; default file output is under ../runs/med-emr-qc/.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
