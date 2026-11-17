## Description:

Captures agent learnings, errors, corrections, and missing capabilities in markdown logs so future sessions can reuse them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincntk](https://clawhub.ai/user/vincntk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture corrections, command failures, knowledge gaps, and reusable practices in project-local learning files. It also guides promotion of durable learnings into agent instruction files or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived content may be persisted into future agent instructions or shared learning files.

Mitigation: Review diffs manually before promoting entries and keep promoted guidance concise, factual, and scoped to verified behavior.

Risk: Learning logs and raw command errors may capture secrets, sensitive paths, or private implementation details.

Mitigation: Redact sensitive values before logging and keep .learnings project-local or ignored when it may contain sensitive content.

Risk: Hook reminders can influence future sessions and instruction files if enabled without review.

Mitigation: Enable hooks only intentionally, inspect hook output, and treat AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, and Copilot instruction changes as security-sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincntk/skills/skill-self-improving-agent)
- [Publisher Profile](https://clawhub.ai/user/vincntk)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown entries, configuration snippets, shell commands, and reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local learning files and, when the extraction helper is run, scaffold a new skill under a relative skills directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
