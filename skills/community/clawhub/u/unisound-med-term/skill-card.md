## Description: <br>
Provides concise medical-term definitions and clinical context from a question supplied directly, through stdin, or from JSON, JSONL, or text input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical content teams can use this skill to send medical terminology questions to a configured medical LLM and receive concise explanatory answers with metadata. It is intended as model-assisted information and not as a formal diagnosis or treatment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided medical questions are sent to a configured hivoice.cn-compatible model endpoint and may contain sensitive health information. <br>
Mitigation: Use a dedicated app key, keep the API URL pointed at a trusted endpoint, and submit only de-identified or organization-approved medical text. <br>
Risk: Model-generated medical explanations may be incomplete or unsuitable for clinical decision-making. <br>
Mitigation: Treat outputs as assistive information and review them under the applicable clinical, compliance, and quality process before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-term) <br>
- [Default hivoice.cn-compatible chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [JSON object or NDJSON, with optional plain text answer output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write UTF-8 JSON or NDJSON to an output path; dry-run returns parsed input metadata without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
