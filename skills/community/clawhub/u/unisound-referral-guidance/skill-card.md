## Description: <br>
Provides primary-care referral guidance from a patient case summary, including transfer need, urgency, target department and hospital level, pre-transfer measures, required documents, structured JSON, and a natural-language summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Primary-care and community-clinic clinicians use this skill to turn a patient case summary into referral decision support, including urgency, target department, hospital level, pre-transfer actions, and transfer-document checklist. It is a clinical decision-support aid and does not replace professional medical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient case text may be sent to a remote model endpoint without enforced de-identification or explicit consent checks. <br>
Mitigation: Review before clinical installation, remove patient identifiers before input, avoid real PHI unless organizational policy permits it, and use only approved medical-model endpoints. <br>
Risk: The command-line app key is sensitive and may be exposed through local shell history, process listings, or logs. <br>
Mitigation: Handle the app key as a secret, limit access to authorized operators, and avoid recording command invocations that include the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-referral-guidance) <br>
- [Unisound publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Unisound medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [JSON followed by a natural-language summary; command-line output may be printed to stdout or written to a file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a patient case-summary input file and an app key for the configured remote medical model endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
