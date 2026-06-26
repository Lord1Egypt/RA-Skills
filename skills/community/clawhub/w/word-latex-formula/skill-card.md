## Description: <br>
Convert manually typed formulas in Word documents (.doc, .docx, .wps) into editable Word equations while preserving layout through local Microsoft Word or LibreOffice conversion and direct OOXML edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyedavid](https://clawhub.ai/user/tianyedavid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document authors use this skill to convert typed formula text in Word manuscripts into editable Word equations. It supports local batch conversion, staged candidate review, and optional AI-assisted formula classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AI review can send formula candidates and nearby text to a configured model endpoint. <br>
Mitigation: Use the local rule-based CLI for sensitive manuscripts, or choose a trusted endpoint and assume candidate text and context will be transmitted. <br>
Risk: The local Web UI can handle documents and API keys in ways users should review before installation. <br>
Mitigation: Avoid saving API keys in the project .env unless plaintext local storage is acceptable, and stop the web server when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianyedavid/word-latex-formula) <br>
- [Usage Reference](references/USAGE.md) <br>
- [Security and Privacy Notes](references/SECURITY_AND_PRIVACY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local CLI or Web UI workflows and optional OpenAI-compatible model configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
