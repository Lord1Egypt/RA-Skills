## Description:

Distills books, papers, or theses into per-concept cheatsheet folders with an index, using source normalization, structure mapping, fan-out drafting, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whit3rabbit](https://clawhub.ai/user/whit3rabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and researchers use this skill to convert long-form source material into concise, source-mapped Markdown notes organized by concept rather than chapter. It supports distilling new sources, extending existing notes, and verifying generated note sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a hook that can rewrite Git commit or pull request commands if registered.

Mitigation: Review or remove the bundled hook before installation, and enable it only when Git or PR message rewriting is an intended behavior.

Risk: Optional model-assisted fixing can send flagged passages to a configured remote endpoint.

Mitigation: Use local-only operation unless a trusted endpoint is explicitly configured through the documented environment variables or adjacent model configuration.

Risk: Source documents may contain concealed instructions or prompt-injection text that later fan-out agents read as data.

Mitigation: Run the bundled scan before fan-out, treat source text as evidence rather than instructions, and stop on injection findings for human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whit3rabbit/skills/rabbit-reads)
- [Security notes](SECURITY.md)
- [Fan-out prompt](references/fanout-prompt.md)
- [Non-fiction book type](references/book-types/non-fiction.md)
- [Fiction book type](references/book-types/fiction.md)
- [Arxiv paper book type](references/book-types/arxiv-paper.md)
- [Thesis book type](references/book-types/thesis.md)
- [Cheatsheets layout](references/layouts/cheatsheets.md)
- [Obsidian layout](references/layouts/obsidian.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes and README or index files, with shell commands and concise guidance during workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a concept-oriented notes folder and verification findings; optional model-assisted fixes require an explicitly configured endpoint.]

## Skill Version(s):

0.5.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
