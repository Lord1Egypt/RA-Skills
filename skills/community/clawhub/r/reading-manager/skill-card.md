## Description:

Personal reading management system for tracking books, articles, reading progress, notes, and generating reading reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Reading Manager to track personal libraries, articles, reading progress, notes, lists, goals, and reports through a local command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent local SQLite database under ~/.config/reading-manager that may contain reading history, notes, URLs, and other personal records.

Mitigation: Use it on trusted machines, avoid storing sensitive notes on shared systems, and review exported data before sharing it.

Risk: ISBN and search commands can send book identifiers or search terms to Google Books for metadata lookup.

Mitigation: Use manual entry instead of online lookup for private reading material or when external queries are not acceptable.

Risk: The included test-publish.sh script invokes a ClawHub publish command.

Mitigation: Run publish scripts only when intentionally releasing the package and after confirming account, slug, and version settings.

## Reference(s):

- [Reading Manager ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/reading-manager)
- [Google Books API Volumes Endpoint](https://www.googleapis.com/books/v1/volumes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands and structured reading-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create and update local SQLite reading data and export notes or reports when the user runs the generated commands.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
