## Description: <br>
WPS Office Suite helps agents create, edit, convert, and inspect Word, Excel, PowerPoint, and PDF documents using WPS Office, Microsoft Office, LibreOffice, or pure Python fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and office automation users use this skill to let an agent operate local office documents, generate basic documents and spreadsheets, convert formats, inspect recent files, and choose an available office engine automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit local documents in place and create or overwrite office files. <br>
Mitigation: Use copies of important documents, keep backups, and review output files before relying on them. <br>
Risk: The skill can inspect recent files in Desktop and Documents, exposing filenames and local metadata to the agent workflow. <br>
Mitigation: Run it only in trusted local profiles and avoid using it where document names or paths are sensitive. <br>
Risk: Feedback commands can open a browser or email client and may include system diagnostics. <br>
Mitigation: Avoid the feedback email command on sensitive systems unless the generated email content has been reviewed. <br>
Risk: Office and LibreOffice automation may launch local applications, hang, or behave differently across installed engines. <br>
Mitigation: Run the environment self-check first, prefer small test files, and close or recover office processes if automation stalls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fyniujin/skills/wps-office-suite) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact architecture notes](artifact/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local office files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify DOCX, XLSX, PPTX, PDF, HTML, TXT, and PNG files locally.] <br>

## Skill Version(s): <br>
2.5.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
