## Description: <br>
Super Freedcamp Agent Skill lets an agent use the Freedcamp REST API to discover projects, list and update tasks, create comments, manage task lists, and review notifications through JSON CLI output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to connect an agent to a Freedcamp workspace for task triage, project discovery, task creation and updates, comments, task lists, and notification review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify a Freedcamp workspace when configured with valid API credentials. <br>
Mitigation: Use the least-privileged Freedcamp credentials available and require confirmation before create, update, comment, or mark-read actions. <br>
Risk: The CLI stores a local session cache that may contain session material for the connected Freedcamp account. <br>
Mitigation: Restrict filesystem access to the cache path or set FREEDCAMP_SESSION_PATH to a protected location. <br>
Risk: Raw HTML can be sent in Freedcamp comments. <br>
Mitigation: Review generated comment content before sending, especially when using the raw HTML option. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-freedcamp-agent-skill) <br>
- [Freedcamp](https://freedcamp.com) <br>
- [Freedcamp API v1](https://freedcamp.com/api/v1) <br>
- [Implementation reference](references/REFERENCE.md) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw skills configuration](https://docs.openclaw.ai/tools/skills-config) <br>
- [OpenClaw CLI config](https://docs.openclaw.ai/cli/config) <br>
- [AgentSkills format](https://agentskills.io/home) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON stdout from a Node.js CLI, with Markdown usage guidance in the skill files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FREEDCAMP_API_KEY and FREEDCAMP_API_SECRET; the local session cache path can be overridden with FREEDCAMP_SESSION_PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
