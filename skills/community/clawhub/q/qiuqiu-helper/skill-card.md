## Description: <br>
Automates workspace tasks including summarizing recent changes, adding timestamped notes, and cleaning old log files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmogdeveloper](https://clawhub.ai/user/mmogdeveloper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace users use Qiuqiu Helper to get a concise status summary, save quick notes, and clean stale log files during routine project work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick note workflow can write user-provided content into a memory folder. <br>
Mitigation: Confirm the note content and target filename before saving sensitive or long-lived information. <br>
Risk: The log cleanup workflow can delete files when pointed at an overly broad or important directory. <br>
Mitigation: Confirm the cleanup path and retention period before running it, and avoid using broad project or system directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmogdeveloper/qiuqiu-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or plain text guidance, with optional shell commands and file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append timestamped notes and delete old log files when those helper workflows are used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
