## Description: <br>
Provides clinical medication consultation, personalized medication education, and rehabilitation guidance Q&A by routing selected questions to a configured medical model API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and healthcare workflow integrators use this skill to run a command-line medical Q&A helper for medication consultation, patient medication education, and rehabilitation guidance. Outputs should be treated as decision support and reviewed under institutional clinical processes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected question text is sent to the configured medical model API. <br>
Mitigation: De-identify patient data before use and only submit text approved for the target medical model service. <br>
Risk: The app key authorizes calls to the medical model API. <br>
Mitigation: Store the key securely, avoid logging it, and restrict access to users who are approved to operate the skill. <br>
Risk: Medical answers may be incomplete or inappropriate for a specific patient. <br>
Mitigation: Treat outputs as decision support only and require qualified clinical review before diagnosis, prescribing, or rehabilitation decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-medication-rehab) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Configured medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON by default, plain text answer with --text-only, and NDJSON for batch output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task, question, answer, model, input mode, and metadata fields; dry-run mode emits parsed input without calling the model.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
