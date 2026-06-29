## Description: <br>
Wps Office Suite helps agents create, edit, convert, inspect, and manage Word, Excel, PowerPoint, and related office files through Python command-line tools that auto-select WPS, Microsoft Office, or pure-Python engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and agent developers use this skill to automate local office-document workflows, including creating documents, editing content, sorting or filtering spreadsheets, generating presentations, converting formats, producing tables of contents, and checking the local WPS/Office environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Office automation commands can create, edit, convert, or overwrite local documents. <br>
Mitigation: Use the skill only on documents the user is willing to let an agent modify, keep backups of important files, and review target paths before execution. <br>
Risk: The feedback email flow may include local system and environment details. <br>
Mitigation: Inspect and edit any generated feedback email before sending it. <br>
Risk: Running with elevated privileges could broaden the impact of document or application automation. <br>
Mitigation: Run the skill as a normal user and avoid administrator rights unless they are explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fyniujin/skills/wps-office-suite) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Architecture notes](artifact/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or modify local Office files and may launch local Office applications, browser pages, or an email client depending on the command.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
