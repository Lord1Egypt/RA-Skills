## Description: <br>
Installs, lists, removes, and diagnoses World2Agent sensors on an OpenClaw machine through the openclaw-sensor-bridge supervisor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daibor](https://clawhub.ai/user/daibor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, monitor, and remove World2Agent sensors that watch outside-world sources and route matching signals into OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make durable host changes by installing npm packages, editing OpenClaw hook settings, and starting a background supervisor. <br>
Mitigation: Install only when local World2Agent/OpenClaw administration is intended, review packages and publishers first, and keep the stop, remove, and backup-restore paths available. <br>
Risk: Sensor credentials may be required for configured sources. <br>
Mitigation: Use limited API keys or tokens and avoid granting broader access than each sensor needs. <br>
Risk: Notifications may be auto-routed to a paired channel. <br>
Mitigation: Confirm the intended notification target before relying on the installed sensor. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, handler-skill Markdown, configuration JSON, and JSON status interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled shell scripts that normally emit one JSON object; log streaming emits raw log lines.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact SKILL.md remains 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
