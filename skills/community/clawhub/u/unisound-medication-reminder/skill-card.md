## Description:

Builds medication reminder plans for chronic disease patient management, including structured schedules and patient-facing reminder text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Patients and care-management agents use this skill to turn medication names, doses, frequencies, reminder times, and date ranges into a three-day medication reminder plan. The skill is limited to reminder management and does not judge medication suitability, adjust prescriptions, or provide dose guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medication details and the API bearer key are sent to a documented remote model service.

Mitigation: Use the skill only when the provider, retention terms, and compliance posture are acceptable; avoid real patient data unless those requirements are met.

Risk: Broad document and OCR input processing can expose more sensitive content than a structured reminder record requires.

Mitigation: Prefer JSON input containing only the fields needed for the reminder plan.

Risk: Generated Markdown can be mistaken for medical advice or dose guidance.

Mitigation: Treat the output as reminder-management text only and keep medication suitability, prescription changes, and dose decisions outside the skill.

Risk: The skill includes an unverified shared-code fallback for document preprocessing.

Mitigation: Review the installed runtime environment and shared preprocessing code before enabling non-JSON inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-medication-reminder)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [MedTimer medication reminder reference](https://f-droid.org/en/packages/com.futsch1.medtimer/)
- [Remote model endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance, Configuration]

**Output Format:** [UTF-8 JSON containing structured reminder data and Markdown patient-facing reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API bearer key and supports JSON, text, table, document, and image inputs when the needed parsers or OCR tools are available.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
