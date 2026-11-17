## Description:

Intelligent information triage system based on Tiago Forte's PARA method (Projects/Areas/Resources/Archive) for automatic categorization and priority scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to classify notes, tasks, links, and saved content into PARA categories, score urgency, detect related items, and export triage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports generated from untrusted notes may be unsafe to open in spreadsheet software if CSV escaping is not fixed.

Mitigation: Prefer JSON or Markdown exports for untrusted notes, or review and sanitize CSV content before opening it in spreadsheet software.

Risk: The skill primarily emits Chinese-language triage labels and recommendations.

Mitigation: Confirm that Chinese-language output is acceptable for the intended users before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, CSV, JavaScript examples, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include content type, PARA category, urgency score, tags, relatedness signals, and recommended actions.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter v1.0.0 and package.json 1.0.1 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
