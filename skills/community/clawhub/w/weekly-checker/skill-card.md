## Description: <br>
Checks OpenClaw gateway status, skill library health, configuration security, Windows system health, logs, and security risks, then generates reports and Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators and maintainers use this skill to run or review weekly gateway, skill library, Windows system, configuration, log, and security checks and to produce JSON reports or Feishu alerts for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports or notifications may expose system status, configuration details, or security findings. <br>
Mitigation: Limit report and notification access to authorized maintainers and review findings before sharing. <br>
Risk: Suggested remediation could affect services, files, or permissions if executed without review. <br>
Mitigation: Keep the documented wait-for-instructions posture and perform only explicitly approved, reversible fixes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jirboy/weekly-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with example JSON report and Feishu notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces check summaries, issue severity guidance, remediation suggestions, and report paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
