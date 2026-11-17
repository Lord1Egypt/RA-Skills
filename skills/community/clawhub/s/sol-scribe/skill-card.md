## Description:

Book writing companion for long-form creative projects, including chapter planning, narrative consistency, and AI-assisted drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

External writers use Solscribe to organize long-form book projects, manage chapter drafts, track word counts and statuses, and export manuscript drafts while keeping chapter content local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unauthenticated localhost server can allow any local process to read or modify manuscript data through localhost:3847.

Mitigation: Review before installing and do not run server.py unless that local access model is acceptable; keep the server stopped when not needed.

Risk: Session logs and backups may contain sensitive manuscript content.

Mitigation: Treat chapter, backup, and session log directories as sensitive local files and avoid sharing or syncing them unintentionally.

Risk: The backup system should not be treated as a perfect undo or permanent recovery mechanism.

Mitigation: Keep independent backups of important manuscript drafts and verify restore procedures before relying on the built-in backups.

## Reference(s):

- [Solscribe ClawHub skill page](https://clawhub.ai/amrree/skills/sol-scribe)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Plain text and Markdown responses; local Markdown chapter files and optional DOCX export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes manuscript state, backups, session logs, chapter Markdown, and exported DOCX files on the local filesystem.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
