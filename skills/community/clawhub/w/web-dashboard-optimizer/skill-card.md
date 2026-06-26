## Description: <br>
Creates smooth, stable web monitoring dashboard templates for AI agents with smart refresh, scroll position retention, modal interaction, auto-restart, and responsive design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqh07-bit](https://clawhub.ai/user/zqh07-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scaffold or adapt local web monitoring dashboards for task execution, data visualization, real-time status panels, and admin interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated monitor script can run a continuously restarting local Node.js service. <br>
Mitigation: Review the script, PID file, log path, and port before running it; stop or supervise the process explicitly in production-like environments. <br>
Risk: Troubleshooting guidance includes a force-kill command for processes on the dashboard port. <br>
Mitigation: Verify the target process before using the command and replace it with a narrower stop procedure when possible. <br>
Risk: The sample server may expose monitoring data over a local HTTP endpoint if adapted without access controls. <br>
Mitigation: Review data sources and bind or access controls before exposing the dashboard beyond a trusted local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zqh07-bit/web-dashboard-optimizer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, Node.js, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local dashboard and restart-script templates; users should review ports, process commands, and exposed monitoring data before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
