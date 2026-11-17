## Description:

Workflow Note provides Chinese writing standards and templates for agents drafting reproducible workflow-building notes about AI-built automation processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tino-chen](https://clawhub.ai/user/tino-chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent draft Chinese workflow notes with a consistent structure, reproducible steps, complete configuration excerpts, verified commands or code, and useful references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied cron prompts, AGENTS.md, HEARTBEAT.md, or similar configuration may contain secrets, personal data, internal addresses, or private instructions.

Mitigation: Review copied configuration content before publishing notes and remove sensitive or private material.

Risk: The workflow asks an agent to build, commit, and push changes as part of publication.

Mitigation: Treat build, commit, and push operations as actions requiring explicit user intent before execution.

## Reference(s):

- [Workflow Note on ClawHub](https://clawhub.ai/tino-chen/skills/workflow-note)
- [Workflow Note guide](https://tino-chen.github.io/notes/workflows/auto-note-system.html)
- [Writing example](references/example.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Chinese Markdown note drafts with YAML frontmatter, headings, tables or ASCII diagrams, command/code blocks, and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review of copied configuration content for secrets, personal data, internal addresses, and private instructions before publication]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
