## Description: <br>
Use this for ClickZetta Studio requests such as querying tasks, listing workspaces, checking projects, and creating or running ClickZetta jobs from a single JDBC secret configured in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luketalent](https://clawhub.ai/user/luketalent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with ClickZetta Studio tasks, workspaces, projects, jobs, and SQL workflows through a configured JDBC secret. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a configured ClickZetta account and may automatically approve some remote action requests. <br>
Mitigation: Install only for trusted publishers, use a least-privileged ClickZetta credential, and review or disable automatic interrupt approval before mutating workflows. <br>
Risk: The skill stores local session tokens for ClickZetta Studio access. <br>
Mitigation: Avoid shared machines and clear the local OpenClaw cache when the session is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luketalent/studio-agent) <br>
- [Publisher profile](https://clawhub.ai/user/luketalent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with JSON runner results and inline shell commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and CZ_STUDIO_JDBC_URL; acts through the configured ClickZetta account.] <br>

## Skill Version(s): <br>
0.1.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
