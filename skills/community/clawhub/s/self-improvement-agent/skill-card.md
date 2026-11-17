## Description:

Captures agent learnings, errors, corrections, and feature requests into structured Markdown logs for later review, recurrence tracking, promotion to workspace guidance, or extraction into reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasye378](https://clawhub.ai/user/lucasye378)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture useful debugging outcomes, user corrections, missing capabilities, and recurring workflow patterns so future sessions can apply them. It also documents optional hook-based reminders and a workflow for turning broadly useful learnings into reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files may retain secrets, personal data, proprietary details, or raw error output.

Mitigation: Review and redact entries before saving or sharing them, and avoid storing sensitive project data in .learnings/.

Risk: Promoting learnings into workspace prompt or control files can change agent behavior across future sessions.

Mitigation: Require explicit human approval before promoting entries into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or similar prompt files.

Risk: Global hooks and cross-session transcript access can broaden the scope of data collection beyond the active task.

Mitigation: Prefer project-scoped hooks, avoid global hook installation on sensitive projects, and require consent before reading other session history.

## Reference(s):

- [Self-Improvement Agent on ClawHub](https://clawhub.ai/lucasye378/skills/self-improvement-agent)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Skill Extraction Workflow](references/skill-extraction.md)
- [Other Agents: Claude Code, Codex, Copilot](references/other-agents.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated skill scaffolds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or suggest structured learning files under .learnings/ and may scaffold skill files when the extraction helper is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
