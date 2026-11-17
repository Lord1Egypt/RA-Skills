## Description:

Creates a new OpenClaw agent and configures a Feishu bot integration from the agent name, Feishu app credentials, display name, and role description provided by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondbright](https://clawhub.ai/user/beyondbright)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create a new agent workspace, bind it to a Feishu bot, update routing configuration, generate role files, and optionally install another ClawHub skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated setup scripts handle Feishu app credentials and modify OpenClaw configuration.

Mitigation: Use test or least-privilege Feishu credentials, review the generated script before execution, and keep a backup of the OpenClaw configuration.

Risk: The Windows script uses Invoke-Expression for generated commands.

Mitigation: Avoid the Windows Invoke-Expression flow unless it is fixed or manually rewritten with direct command invocation.

Risk: The skill may copy an existing MEMORY.md into a new agent workspace.

Mitigation: Copy persistent memory only with explicit intent, and inspect MEMORY.md for sensitive or irrelevant content before reuse.

Risk: An optional ClawHub skill can be installed into the newly created agent workspace.

Mitigation: Install only trusted skills and review their behavior before adding them to the new agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beyondbright/skills/walter-agent-factory)
- [Publisher profile](https://clawhub.ai/user/beyondbright)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Bash and PowerShell script blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied OpenClaw agent details and Feishu app credentials; generated scripts modify local OpenClaw configuration and workspace files.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
