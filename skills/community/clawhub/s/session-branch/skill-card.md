## Description:

Branches a coding session into a new conversation by generating a structured handoff document and startup prompts when explicitly invoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when a long or branching coding conversation needs a sanitized handoff document, startup prompt, and continuation plan for a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or overwrites a project handoff file.

Mitigation: Confirm the intended handoff path before execution and review any existing file before allowing overwrite.

Risk: Optional IDE memory, profile, or configuration scans may expose personal or project-internal context.

Mitigation: Grant access only to needed sources, decline unnecessary scans, and require explicit consent before reading memory or identity files.

Risk: Generated handoff content may retain sensitive context if sanitization misses an item.

Mitigation: Review the generated handoff before sharing, committing, or using it in another environment.

## Reference(s):

- [Handoff Template](references/handoff-template.md)
- [Validation Checklist](references/checklist.md)
- [Startup Prompt Templates](references/startup-prompts.md)
- [TRAE Memory System Reference Guide](references/memory-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown handoff document, startup prompt text, validation checklist results, and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a project handoff file and may include sanitized summaries of current session state.]

## Skill Version(s):

1.4.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
