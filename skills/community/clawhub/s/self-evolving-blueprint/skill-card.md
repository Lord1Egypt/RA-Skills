## Description:

Build a self-evolving memory and learning system for an OpenClaw AI assistant using a three-layer memory architecture, self-improvement workflow, and reusable Markdown templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shu0yu](https://clawhub.ai/user/shu0yu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up local memory files, conversation retrieval, and self-improvement records so an AI assistant can retain user preferences, project context, mistakes, and useful habits across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can accumulate sensitive personal details, preferences, project context, and conversation history.

Mitigation: Avoid storing secrets or sensitive personal details, review proposed writes before saving them, and use the documented pause, skip, delete, and rollback controls.

Risk: Broad read, write, edit, exec, and memory access can affect local workspace files when enabled.

Mitigation: Grant only the tools needed for the intended setup, require confirmation before file edits or shell commands, and keep workspace backups before copying templates.

Risk: Self-updating rules can preserve incorrect assumptions or reinforce unwanted assistant behavior.

Mitigation: Promote Mistakes, Habits, and AGENTS changes only after user review, keep verification status visible, and retire rules that are rejected or no longer useful.

## Reference(s):

- [Three-Layer Memory Architecture](references/architecture.md)
- [Self-Evolution System](references/self-evolution.md)
- [Workflow and Operating Rules](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with template files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace templates and operating guidance; it does not call external APIs by itself.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
