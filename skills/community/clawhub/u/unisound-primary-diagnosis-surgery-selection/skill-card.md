## Description:

Selects the primary diagnosis and primary surgery for an inpatient encounter from caller-provided candidate lists using a configured medical LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare coding or medical-record operations teams use this skill to choose the principal diagnosis and procedure for insurance coding or discharge-summary workflows from a supplied record summary and candidate lists. Its output is assistive and should be reviewed by qualified personnel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical records and API credentials can be sent to any caller-supplied LLM base URL.

Mitigation: Use only an approved LLM service endpoint and do not allow untrusted users or wrappers to set the base URL.

Risk: Input may contain medical data or identifiers that are not appropriate for the configured LLM service.

Mitigation: Run only in an environment approved for the configured service and de-identify names, IDs, phone numbers, and detailed addresses before use.

Risk: Prepared medical text can be persisted when the save-prepared option is enabled.

Mitigation: Avoid saving prepared text unless the output directory is protected and the retention period is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-primary-diagnosis-surgery-selection)
- [Documented medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON object with main_diagnosis and main_surgery fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The selected diagnosis and surgery are validated against the provided candidate lists; an optional output path can persist the JSON result.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
