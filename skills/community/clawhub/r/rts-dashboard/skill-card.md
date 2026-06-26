## Description: <br>
RTS Dashboard provides a browser-based tactical command center for monitoring OpenClaw agents, skills, sessions, cron jobs, system vitals, and Gateway chat interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[282059559donghui-prog](https://clawhub.ai/user/282059559donghui-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to start and operate a local tactical dashboard for visual monitoring of agents, skills, sessions, cron jobs, system health, and Gateway chat activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The localhost dashboard can read OpenClaw configuration, session transcripts, and the Gateway token. <br>
Mitigation: Install only in a trusted local environment, keep port 4320 private to localhost, and avoid exposing the dashboard through tunnels or shared browsers. <br>
Risk: The dashboard can send chat messages to agents and stop or restart Gateway-related local controls. <br>
Mitigation: Use it only with trusted OpenClaw instances and review the intended agent or Gateway action before launching or operating the dashboard. <br>
Risk: The dashboard creates a persistent device key file for Gateway authentication. <br>
Mitigation: Delete or rotate .device-keys.json when you stop using the dashboard or if the local workspace may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/282059559donghui-prog/rts-dashboard) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and a localhost dashboard URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local Node.js dashboard on port 4320 and provide Gateway configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
