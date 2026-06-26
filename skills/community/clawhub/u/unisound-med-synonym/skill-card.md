## Description: <br>
Matches medical terms to equivalent or closest standard terminology from caller-supplied questions using an external medical language model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and healthcare workflow integrators use this skill to submit medical terminology synonym-matching prompts and receive structured model responses for downstream review. Outputs are assistive model-generated information, not formal clinical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical questions may contain identifiable patient information that would be sent to an external model API. <br>
Mitigation: De-identify patient data and follow institutional review and workflow requirements before submitting questions. <br>
Risk: A configurable API endpoint or reused API key can expose prompts or credentials if directed to an untrusted service. <br>
Mitigation: Use a dedicated API key with a trusted provider and do not override --api-url to an untrusted destination. <br>
Risk: Model output could be mistaken for a formal clinical decision. <br>
Mitigation: Treat responses as assistive terminology-matching information and require qualified review before clinical use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-synonym) <br>
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, files, guidance] <br>
**Output Format:** [JSON by default, with optional plain text answer output or NDJSON/file output for batch runs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts direct question text, JSON/JSONL records, or stdin; dry-run emits parsed question JSON without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
