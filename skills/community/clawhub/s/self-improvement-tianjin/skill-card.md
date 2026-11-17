## Description:

Captures learnings, errors, corrections, feature requests, and recurring patterns so agents can preserve useful discoveries and improve future project guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianjin-ren](https://clawhub.ai/user/tianjin-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log corrections, command failures, knowledge gaps, feature requests, and reusable best practices into structured learning files. It also guides when to promote broadly useful learning into project or workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived guidance can persist incorrect or misleading instructions into project or workspace memory files.

Mitigation: Review logged learnings and require explicit human approval before promotion into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: Always-on hooks can repeatedly inject guidance into agent context and affect future behavior.

Mitigation: Prefer project-scoped, opt-in hooks and avoid global hook configuration unless the operational impact is understood.

Risk: Learning logs and session-sharing workflows may capture sensitive prompts, secrets, or raw transcripts.

Mitigation: Do not log secrets or raw transcripts, and review entries before sharing them across sessions or storing them in durable memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tianjin-ren/skills/self-improvement-tianjin)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to append or update local learning and memory files when the guidance is followed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
