## Description: <br>
Assesses health-exam report text across cardiovascular, metabolic, cancer, liver, kidney, and thyroid risk dimensions, then produces structured risk stratification and a health-management plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Health management organizations and exam centers can use this skill to turn physical-exam reports into multidimensional risk classifications, time-bound health plans, lifestyle guidance, and referral suggestions. The output is health-management guidance and does not replace diagnosis or treatment by a clinician. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health-exam report text is sent to a remote LLM service without implemented de-identification or a clear runtime consent step. <br>
Mitigation: Remove names, IDs, phone numbers, addresses, employer details, and other identifiers before use, and run only where sending report contents to the configured service is approved. <br>
Risk: The skill can produce health-management recommendations that may be mistaken for medical diagnosis or treatment. <br>
Mitigation: Treat results as health-management guidance only and require qualified clinical review for diagnosis, treatment, or urgent-care decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-health-risk-assessment) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON followed by a natural-language health risk report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print to stdout or write to a file; depends on a configured remote LLM service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
