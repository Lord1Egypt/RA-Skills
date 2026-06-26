## Description: <br>
病历实体抽取与结构化。由调用方提供题目文本或含 `question` 字段的结构化输入，经内部医疗大模型按题干约束生成作答；仅含 `scripts/run.py`，可独立拷贝部署。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical informatics teams and developers use this skill to pass medical-record prompts or structured question records to a remote medical LLM and receive entity-extraction answers in JSON or text form. Outputs are model-assisted information and should not be treated as formal clinical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical-record prompts may contain sensitive patient data and are sent to a remote model endpoint. <br>
Mitigation: De-identify or otherwise authorize medical records before processing and follow applicable organizational data-handling procedures. <br>
Risk: The skill requires an app key and allows the API URL to be overridden. <br>
Mitigation: Use a scoped app key and keep --api-url set to an approved destination. <br>
Risk: Saved outputs may contain sensitive prompt content, metadata, or model answers. <br>
Mitigation: Write outputs only to approved locations with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-sm-doc) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Remote medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [JSON object for a single item, NDJSON for batch mode, or plain answer text when --text-only is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a remote hivoice.cn medical model API unless --dry-run is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
