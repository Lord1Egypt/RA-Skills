## Description: <br>
Generates personalized vaccination reminder checklists and natural-language summaries from a resident's age, vaccination history, and special health conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community health and township clinic public health staff use this skill to produce resident-specific vaccination reminder checklists and summaries from age, vaccination records, and special health conditions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends health and vaccination records to a remote Hivoice/internal medical model endpoint, and the code does not perform de-identification itself. <br>
Mitigation: Use only when operators are authorized to send the selected records, remove direct identifiers before submission, and treat any saved output as sensitive medical data. <br>
Risk: Vaccination guidance may be incomplete, region-specific, or inappropriate for a resident's clinical circumstances. <br>
Mitigation: Have public health staff and the responsible vaccination clinician review the output against current local immunization rules and the resident's medical history before action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-vaccination-reminder) <br>
- [Hivoice medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON followed by a natural-language summary; optionally saved to a UTF-8 text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey for the configured remote medical model endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
