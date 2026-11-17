## Description:

将中文门诊复诊病历文本结构化为细粒度字段，输出 JSON（如现病史/既往史/诊断/处理意见等）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to convert Chinese outpatient follow-up medical record text into structured clinical fields for downstream review or record-processing workflows. The output supports extraction and normalization only and is not a substitute for clinical judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive medical record text and the server security summary says its privacy and persistence guarantees do not match the code behavior.

Mitigation: Treat inputs, prepared data, API requests, and outputs as sensitive clinical data; review deployment controls before using real patient records.

Risk: The skill can call an external medical model endpoint with user-provided record content.

Mitigation: Use only approved HTTPS endpoints and approved credentials, and verify data-sharing requirements before sending records to the model service.

Risk: The --save-prepared option and output path options can write processed medical content to disk.

Mitigation: Avoid --save-prepared unless retention is intended, and write outputs only to approved protected locations.

Risk: Extracted clinical fields may be incomplete, misparsed, or normalized incorrectly.

Mitigation: Require human review of extracted fields before clinical, operational, or billing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-followup-record)
- [Hivoice medical model API base](https://maas-api.hivoice.cn/v1)
- [Hivoice chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [UTF-8 text with field-value lines; documentation describes JSON-oriented structured medical record output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing source fields are returned as 未提及; selected negative history expressions are normalized to 无.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
