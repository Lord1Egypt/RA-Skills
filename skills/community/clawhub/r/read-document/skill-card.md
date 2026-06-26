## Description: <br>
Convert any document to markdown using Canonizr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmillerbakewell](https://clawhub.ai/user/hmillerbakewell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert PDFs, images, office files, and other documents into Markdown through the Canonizr CLI, with optional JSON metadata for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive document contents may be exposed depending on where the Canonizr pipeline runs. <br>
Mitigation: Confirm the Canonizr runtime and data handling path before processing sensitive documents. <br>
Risk: Service-management commands can start or stop the local Canonizr service. <br>
Mitigation: Run Canonizr service commands only when intentionally managing the local conversion service. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown transcript or JSON response, with shell commands for Canonizr CLI usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conversion behavior depends on the local Canonizr service and input document type.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
