## Description:

Captures learnings, errors, user corrections, feature requests, and knowledge gaps so coding agents can maintain durable improvement notes and promote important patterns to project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanghuaqi](https://clawhub.ai/user/fanghuaqi)

### License/Terms of Use:


## Use Case:

Developers and coding-agent operators use this skill to record command failures, corrections, feature requests, and durable project knowledge. The skill helps agents review local learning logs and promote recurring, broadly useful lessons into project or workspace instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived content into future agent instruction files.

Mitigation: Keep .learnings local by default, redact secrets and personal data before logging, and require human review before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Broad hooks can inject learning reminders across sessions.

Mitigation: Enable hooks only when desired, prefer project-scoped configuration, and avoid global always-on hook installation unless the workflow has been reviewed.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Learning Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates local learning logs and may propose promotions into agent instruction files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
