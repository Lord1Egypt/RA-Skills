## Description: <br>
Reviews diagnosis codes against ICD/DRG guideline rules and clinical-record evidence, returning pass, fail, or manual-review outcomes for provided diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical coding, claims, and hospital operations teams can use this skill to check whether candidate diagnosis codes are supported by structured case records and guideline rules. It is an audit aid and does not provide medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive clinical record content may be sent to external LLM and guideline-service endpoints. <br>
Mitigation: Use only approved or allowlisted endpoints, require consent and redaction controls before off-system processing, and confirm organizational policy permits the data flow. <br>
Risk: The skill requires sensitive credentials such as the model appkey and optional guideline API key. <br>
Mitigation: Manage credentials through approved secret-handling workflows, avoid exposing secrets in shell history or logs, and restrict access to the minimum required users and environments. <br>
Risk: Prepared-text debug exports can create plaintext copies of clinical records. <br>
Mitigation: Do not use plaintext prepared exports with real patient data unless the content is redacted and stored under approved retention and access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-diagnosis-review) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [External medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON object with final_decision and reasoning fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [final_decision is one of "通过", "不通过", or "待人工复核"; reasoning is concise and user-facing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
