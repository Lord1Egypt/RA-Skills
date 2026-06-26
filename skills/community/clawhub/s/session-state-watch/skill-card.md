## Description: <br>
Detect SESSION-STATE.md changes from cron/background tasks and notify main session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyzh09](https://clawhub.ai/user/tyzh09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to detect when background or cron tasks append updates to SESSION-STATE.md, then surface those updates in the main agent session before substantive responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watcher can automatically truncate SESSION-STATE.md and discard older session history. <br>
Mitigation: Disable or adjust auto-truncation before use, and add backup or archival rotation for important session history. <br>
Risk: The daemon stop command uses a loose process match. <br>
Mitigation: Avoid --stop-daemon until it is changed to use a PID file or another precise process-management method. <br>
Risk: SESSION-STATE.md content from cron or background tasks may be untrusted. <br>
Mitigation: Review the file contents before acting on them, especially when updates originate from automated jobs. <br>


## Reference(s): <br>
- [Session State Watch on ClawHub](https://clawhub.ai/tyzh09/session-state-watch) <br>
- [Event-driven watch mode](scripts/README-event-driven.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update SESSION-STATE.md and a local tracker file when the included shell script is run.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
