## Description:

Generates structured Excel QA test cases from Markdown, PDF, Word, or image-based requirement artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, product teams, and developers use this skill to convert PRDs, API documents, UI flows, and batch requirement sets into business-domain grouped test cases and formatted Excel workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets may preserve unsafe formulas from input text.

Mitigation: Open generated spreadsheets with external links and active content disabled until formula sanitization is added.

Risk: Requirement documents from untrusted sources may expose the workflow to unsafe or unintended file content.

Mitigation: Use a virtual environment with pinned dependencies and invoke the skill only on intended files.

Risk: Generated test cases can miss requirements or contain misleading coverage assumptions.

Mitigation: Review generated cases against the source requirements before using them for QA planning or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kokxi/skills/qa-testcase-generator)
- [README](artifact/README.md)
- [Schema Reference](artifact/references/schemas.md)
- [Quality Reference](artifact/references/quality.md)
- [Design Methods Reference](artifact/references/design_methods.md)
- [Image Analysis Reference](artifact/references/image_analysis.md)
- [Troubleshooting Reference](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance, JSON test case data, and formatted Excel workbooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excel output includes priority coloring and module separator rows; batch workflows preserve source file labels.]

## Skill Version(s):

2.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
