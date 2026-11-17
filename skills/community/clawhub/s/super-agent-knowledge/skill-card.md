## Description:

Super Agent Knowledge helps agents capture, organize, search, validate, and maintain reusable knowledge from URLs, media extracts, social posts, papers, and research notes as structured markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to preserve useful source material and research outputs in a searchable local knowledge base. It is suited for workflows that need quick capture, tag-based retrieval, validation, cleanup, and QMD indexing of markdown knowledge entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install and run an unpinned separate knowledge package.

Mitigation: Review the actual knowledge package and scripts/know implementation before installing or using it in automated workflows.

Risk: Recurring tidy or auto-fix runs can change files in the configured knowledge directory.

Mitigation: Keep KNOWLEDGE_DIR scoped to a dedicated knowledge folder, run maintenance in audit or dry-run mode first if available, and avoid scheduled auto-fix until provenance and backup behavior are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-agent-knowledge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML frontmatter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local markdown knowledge entries and an auto-maintained index when used with the referenced command-line tool.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
