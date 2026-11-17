## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can preserve useful lessons and promote broadly applicable guidance into project memory or reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture non-obvious failures, corrections, missing capabilities, and reusable best practices during coding sessions. It supports optional hooks, learning templates, and promotion workflows for agent memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning and memory workflows can preserve incorrect, sensitive, or unwanted content.

Mitigation: Review each entry before it is written or promoted, redact secrets and personal data, and require explicit approval before changing agent prompt or memory files.

Risk: Broad or global hooks can inject reminders into sessions where the workflow is not appropriate.

Mitigation: Keep hooks project-scoped, enable them only where this learning workflow is desired, and disable them for unrelated or sensitive workspaces.

Risk: Cross-session transcript tools can expose information outside the intended confidentiality boundary.

Mitigation: Use cross-session transcript access only when the session owner and sharing boundary are clear.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bingze00000/skills/self-improving-agent-jarvis)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or recommend .learnings/ entries, memory-file updates, hook configuration, and skill scaffolds.]

## Skill Version(s):

3.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
