## Description: <br>
Records patient-side chronic-care blood glucose measurements by structuring values, units, measurement types, timestamps, and notes into a standard output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patients, caregivers, or chronic-care workflow builders use this skill to capture blood glucose readings and convert supported input formats into structured records with an optional short natural-language confirmation. It is a logging aid only and does not provide diagnosis or replace clinician judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data and may send glucose values, timestamps, notes, and document contents to a remote model/API provider. <br>
Mitigation: Use structured input where possible, avoid uploading broad medical documents unless necessary, obtain appropriate consent, and verify provider retention, access-control, and privacy practices before deployment. <br>
Risk: Broad document and image inputs can include more medical or personal information than a glucose log requires. <br>
Mitigation: Minimize source files, redact unrelated content, and prefer direct field entry or local preprocessing for sensitive records. <br>
Risk: Generated summaries or reminders could be mistaken for medical advice. <br>
Mitigation: Present outputs as record confirmations, keep clinical decisions with qualified professionals, and review any user-facing medical wording before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-glucose-monitor-record) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Glucosio reference on F-Droid](https://f-droid.org/packages/org.glucosio.android/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text] <br>
**Output Format:** [UTF-8 JSON with structured data and optional Markdown or natural-language text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized glucose value, unit, measurement type, measured time, notes, status, and generated confirmation text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
