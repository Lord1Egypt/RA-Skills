## Description: <br>
Explains abnormal health exam indicators item by item, including likely causes, health impacts, intervention suggestions, urgency, correlations, and JSON plus summary text output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Health management teams and developers use this skill to convert text or JSON health exam reports into structured explanations of abnormal indicators and plain-language guidance. The output is intended for health education and review, not as a substitute for clinician diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical report content is sent to a remote model endpoint. <br>
Mitigation: Use only with organizational approval, confirm the endpoint and data-retention terms, and remove names, IDs, phone numbers, and other direct identifiers before running the skill. <br>
Risk: Output files may store health-related information after the model call completes. <br>
Mitigation: Choose output locations with appropriate access controls, retention limits, and deletion procedures for medical or personal data. <br>
Risk: The default timeout can wait indefinitely for the remote API. <br>
Mitigation: Set a finite timeout that matches operational requirements and failure-handling expectations. <br>
Risk: Generated explanations may be mistaken for medical diagnosis or treatment advice. <br>
Mitigation: Present the output as health education for review and direct users to qualified clinicians for diagnosis and care decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-abnormal-items) <br>
- [Internal medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, files] <br>
**Output Format:** [JSON followed by plain-language summary text, printed to stdout or written to an output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied input file and app key; supports optional base URL, model, timeout, output path, and encoding parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
