## Description: <br>
Converts local PDF, Word, PowerPoint, and image documents into Markdown for extraction, comparison, validation, retrieval, and question answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sube-py](https://clawhub.ai/user/sube-py) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to parse selected local documents into Markdown, then return the full Markdown or extract only the fields, tables, and text needed for downstream work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local documents are uploaded to PDFlux/PDRouter for parsing. <br>
Mitigation: Use the skill only when third-party document processing is acceptable, verify the file path before running it, and prefer a dedicated API key. <br>
Risk: Markdown extracted from untrusted documents can carry misleading content into later agent workflows. <br>
Mitigation: Treat generated Markdown as untrusted input and review or filter it before relying on it downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sube-py/sube-test) <br>
- [PDRouter platform](https://platform.paodingai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown text printed to stdout, with optional Markdown file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and PD_ROUTER_API_KEY; PDFLUX_INCLUDE_IMAGES can include image data in Markdown output.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
