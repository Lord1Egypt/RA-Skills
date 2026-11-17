## Description:

Records and structures patient blood glucose readings for chronic disease management, including values, units, measurement types, timestamps, and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare workflow builders can use this skill to collect patient glucose readings from JSON, table, text, document, or image inputs and return structured blood-glucose records with a concise patient-facing Markdown analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive blood-glucose records and notes and requires external medical-model analysis.

Mitigation: Avoid including names, identifiers, or extra medical details in notes, and confirm health-data consent, retention, and compliance controls before use.

Risk: Document and image inputs may include more personal health information than the skill needs.

Mitigation: Prefer JSON or CSV inputs and review prepared data before sending it for analysis.

Risk: The appkey is supplied at runtime and may be exposed through local command handling.

Mitigation: Rotate appkeys used on the command line and follow local credential-handling controls.

Risk: Generated patient-facing Markdown may be incomplete or misleading for medical decisions.

Mitigation: Review outputs before relying on them and keep clinical decisions with qualified healthcare professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-glucose-monitor-record)
- [Glucosio F-Droid package](https://f-droid.org/packages/org.glucosio.android/)
- [Configured medical-model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [UTF-8 JSON containing structured blood-glucose records and Markdown natural-language analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command can write the JSON result to a file or stdout and requires a caller-provided appkey.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
