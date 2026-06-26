## Description: <br>
Supports clinical case analysis, differential diagnosis, and common primary-care diagnostic reasoning through task-specific prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical workflow integrators and developers use this skill to submit de-identified case questions to a configured medical LLM for case analysis, differential diagnosis, and diagnostic reasoning support. It is assistive output and not a substitute for formal clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical prompts, responses, or saved output files may contain sensitive patient information. <br>
Mitigation: Use only de-identified clinical text unless the organization has approved the configured API endpoint and retention practices; treat saved outputs as sensitive clinical records. <br>
Risk: Generated diagnostic reasoning can be incomplete, incorrect, or inappropriate for a specific patient. <br>
Mitigation: Use the output as assistive information only and require review by qualified clinical personnel before any care decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-clinical-diagnosis) <br>
- [Configured medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON by default, with optional plain text answer output and NDJSON for batches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save full JSON or NDJSON to a user-specified output path; requires an app key unless dry-run is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
