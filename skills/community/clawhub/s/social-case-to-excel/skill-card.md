## Description:

Organizes sourced social media cases into an illustrated Excel library and research documents with methods, outcome evidence, and practical applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingling1989r](https://clawhub.ai/user/lingling1989r)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing researchers and brand teams use this skill to turn social posts and comments into traceable case studies, method breakdowns, and illustrated reports for campaign reviews and audience insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook and QA builders can execute matching Python files from shared /tmp paths.

Mitigation: Review scripts before running them; use a private per-run working directory and explicit reviewed file lists or JSON inputs instead of /tmp wildcards, and avoid shared machines.

Risk: ClaudeBaby credentials could appear in generated reports.

Mitigation: Keep tokens in the configured MCP store or environment, and check reports for credential leakage before sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lingling1989r/skills/social-case-to-excel)
- [Research workflow](references/pipeline.md)
- [Workbook schema](references/schema.md)
- [Comment insight mode](references/comment-insight-mode.md)

## Skill Output:

**Output Type(s):** [Spreadsheet files, Markdown, HTML]

**Output Format:** [Multi-sheet XLSX workbook and illustrated Markdown document; optional HTML document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source links, evidence limitations, methods, and matched post images when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
