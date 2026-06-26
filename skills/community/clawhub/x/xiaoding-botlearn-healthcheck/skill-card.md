## Description: <br>
BotLearn Healthcheck inspects OpenClaw instances across hardware, configuration, security, skills, and autonomy domains, then generates health reports and fix guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect OpenClaw health data, assess five operational domains, generate persistent reports, and receive guided remediation steps with confirmation before changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect broad local OpenClaw state, including configuration, logs, identity-related directories, security diagnostics, heartbeat files, and workspace metadata. <br>
Mitigation: Use targeted checks where possible, review generated reports for sensitive local details, and avoid sharing reports without redaction. <br>
Risk: Diagnostic collection can surface sensitive paths or credential-related findings. <br>
Mitigation: Keep credential values redacted and report only credential types, paths, and remediation steps. <br>
Risk: Fix guidance may include commands that modify local OpenClaw state. <br>
Mitigation: Require explicit user confirmation, show the intended command and rollback plan, and verify results after execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/asterisk622/xiaoding-botlearn-healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and HTML health reports with concise status summaries, domain scores, issue tables, and fix guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes health reports under OPENCLAW_HOME memory health-report paths and uses local OpenClaw diagnostics where available.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
