## Description:

Captures agent learnings, errors, corrections, and feature requests so future sessions can reuse project-specific knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyz3327-design](https://clawhub.ai/user/chengyz3327-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to log corrections, failed commands, missing capabilities, and recurring practices into project learning files, then promote durable patterns to agent memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files or promoted agent memory can capture sensitive session details or misleading guidance.

Mitigation: Keep learnings project-scoped, avoid secrets and raw transcripts, and require a visible diff plus explicit approval before promoting entries into agent memory files.

Risk: Optional hooks can inject reminders into agent context and run with the agent environment's permissions.

Mitigation: Review hook scripts and settings changes before enabling them, avoid global hooks, and enable only the minimum hooks needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chengyz3327-design/skills/warren-self-improving-agent-v2)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and optional hook script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-scoped .learnings files and optional agent memory files when the user approves promotion.]

## Skill Version(s):

3.0.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
