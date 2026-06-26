## Description: <br>
Converts colloquial medical record text into standardized clinical documentation with normalized terminology, rigorous phrasing, standardized data formatting, and structured sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical operations teams use this skill to normalize de-identified colloquial medical notes into structured, standardized clinical record text for documentation quality, review, and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical text may contain sensitive patient information. <br>
Mitigation: De-identify records before use and only process text that is permitted to be sent to the configured Hivoice-compatible model endpoint. <br>
Risk: The required app key could be exposed through command history, logs, or shared environments. <br>
Mitigation: Protect the app key, limit access to the execution environment, and avoid logging command invocations that include credentials. <br>
Risk: Optional prepared-text and output files can persist medical content on disk. <br>
Mitigation: Avoid saving files for identifiable patient data unless the destination directory is access-controlled and retention is approved. <br>
Risk: Generated normalized records may contain clinical errors or omissions. <br>
Mitigation: Require review by qualified clinical personnel before relying on the output for patient care, billing, quality review, or research use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-medical-term-normalization) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Hivoice-compatible model endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [UTF-8 text or optional JSON/file output from a command-line invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write normalized record text, JSON output, or prepared input text when optional output flags are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
