## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents across OpenClaw, Claude Code, Codex, GitHub Copilot, and similar environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, feature requests, knowledge gaps, and recurring workflow improvements as structured learning records. They can optionally promote reviewed learnings into agent memory files, hook reminders, or reusable skill scaffolds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent self-improvement memory can capture private details or incorrect guidance that later steers agent behavior.

Mitigation: Keep .learnings out of version control when it may contain sensitive details, review entries before promotion, and require human review before updating CLAUDE.md, AGENTS.md, Copilot instructions, SOUL.md, or TOOLS.md.

Risk: Automatic hooks can inject reminders broadly and may inspect command output for error detection.

Mitigation: Prefer project-local, opt-in hook setup; avoid global hooks unless the scripts have been reviewed; disable error-detection hooks when command output may contain sensitive data.

Risk: The extraction helper can write new skill scaffolds into a relative skills directory.

Mitigation: Run the helper with --dry-run first and review generated files before relying on or sharing the new skill.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown learning entries, inline shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .learnings records, agent memory files, hook settings, and generated skill scaffolds when explicitly used.]

## Skill Version(s):

3.0.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
