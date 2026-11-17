## Description:

MCP server that tracks Claude Code subagent performance in real-time. Detects silent failures, token waste from idle loops, and duplicate task spawns. Get fleet-wide health scores and actionable alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinas90](https://clawhub.ai/user/abhinas90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a local Claude Code MCP server to monitor subagent health, detect stalled agents, estimate token waste, and summarize fleet status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local MCP server stores subagent names and task descriptions on disk under ~/.claude.

Mitigation: Avoid recording secrets, credentials, customer data, or other sensitive information in task descriptions.

Risk: Duplicate-detection and token-waste values are heuristic and may be incomplete.

Mitigation: Use the reported values as operational signals for review rather than audited measurements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhinas90/skills/subagent-health-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/abhinas90)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and MCP tool text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; the MCP server stores local state under ~/.claude.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
