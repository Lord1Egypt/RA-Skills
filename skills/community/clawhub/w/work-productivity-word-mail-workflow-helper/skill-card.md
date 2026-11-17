## Description:

Builds and troubleshoots Microsoft Word mail merge and DOCX template workflows using merge fields, content controls, document properties, repeated sections, data sources, and formatting-preserving generation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Administrative teams, legal operations, HR teams, and developers use this skill to plan, implement, and validate Word mail merge and DOCX template assembly workflows without breaking formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may cause the skill to activate for nearby productivity tasks where Word or DOCX mail merge guidance was not intended.

Mitigation: Narrow or disable implicit invocation when deployment policy requires explicit activation for Word, DOCX, or mail merge workflows.

Risk: Incorrect mappings, missing data, or formatting changes can affect generated legal, HR, operations, sales, or administrative documents.

Mitigation: Validate generated documents for field completion, formatting, page count, section breaks, table rows, filenames, and required PDF export before distribution.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-word-mail-workflow-helper)
- [Word Template and XML Data Source Merge](https://segmentfault.com/a/1190000023933964)
- [Aspose Words DOCX Merge](https://segmentfault.com/a/1190000042001412)
- [SAP CRM Word Template](https://segmentfault.com/a/1190000023893454)
- [PHPWord Template Usage](https://segmentfault.com/a/1190000022674686)
- [Python DOCX Text Extraction](https://segmentfault.com/q/1010000042819314)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with mappings, workflows, checklists, and inline code or commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include notes about Word desktop field updates, PDF export, data normalization, and batch validation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
