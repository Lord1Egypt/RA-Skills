## Description: <br>
Shared Brain provides a persistent memory layer for multi-agent OpenClaw workspaces so agents can queue, curate, and share durable project facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to install and maintain shared persistent memory across multiple AI agents. It helps agents write validated facts to a queue, curate them into a canonical memory file, and load current project ground truth at startup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace-wide persistent memory can influence every agent in the workspace. <br>
Mitigation: Review the skill before installation, run sb-install.sh --dry-run first, and back up AGENTS.md, HEARTBEAT.md, and existing memory files before applying changes. <br>
Risk: Untrusted or sensitive content stored in shared memory could propagate into future agent sessions. <br>
Mitigation: Restrict who can write to the queue and do not store secrets, webhook content, user content, emails, or other untrusted external text in the shared brain. <br>


## Reference(s): <br>
- [Heartbeat Integration](references/heartbeat-integration.md) <br>
- [Shared Brain on ClawHub](https://clawhub.ai/ohernandez-dev-blossom/shared-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs and updates workspace memory files, AGENTS.md startup instructions, HEARTBEAT.md curation steps, and local helper scripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
