## Description: <br>
Selects the primary diagnosis and primary surgery for a hospital admission from user-provided candidate lists using medical record summaries and an internal medical LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical documentation, medical coding, and integration teams use this skill to process de-identified admission summaries with candidate diagnosis and surgery lists, then return the admission's main diagnosis and main surgery as coding support. The output is auxiliary information for insurance coding or medical record forms and is not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical record text can be sent to a configurable remote LLM endpoint. <br>
Mitigation: Use only in an approved medical-data environment, de-identify patient data before input, and confirm endpoint, retention, authorization, and compliance controls before processing PHI. <br>
Risk: Prepared medical text may be written to disk when debug saving is enabled. <br>
Mitigation: Avoid prepared-text saving with real PHI unless explicitly approved; when needed, write only to controlled storage and remove debug artifacts under the applicable retention policy. <br>
Risk: LLM-selected primary diagnosis or surgery may be incorrect even when constrained to candidate lists. <br>
Mitigation: Require qualified human review before use in coding, billing, medical records, or care workflows, and keep the skill's output limited to decision support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-primary-diagnosis-surgery-selection) <br>
- [Default internal medical LLM endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files] <br>
**Output Format:** [JSON object with main_diagnosis and main_surgery fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validates the selected diagnosis and surgery against the provided candidate lists; optional output arguments can write the same JSON result to disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
