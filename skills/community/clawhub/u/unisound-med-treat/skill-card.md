## Description: <br>
Generates standardized diagnosis and treatment guidance frameworks for disease-specific medical prompts using a configured internal medical LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and healthcare workflow integrators use this skill to send medical case prompts to a configured Unisound/Hivoice medical LLM and receive structured diagnosis, examination, and treatment framework guidance. Outputs are model-assisted information and are not formal clinical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided medical case text is sent to the configured Hivoice/Unisound API. <br>
Mitigation: Use the skill only when that transfer is allowed, de-identify real patient data, and follow applicable clinical data handling procedures. <br>
Risk: The required app key could be exposed or misused. <br>
Mitigation: Provide the key through protected runtime handling, avoid committing it to files or logs, and rotate it if exposure is suspected. <br>
Risk: Overriding the API URL could send sensitive prompts to an untrusted endpoint. <br>
Mitigation: Keep the default endpoint or verify any replacement endpoint before use. <br>
Risk: Generated medical guidance may be incomplete or unsuitable for a specific patient. <br>
Mitigation: Treat outputs as assistive information only and require qualified clinical review before any care decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-med-treat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON by default, plain text when text-only output is requested, and NDJSON for batch runs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an app key except in dry-run mode and can write full results to an output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
