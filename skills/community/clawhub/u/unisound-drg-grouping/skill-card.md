## Description: <br>
Helps doctors choose the most likely DRG grouping from discharge-document text and candidate DRG options using an internal medical language model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Doctors, clinical coding teams, and evaluation engineers use this skill to submit complete DRG case prompts and receive a single candidate DRG selection for baseline comparison or pre-integration testing. It is an auxiliary grouping aid, not an official reimbursement or hospital grouping decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DRG prompts may contain real patient information that is sent to the configured model provider. <br>
Mitigation: Use the skill only where that data transfer is approved, and de-identify patient data when required. <br>
Risk: The required app key can be exposed through shared logs, command history, or mishandled configuration. <br>
Mitigation: Protect the app key and avoid placing it in shared logs or shell history. <br>
Risk: Changing the API URL can redirect case text to an untrusted endpoint. <br>
Mitigation: Override the API URL only when the endpoint is trusted and approved. <br>
Risk: The model output is an auxiliary grouping suggestion and may be mistaken for an official DRG or reimbursement decision. <br>
Mitigation: Review outputs through the appropriate clinical coding or institutional workflow before use in operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-drg-grouping) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON by default, with optional plain-text answer output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a single DRG answer selected from candidates; batch JSONL runs emit NDJSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
