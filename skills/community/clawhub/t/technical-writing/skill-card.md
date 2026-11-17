## Description:

Technical Writing helps agents write, structure, and improve developer documentation, including READMEs, API documentation, ADRs, RFCs, changelogs, runbooks, diagrams, docs-as-code workflows, and code examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royhk920](https://clawhub.ai/user/royhk920)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to draft and improve developer-facing documentation such as READMEs, API references, ADRs, RFCs, changelogs, runbooks, and diagram-as-code guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready command examples may run remote installers, restart services, scale deployments, or alter production systems if reused without review.

Mitigation: Review, adapt, and test commands before use; replace remote installer pipelines with verified package or checksum-based install steps; require explicit approval, environment confirmation, impact, rollback, and post-check steps for runbooks.

Risk: Generated documentation can include incorrect or misleading guidance.

Mitigation: Subject generated documentation to human technical review and documentation CI, including linting, link checks, and tested code examples, before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/royhk920/skills/technical-writing)
- [Technical Writing Style Guide](artifact/references/writing-style-guide.md)
- [Mermaid Diagram Cheatsheet](artifact/references/mermaid-cheatsheet.md)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with prose, tables, templates, code blocks, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include copy-ready documentation templates and commands that require review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
