## Description: <br>
Convert OpenClaw skills into properly configured agents with correct workspace setup, binding, and orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drafthead](https://clawhub.ai/user/drafthead) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert OpenClaw skills into registered agents with workspace files, tool access, binding strategy, and session-spawn configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to create persistent agents and patch OpenClaw configuration. <br>
Mitigation: Back up OpenClaw configuration and agent directories before applying changes, and define how created agents will be stopped, disabled, and deleted. <br>
Risk: Configuration patches and generated agent files can overgrant tools or bind agents to the wrong workspace. <br>
Mitigation: Inspect every config.patch payload, verify cwd and agentDir values, and grant only the tools each agent needs. <br>
Risk: Cleanup steps may include destructive directory deletion. <br>
Mitigation: Avoid copy-pasting rm -rf cleanup commands; prefer dry-runs or moving directories to backups first. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drafthead/skill-to-agent-converter) <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [War Room Skill Conversion Example](references/war-room-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent OpenClaw agent workspaces, configuration patches, and session-spawn settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
