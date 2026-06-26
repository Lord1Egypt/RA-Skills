## Description: <br>
Install and manage QuantumOS, an AI command center dashboard for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murtiurti4](https://clawhub.ai/user/murtiurti4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, start, stop, update, and troubleshoot the QuantumOS dashboard for chat, Mission Control task management, feed monitoring, and agent settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an OpenClaw gateway token in a local application configuration file. <br>
Mitigation: Treat the gateway token as a secret, keep the local configuration file private, verify it is not committed, and rotate the token if it is exposed. <br>
Risk: Mission Control automation can cause dashboard-created tasks to trigger future agent work. <br>
Mitigation: Add the automation only in trusted workspaces where this behavior is desired, and review incoming tasks before relying on agent actions. <br>


## Reference(s): <br>
- [QuantumOS on ClawHub](https://clawhub.ai/murtiurti4/quantumos) <br>
- [Node.js](https://nodejs.org) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users to run a setup script, configure environment variables, and optionally add Mission Control automation.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
