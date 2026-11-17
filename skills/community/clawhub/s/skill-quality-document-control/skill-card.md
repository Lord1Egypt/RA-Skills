## Description:

A Chinese-language assistant for quality-system document control that helps generate numbering systems, approval and change workflows, controlled document matrices, retention guidance, external-document controls, and version or obsolescence assessments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, compliance, and document-control teams use this skill to produce Markdown templates and guidance for controlled document numbering, change management, document matrices, retention periods, external document control, and version or obsolete-document decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retention and destruction guidance may not match the user's jurisdiction, industry rules, or company approval process.

Mitigation: Review retention periods, destruction steps, and approval routing against applicable law, customer requirements, and internal procedures before operational use.

Risk: Generated document-control templates may contain placeholders or examples that are not valid for a specific enterprise.

Mitigation: Replace company codes, lifecycle assumptions, customer requirements, and other marked placeholders with verified enterprise-specific information.

Risk: The skill provides guidance and templates, not final approval, signature authority, or official controlled documents.

Mitigation: Route outputs through the organization's document-control approval process before release or use as controlled records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-quality-document-control)
- [Server-Resolved Source Repository](https://github.com/duding-engicool/skill-quality-document-control)
- [File Numbering System](artifact/references/numbering-system.md)
- [File Change Management](artifact/references/change-management.md)
- [Quality-System Document Matrix](artifact/references/document-matrix.md)
- [Record Retention Policy](artifact/references/retention-policy.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown text with tables, checklists, templates, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Enterprise-specific missing information is marked for user completion rather than invented.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
