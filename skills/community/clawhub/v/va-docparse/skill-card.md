## Description: <br>
vaDocparse extracts text, tables, and formulas from PDFs and supported image files using a configured document parsing service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[va-ais](https://clawhub.ai/user/va-ais) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and engineers use this skill to extract readable Markdown or JSON content from PDFs and supported image documents. It is intended for OCR-style document parsing, not audio, video, general photos, source code, or Office files that have not been converted to PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload complete local PDFs or images to a configured remote document parsing service. <br>
Mitigation: Install only with a trusted service endpoint, prefer HTTPS, and avoid highly sensitive documents unless the service retention and logging policy is acceptable. <br>
Risk: Service credentials and endpoint configuration may be stored in plaintext configuration files. <br>
Mitigation: Replace bundled fallback values, store credentials in a protected environment or managed configuration, and rotate any exposed API key. <br>
Risk: The configured parsing service determines the fidelity and privacy properties of the extracted content. <br>
Mitigation: Review the service provider, validate outputs before downstream use, and preserve the original response without unsupported rewriting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/va-ais/va-docparse) <br>
- [Publisher profile](https://clawhub.ai/user/va-ais) <br>
- [Artifact origin](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON document extraction output with status and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes parsed content to a local output file and can return a summary, file path, output size, and error codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
