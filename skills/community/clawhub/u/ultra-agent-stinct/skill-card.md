## Description:

Ultra Agent Stinct guides coding agents through debugging, code changes, tests, git checks, and escalation when a task hits errors or unexpected behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grimmjoww](https://clawhub.ai/user/grimmjoww)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding-agent operators use this skill to give agents a structured recovery workflow when builds, tests, scripts, or code edits fail during normal software tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate broadly during debugging and may guide an agent to run project commands or edit code.

Mitigation: Install only when that always-on debugging behavior is acceptable, keep changes reviewable, and require explicit approval for destructive, commit, push, or deletion actions.

Risk: The skill can recommend spawning external coding agents for large tasks, which may expose repository content, credentials, or network access if not scoped.

Mitigation: Require explicit approval before delegation, pass delegated prompts without shell string interpolation, and run delegated agents with limited repository, credential, and network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/grimmjoww/skills/ultra-agent-stinct)
- [Git Workflow Reference](references/git-workflow.md)
- [Escalation Guide](references/escalation-guide.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing workflow guidance; may lead the agent to run commands, edit files, or delegate work when invoked.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
