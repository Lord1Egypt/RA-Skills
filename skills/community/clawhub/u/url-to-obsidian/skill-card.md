## Description:

Url To Obsidian fetches user-provided web pages, cleans and formats the content, and saves it as Obsidian Markdown notes with source metadata, optional Simplified Chinese translation, and multi-page handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufengsheng](https://clawhub.ai/user/wufengsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and Obsidian users use this skill to archive technical documentation, blog posts, GitHub README pages, and index-style documentation into structured Obsidian notes while preserving source links, commands, and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided URLs through available web tools, which can expose confidential or login-only content to the selected fetch backend.

Mitigation: Use it only on pages appropriate for the active fetch backend, and avoid confidential or login-only pages unless that backend is understood and approved.

Risk: The skill writes Markdown files into an Obsidian vault, so an incorrect destination or conflict choice can affect local notes.

Mitigation: Review the proposed note name, destination, and conflict action before saving, and inspect the generated note after write validation.

Risk: Saved web pages may contain command examples that are copied into notes.

Mitigation: Review commands from generated notes before running them.

## Reference(s):

- [Obsidian note template reference](artifact/references/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with YAML frontmatter, Obsidian callouts, source links, tags, and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save a single page, merge selected subpages into one note, or create multiple notes; preserves code blocks, command examples, package names, and URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
