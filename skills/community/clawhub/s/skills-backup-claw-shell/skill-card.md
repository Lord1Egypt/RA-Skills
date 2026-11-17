## Description:

Executes shell commands inside a dedicated tmux session named claw and returns captured command output to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gexsta](https://clawhub.ai/user/gexsta)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when they intentionally want an agent to run shell commands in a persistent tmux session and inspect the resulting terminal output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad shell access through tmux on the host.

Mitigation: Install only when this capability is intentional, and run it in a tightly sandboxed environment.

Risk: The built-in dangerous-command check is weak control for command approval or containment.

Mitigation: Avoid secrets in the environment and require independent user review before running sensitive or destructive commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gexsta/skills/skills-backup-claw-shell)
- [ClawHub publisher profile](https://clawhub.ai/user/gexsta)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [JSON object containing the submitted command and captured terminal output, or an error object for rejected commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands run inside the tmux session named claw.]

## Skill Version(s):

1.0.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
