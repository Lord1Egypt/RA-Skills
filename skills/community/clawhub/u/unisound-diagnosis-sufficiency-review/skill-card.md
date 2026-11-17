## Description:

诊断依据充分性审核。输入结构化病案 record 与待审核诊断列表，输出诊断依据充分性审核结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare operations teams use this skill to review whether structured medical-record evidence sufficiently supports listed primary and other diagnoses for ICD/DRG audit workflows. It returns concise auxiliary review results and is not medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical-record excerpts may be sent to guideline and model services.

Mitigation: Use only de-identified inputs, restrict outbound network access to approved endpoints, and prefer offline review with --no-llm when external transmission is not appropriate.

Risk: Bearer credentials may be sent to configurable network endpoints.

Mitigation: Provide credentials through managed secret handling and avoid arbitrary --base values unless the endpoint is approved.

Risk: Record-derived data can be written to disk when prepared-text or output-file options are used.

Mitigation: Avoid --save-prepared and output-file options unless the destination is access-controlled and retention is managed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-diagnosis-sufficiency-review)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Internal medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with final_decision and reasoning fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [final_decision is one of 依据充分, 依据不充分, or 待人工复核; reasoning is concise and does not expose chain-of-thought.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
