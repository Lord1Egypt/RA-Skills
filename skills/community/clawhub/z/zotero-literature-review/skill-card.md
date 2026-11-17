## Description:

Zotero Literature Review helps agents create structured academic literature reviews by searching Zotero libraries, validating PDFs, extracting source-grounded details, and producing review drafts with quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sun2001](https://clawhub.ai/user/sun2001)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical teams with Zotero collections use this skill to produce source-grounded literature reviews, related-work sections, and technical survey drafts from verified local PDFs and optional web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive research materials because it directs the agent to read local Zotero libraries, PDFs, tags, metadata, and generated temporary files.

Mitigation: Scope tasks to a specific Zotero collection or folder, use local-only mode when external search is unnecessary, and review selected files before execution.

Risk: Extracted-text intermediates and generated reports may retain confidential PDF content or metadata.

Mitigation: Store outputs in project-specific folders, review generated files before sharing, and delete temporary extraction files after the task is complete.

Risk: Optional online search may send research topics or query terms to external search tools.

Mitigation: Use local Zotero-only mode for sensitive topics or remove confidential terms before enabling web search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sun2001/skills/zotero-literature-review)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Usage examples](artifact/应用示例.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and document-oriented files with supporting reports, project indexes, extracted citation details, and task guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified citation metadata, extracted PDF details, quality-check summaries, and explicit markers for information that cannot be validated.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
