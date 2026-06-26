## Description: <br>
Self-recovery and auto-repair system for OpenClaw agents that monitors agent health, detects failures, diagnoses root causes, and applies fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check OpenClaw agent health, preview repairs, run automatic recovery, and monitor repeated failures across cron, memory, configuration, sessions, skills, and network checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The heal and monitor modes can modify local OpenClaw state, including configuration, memory, session files, logs, and cron job state. <br>
Mitigation: Start with check and heal --dry-run, back up important OpenClaw files, and enable monitor mode only when repeated automatic repairs are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stevojarvisai-star/self-healing-agent) <br>
- [Publisher profile](https://clawhub.ai/user/stevojarvisai-star) <br>
- [GetAgentIQ](https://getagentiq.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON for health checks, and Markdown health reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in check, heal, monitor, or report mode; dry-run is available for repair previews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
