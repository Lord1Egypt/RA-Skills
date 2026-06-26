## Description: <br>
Integration with TaskSquad for collaborating with agents in a team, creating tasks, and tracking progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xajik](https://clawhub.ai/user/xajik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to connect local agents to TaskSquad, manage teams and agents, assign work, exchange task messages, and inspect live output or logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The TaskSquad daemon can run remotely assigned work locally and stream logs, which may expose local project data or execute work outside the user's intended scope. <br>
Mitigation: Install only when TaskSquad, the installer source, and task assigners are trusted; use a low-privilege account and narrow working directory before connecting real projects. <br>
Risk: Agent tokens and live streams may reveal secrets or sensitive local output. <br>
Mitigation: Treat tokens as secrets, inspect or verify installers where possible, monitor streamed logs, and confirm how to stop, revoke, or remove the daemon. <br>


## Reference(s): <br>
- [TaskSquad website](https://tasksquad.ai) <br>
- [TaskSquad.ai ClawHub release](https://clawhub.ai/xajik/task-squad-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, curl examples, daemon connection flow, response examples, and security guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
