## Description:

Generates structured weekly work reports from Git commit history and file-change statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeee886](https://clawhub.ai/user/zoeee886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to generate weekly, daily, or sprint Markdown progress reports from Git history, file-change statistics, and optional author filters. It can also summarize recent file modifications when a folder is not a Git repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include author names, commit messages, dates, and changed-file details from repository history.

Mitigation: Review generated reports before sharing them and narrow the repository path, time range, or author filter when sensitive history should be excluded.

Risk: Markdown generated from untrusted repository history may include unsafe raw HTML or remote image references when viewed in permissive renderers.

Mitigation: Use a Markdown viewer that disables raw HTML and remote images when processing commits from untrusted contributors.

Risk: The bundled PowerShell helper reads Git history and writes a Markdown report to the selected output path.

Mitigation: Inspect the command parameters before execution and choose an intended repository and output location.

## Reference(s):

- [Server-resolved source repository](https://github.com/zoeee886/clawhub-skills/tree/main/weekly-report)
- [ClawHub skill page](https://clawhub.ai/zoeee886/skills/weekly-report-2)
- [Weekly report examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional PowerShell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write weekly-report.md or a requested Markdown output path; commit details are kept to at most 50 rows.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
