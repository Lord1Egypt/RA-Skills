## Description:

Build and operate a cross-gateway AgentNetwork using Discord as the message bus and GitHub as shared state storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate agents across gateways, maintain a shared roster, publish heartbeat and registry events, and route task messages through Discord with GitHub-backed shared state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate shared GitHub-backed registry state and publish coordination events to a Discord channel.

Mitigation: Review references/git-config.json before use, run in a dedicated clean repository or worktree, and require human approval for pushes and admin offline/remove actions.

Risk: The skill can create or synchronize AGENT_CONSTITUTION.md and update a workspace MEMORY.md constitution index, which may affect future agent behavior.

Mitigation: Require human review for constitution changes, avoid automatic MEMORY.md edits unless intended, and verify rollback steps after sync failures.

Risk: Remote shared instructions and registry state can become mutable sources of operational behavior.

Mitigation: Treat the shared repository as controlled infrastructure with access restrictions, change review, and periodic inspection of registry and constitution contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reed1898/skills/reed-agent-network)
- [Configured shared-state repository](https://github.com/reed1898/agent-network-data.git)
- [git-config.json](references/git-config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON protocol messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update registry JSON, AGENT_CONSTITUTION.md, and a managed MEMORY.md constitution index when initialized.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
