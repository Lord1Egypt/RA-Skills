## Description:

Captures learnings, errors, and corrections so agents can log failures, user corrections, missing capabilities, outdated knowledge, and recurring best practices for continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biocrfhkust-cloud](https://clawhub.ai/user/biocrfhkust-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, corrections, feature requests, and useful practices in `.learnings/` Markdown files, then promote durable patterns into project or workspace guidance for future agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived content can be stored and promoted into future agent instruction files without clear approval or redaction controls.

Mitigation: Keep hooks opt-in and project-scoped, review exact diffs before writing to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or copilot instructions, and redact secrets, tokens, personal data, raw stack traces, request payloads, and customer details before logging or sharing learnings.

Risk: Persistent learning logs may preserve sensitive operational context.

Mitigation: Log concise sanitized summaries and omit secrets, customer data, raw payloads, and unnecessary stack traces.

Risk: The extraction helper can scaffold new skill files from logged learnings.

Mitigation: Use dry-run mode or review generated files before enabling, committing, or sharing extracted skills.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, file templates, and optional hook or skill scaffolding code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update `.learnings/` logs, agent memory files, hook configuration, or extracted skill files when the user opts in.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
