## Description:

Assists public health workers with chronic disease screening by evaluating resident health data for risks such as hypertension, diabetes, cardiovascular and cerebrovascular disease, COPD, and chronic kidney disease, then returning risk levels and management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External public health staff at community health service institutions and township clinics use this skill to screen resident health records for chronic disease risk, control status, follow-up frequency, and management recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive resident health data and an API key can be sent to a configurable remote LLM endpoint.

Mitigation: Use only with authorization for that service, remove direct identifiers before input, and restrict or review any custom --base value.

Risk: Saved output files may contain sensitive medical screening information.

Mitigation: Store output only in protected locations with appropriate access controls, retention limits, and deletion procedures.

Risk: Privacy claims in the artifact are not enforced by the executable behavior.

Mitigation: Apply operational de-identification and data-handling controls before invocation instead of relying on the skill to enforce them.

Risk: Screening results may be mistaken for clinical diagnosis.

Mitigation: Use the output as decision support for qualified staff and require licensed clinicians to confirm final diagnoses and treatment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-chronic-screening)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Configured medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON screening results followed by a natural-language summary; CLI output can be printed to stdout or written as a UTF-8 file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain sensitive health screening information and should be handled as protected medical data.]

## Skill Version(s):

1.0.2 (source: server release metadata and target metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
