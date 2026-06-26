## Description: <br>
System Inspection is a low-noise OpenClaw health-check SOP for checking gateway status, channel health, cron/task state, and recent error logs, then reporting only actionable issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators use this skill to run scheduled or manual system inspections across gateway, channel, cron, task, and log signals. It helps summarize findings as conclusion, reason, and recommendation entries while suppressing routine no-action updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create operational side effects by probing configured channels, sending low-noise test messages, and recommending or performing gateway restarts during troubleshooting. <br>
Mitigation: Run manually first, require human approval before restarts or test messages, and confirm channel probes are appropriate for the deployment. <br>
Risk: The skill records inspection summaries into personal and shared memory paths, which could persist operational details. <br>
Mitigation: Use sanitized, opt-in audit records and write only to memory paths controlled by the deployment owner. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1yihui/system-inspection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status summary with inline shell commands and optional NO_REPLY output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write inspection summaries to personal and shared memory files when the run completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
