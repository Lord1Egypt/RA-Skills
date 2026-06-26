## Description: <br>
Generate PPT decks from prompts/block XML while preserving corporate brand style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phil-osophy-42](https://clawhub.ai/user/phil-osophy-42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to generate branded PowerPoint decks from structured block XML or presentation prompts while reusing a local corporate template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because user inputs can select local template and output paths without confinement. <br>
Mitigation: Install only in a restricted workspace or add path validation that rejects absolute paths and '..', confines templates to a trusted template directory, and writes outputs only to an approved output directory. <br>
Risk: A supplied PowerPoint template can influence generated deck content and should be treated as trusted input. <br>
Mitigation: Use only reviewed corporate templates from trusted storage and avoid rendering decks from unknown or untrusted PPT template files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phil-osophy-42/slug) <br>
- [Publisher profile](https://clawhub.ai/user/phil-osophy-42) <br>


## Skill Output: <br>
**Output Type(s):** [files, text] <br>
**Output Format:** [PPTX file with JSON-like status fields for output path, slide count, fallback count, and message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python-pptx and a trusted local PPT template; block_xml is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
