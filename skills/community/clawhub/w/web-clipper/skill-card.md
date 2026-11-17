## Description:

Save any web page as an Obsidian-compatible Markdown clipping using Jina Reader API for clean content extraction, with support for tags, subfolders, and vault paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatgptnexus](https://clawhub.ai/user/chatgptnexus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to clip public web pages into clean Markdown notes for Obsidian-style knowledge bases, including source metadata and optional tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic execution from vague chat context can run local commands sooner than the user expects.

Mitigation: Review before installing and require explicit confirmation of the exact URL and destination before execution.

Risk: The skill sends requested page URLs to Jina Reader and may expose URLs or page access patterns to that external service.

Mitigation: Use it only for public URLs you are comfortable sending to Jina Reader.

Risk: User-controlled vault, folder, or URL values can affect local file writes.

Mitigation: Avoid untrusted destination values until shell-safe execution and vault path containment are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chatgptnexus/skills/web-clipper)
- [Jina AI](https://jina.ai)
- [Jina API Key](https://jina.ai/?sui=apikey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes clipped Markdown files to a configured Obsidian-style vault folder.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
