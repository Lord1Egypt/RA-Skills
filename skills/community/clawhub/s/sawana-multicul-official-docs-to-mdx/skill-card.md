## Description:

Download and normalize official documentation pages into local .mdx files at user-specified paths using markdown.new.

This skill is ready for commercial/non-commercial use.

## Publisher:

[multicul-silver-wolf](https://clawhub.ai/user/multicul-silver-wolf)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to fetch official documentation from a URL, convert it into cleaned local MDX, and maintain reproducible docs snapshots for local knowledge bases, RAG preparation, or project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided documentation URLs are sent to markdown.new, a third-party conversion service.

Mitigation: Use public official documentation URLs only; avoid private, internal, tokenized, or otherwise sensitive URLs.

Risk: Converted MDX is written to user-specified paths and may overwrite existing workspace files.

Mitigation: Choose output paths deliberately, check for existing files before running, and review generated MDX before compiling or publishing it.

Risk: Converted documentation content is untrusted input from an upstream web page.

Mitigation: Review the generated MDX for unsafe or misleading content before adding it to documentation, RAG, or publishing workflows.

## Reference(s):

- [mdnew_to_mdx.sh reference](references/mdnew_to_mdx.md)
- [markdown.new](https://markdown.new)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [MDX files with YAML frontmatter and concise Markdown status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated MDX includes title, description, sourceUrl, and retrievedAt frontmatter; output files may be overwritten.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
