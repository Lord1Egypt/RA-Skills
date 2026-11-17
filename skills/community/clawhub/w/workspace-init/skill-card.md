## Description:

Bootstrap a new OpenClaw agent workspace with best-practice file structure, including AGENTS.md, SOUL.md, HEARTBEAT.md, memory files, and agent discovery configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to initialize an OpenClaw workspace with persistent instruction, memory, user, tool, and heartbeat files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup persists third-party agent-network instructions and heartbeat network checks in workspace files.

Mitigation: Review the generated AGENTS.md and HEARTBEAT.md content before adoption and remove OADP markers or heartbeat network commands unless the agent-network behavior is intended.

Risk: The setup sends the machine hostname to onlyflies.buzz during the automatic ping.

Mitigation: Run the setup only if the external service is trusted, or disable the automatic ping before execution.

## Reference(s):

- [Workspace Init ClawHub page](https://clawhub.ai/imaflytok/skills/workspace-init)
- [Publisher profile](https://clawhub.ai/user/imaflytok)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initializes files under OPENCLAW_WORKSPACE or ~/.openclaw/workspace and may run network requests during setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
