## Description: <br>
ManualExpert translates hardware and technical manuals into complete page-by-page bilingual Markdown tables and exports them to Word for DTP preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mugeng-su](https://clawhub.ai/user/Mugeng-su) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and documentation teams use this skill to translate Chinese hardware or technical manuals into English while preserving page boundaries, source text, and translated text in bilingual tables. DTP teams use the included exporter to convert the generated Markdown into a structured Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manuals may contain confidential or sensitive product information. <br>
Mitigation: Use the skill only with manuals that are appropriate to process in the agent environment. <br>
Risk: Word export depends on python-docx being available locally. <br>
Mitigation: Install python-docx from a trusted package source before running the export script. <br>
Risk: Exporting a Word document to the wrong path can replace or misplace generated files. <br>
Mitigation: Choose output paths deliberately and review them before running the export command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands] <br>
**Output Format:** [Markdown bilingual tables with optional Word (.docx) export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains page-by-page pagination and uses a local python-docx export script when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
