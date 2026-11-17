## Description:

Captures learnings, errors, and corrections to enable continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lintqiu](https://clawhub.ai/user/lintqiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, missing capabilities, and recurring best practices in structured learning logs. The skill also provides optional setup guidance and hooks that remind agents to evaluate whether durable learning should be recorded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages durable learning logs and promotion into future agent instruction files, which could preserve incorrect, sensitive, or overbroad guidance.

Mitigation: Review each proposed log or promotion, redact secrets and sensitive context, and require explicit approval before writing to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or copilot instructions.

Risk: Optional hooks can add recurring reminders to agent context and may influence future behavior if enabled too broadly.

Mitigation: Keep hooks project-scoped, avoid empty global matchers, enable them only when the operator wants durable learning capture, and disable them when not needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lintqiu/skills/self-improvement-test)
- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Self-Improvement Hook](hooks/openclaw/HOOK.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, JSON, JavaScript, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries plus optional hook and skill-extraction guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
