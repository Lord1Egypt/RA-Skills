## Description: <br>
A local security audit skill for individual developers and small teams that scans for exposed credentials, open ports, insecure configuration, file permission issues, and Docker risks, and can suggest or apply common fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, individual maintainers, and small teams use this skill to run local pre-deployment or periodic security checks and receive structured findings with practical remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can contain sensitive file paths or secret evidence snippets. <br>
Mitigation: Review and redact findings before sharing reports outside the intended project team. <br>
Risk: Auto-fix behavior can change local file permissions or create a .gitignore file in the working directory. <br>
Mitigation: Run the skill from the intended project directory and enable auto-fix only after confirming those local changes are acceptable. <br>
Risk: Local scans inspect the current project and may run operating-system commands for port or configuration checks. <br>
Mitigation: Install and run the skill only when local project inspection and command execution are expected for the audit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON audit reports and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include finding severity, affected files, remediation notes, execution logs, and limited evidence snippets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
