## Description: <br>
Reviews surgery and procedure coding against ICD/DRG audit rules using structured medical records, candidate procedures, record evidence, and rule matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical coding reviewers and health insurance operations teams use this skill to check proposed surgery or procedure codes against ICD/DRG audit rules and supporting record evidence. It returns an assistive coding-review conclusion, not diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive medical records through external and user-configurable services. <br>
Mitigation: Install only in an environment approved for sensitive medical data, configure the guideline API and LLM base URL to trusted services, redact identifiers before input, and use the no-LLM mode when remote processing is not allowed. <br>
Risk: Prepared medical record text can be persisted when the save-prepared option is used. <br>
Mitigation: Avoid saving prepared text unless stored PHI is explicitly permitted and protected by the deployment environment. <br>
Risk: The output is an assistive medical coding review and may require expert judgment. <br>
Mitigation: Treat pass, fail, and manual-review conclusions as coding-review support and keep human review in the workflow for ambiguous or high-impact cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-surgery-review) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, Guidance] <br>
**Output Format:** [JSON object with final_decision and reasoning fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The decision is constrained to pass, fail, or manual review, with concise evidence-oriented reasoning.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
