## Description: <br>
Monitors Raspberry Pi CPU temperature, provides crontab and OpenClaw cron setup options, and sends an alert when the configured temperature threshold is exceeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archerweiye](https://clawhub.ai/user/archerweiye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Raspberry Pi operators use this skill to generate or apply lightweight CPU temperature monitoring, scheduled checks, and over-temperature alerting for local devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled execution may continue running after installation. <br>
Mitigation: Review any crontab or OpenClaw cron entry before enabling it, confirm the schedule and threshold, and document how to remove the job. <br>
Risk: The alert script reads a local OpenClaw gateway token from a hard-coded path. <br>
Mitigation: Replace the token path with explicit local configuration and prefer a narrowly scoped alerting token or an unauthenticated local notifier. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash code blocks and shell script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes configurable temperature threshold, schedule interval, and alert channel guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
