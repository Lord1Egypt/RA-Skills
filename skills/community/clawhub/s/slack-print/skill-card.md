## Description: <br>
Print files uploaded to a Slack channel with smart matching for multiple files, filename filters, file type, and recent upload time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caigang78](https://clawhub.ai/user/caigang78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and agents use this skill to find recent Slack-uploaded files, apply simple filename or file-type filters, and send matching files or text content to a named local printer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch Slack files and send them to a named printer without an explicit safety confirmation. <br>
Mitigation: Confirm the target Slack file, printer, and file count before running print commands. <br>
Risk: The skill exposes broad printer-control commands, including queue inspection and bulk cancellation. <br>
Mitigation: Use printer-management commands only for the intended printer, and avoid bulk cancellation unless intentionally clearing that printer queue. <br>
Risk: Slack downloads may contain sensitive or unintended documents. <br>
Mitigation: Use filename, file type, time window, and limit filters to narrow matches before printing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caigang78/slack-print) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline bash commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured printer name and Slack file access in the runtime environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
