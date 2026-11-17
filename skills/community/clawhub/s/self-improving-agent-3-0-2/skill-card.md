## Description:

Captures agent learnings, command errors, user corrections, and feature requests in structured markdown so future sessions can reuse and promote them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fedrov2025](https://clawhub.ai/user/fedrov2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record unexpected failures, corrections, knowledge gaps, and recurring workflow improvements, then promote broadly useful learnings into agent memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning entries may carry inaccurate or sensitive conversation content into future agent context.

Mitigation: Review and redact entries before sharing them or promoting them into auto-loaded instruction files.

Risk: Optional hooks can add recurring reminders across broad scopes when enabled globally.

Mitigation: Keep hooks project-scoped where possible and review hook scripts before enabling them.

Risk: Promoted learnings can change future agent behavior.

Mitigation: Require human review before adding learnings to shared memory, AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown entries, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local .learnings files and optionally add bootstrap reminder content when hooks are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
