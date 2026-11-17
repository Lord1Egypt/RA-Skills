## Description:

Helps agents capture learnings, errors, feature requests, and correction patterns in structured markdown logs so future sessions can improve from prior work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep durable records of corrections, command failures, feature requests, and reusable lessons. It is especially useful in OpenClaw or similar coding-agent workflows where learnings may be reviewed and promoted into workspace memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted memory files can carry incorrect guidance into future agent sessions.

Mitigation: Require manual review before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions, and keep entries concise and source-grounded.

Risk: Optional hooks can make reminders always-on and may inspect command output for error patterns when configured.

Mitigation: Install hooks only in trusted, project-scoped environments, prefer local over global hook configuration, and enable error-detection hooks only after reviewing the behavior.

Risk: Cross-session transcript or message sharing can expose sensitive context if used too broadly.

Mitigation: Use cross-session sharing only when the target session and scope are explicitly chosen, and share sanitized summaries rather than raw transcripts, secrets, tokens, keys, or full command output.

## Reference(s):

- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets, configuration examples, and optional hook or helper script files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or append .learnings markdown files and propose reviewed updates to persistent agent memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
