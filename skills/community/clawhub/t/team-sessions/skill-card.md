## Description:

Team Sessions provides a structured workflow for a lead agent to delegate tasks to isolated subagent workspaces using OpenClaw session tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-zwl](https://clawhub.ai/user/zhao-zwl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-agent task delegation, configure isolated member workspaces, and route work through a single lead agent instead of direct subagent-to-subagent communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default setup grants broad subagent spawning through allowAgents ["*"] and modifies persistent OpenClaw configuration.

Mitigation: Install only when a multi-agent delegation workflow is intended, replace the wildcard with an explicit allowlist of approved agent IDs, and document how to undo the openclaw.json change.

Risk: Subagent workspaces may expose secrets or private code to agents that do not need that context.

Mitigation: Review each subagent workspace and SOUL.md before use, keep workspaces scoped to the assigned role, and avoid sending secrets or unnecessary private code to subagents.

Risk: Persistent member workspaces and gateway restarts can leave lasting operational state after testing or experimentation.

Mitigation: Track created workspaces and configuration changes, restart the gateway only after review, and remove unused persistent workspaces when the workflow is retired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhao-zwl/skills/team-sessions)
- [README](artifact/README.md)
- [Usage Examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Code]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on OpenClaw subagent configuration, session spawning, task package format, and workspace isolation.]

## Skill Version(s):

1.0.2 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
