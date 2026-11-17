## Description:

Helps an agent summarize conversation-derived budget scripts, data models, and field updates for maintaining platform-script and budget-data-model skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lan2898408767](https://clawhub.ai/user/lan2898408767)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams maintaining budget-system agent skills use this skill to capture new script patterns, table definitions, fields, and business rules from a conversation and organize them into existing skill reference files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived scripts and data models could be saved into other skill files without a clear review step.

Mitigation: Require a preview diff and explicit confirmation before every write, and restrict destination files to the intended budget-script and data-model references.

Risk: Captured conversation content could include secrets, personal data, internal endpoints, or unreviewed code.

Mitigation: Do not save sensitive data or unreviewed code from conversation history; review and redact proposed updates before accepting them.

Risk: Incorrect scripts, fields, or business rules could be propagated into future budget workflows.

Mitigation: Validate script syntax, API availability, field names, data types, and duplicates before appending new entries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lan2898408767/skills/shucheng-summary-budget-model-and-new-script)
- [Usage Guide](references/使用说明.md)
- [Update Log](references/update_log.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown text with Groovy examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or append updates to skill reference files and update logs when authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
