## Description:

Use when managing BangunAI Blog content, automating blog workflows, and writing MDX articles with BangunAI conventions. Supports Obsidian-like features (callouts, mermaid, LaTeX, wikilinks, backlinks, graph view).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwirx](https://clawhub.ai/user/dwirx)

### License/Terms of Use:


## Use Case:

Developers and authors use this skill to manage BangunAI Blog content, create MDX posts, maintain daily notes, update static pages, and follow the blog's frontmatter and component conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for one local blog path, and its file-writing examples can overwrite or delete local content without strong safeguards.

Mitigation: Install only when the agent should manage /home/hades/BangunAI-Blog; before allowing writes, deletes, commits, or pushes, require the agent to show the target path and diff.

Risk: User-provided filenames or categories could target unexpected paths if accepted without validation.

Mitigation: Reject filenames or categories containing slashes, dot-dot segments, or unexpected extensions before allowing filesystem actions.

## Reference(s):

- [BangunAI Blog Manager README](artifact/README.md)
- [BangunAI Blog Manager Integration Guide](artifact/INTEGRATION.md)
- [BangunAI Blog Manager Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MDX examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can propose content-file writes, page updates, deletions, git operations, and local blog workflow commands.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
