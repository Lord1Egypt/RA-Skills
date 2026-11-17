## Description:

Sop Extractor helps agents turn repeatable business procedures into reusable AI skills through structured dialogue or SOP document parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Employees in operations, finance, HR, and similar business roles use this skill to extract repeatable work procedures from documents or guided interviews, then review and save them as reusable AI skill workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills may create persistent automations that install software, inspect local agent configuration, or store credentials with insufficient scoping and consent.

Mitigation: Review and scan generated skills before installation, require explicit user confirmation before saving or running them, and use scoped tokens or a secret manager instead of shell profiles or plaintext environment files.

Risk: Workflows for finance, HR, approvals, or business systems may affect sensitive records or decisions if run without human oversight.

Mitigation: Require human confirmation before any generated workflow takes action in approval, payment, personnel, or other business-critical systems.

Risk: Source SOPs, screenshots, or examples may contain confidential business details that could be copied into generated skill text.

Mitigation: Redact sensitive documents and screenshots before extraction, and review generated Markdown for confidential data before sharing or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/skills/sop-extractor)
- [Dialogue examples](references/dialogue-examples.md)
- [Questioning guide](references/questioning-guide.md)
- [SOP parsing guide](references/sop-parsing-guide.md)
- [Tool discovery guide](references/tool-discovery-guide.md)
- [Generated skill template](references/skill-template.md)
- [Credential setup guide](references/credential-setup-guide.md)
- [Expense approval example](references/examples/expense-approval-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflow documents can include frontmatter, checklists, tool dependency notes, human handoff steps, and credential setup guidance.]

## Skill Version(s):

1.2.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
