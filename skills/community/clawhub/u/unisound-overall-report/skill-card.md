## Description: <br>
Interprets complete physical-exam reports and returns an overall health grade, key findings with severity, prioritized actions, lifestyle recommendations, JSON output, and a plain-language explanation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External health-management teams and physical-exam centers use this skill to turn complete exam-report text into a structured overall interpretation, priority follow-up actions, and recipient-facing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical report contents are sent to a remote model endpoint. <br>
Mitigation: Use only with an approved endpoint and key, and remove names, IDs, phone numbers, and other identifiers before running the skill. <br>
Risk: The security evidence says the code does not perform the de-identification claimed by the skill text. <br>
Mitigation: De-identify reports before invoking the skill; do not rely on the skill code to anonymize patient data. <br>
Risk: The output could be mistaken for a medical diagnosis. <br>
Mitigation: Treat the result as health-management guidance and route abnormal or urgent findings to licensed medical professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-overall-report) <br>
- [Configured model API base](https://maas-api.hivoice.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON followed by a plain-language interpretation; optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a physical-exam report input file and an appkey for the configured remote medical model endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
