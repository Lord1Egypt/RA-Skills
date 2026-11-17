## Description:

Exports all X/Twitter bookmarks into individual Markdown files with metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn locally captured X/Twitter bookmark API responses into organized Markdown files for note-taking systems such as Obsidian or Notion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The input bookmarks.json and generated Markdown files may contain private bookmark content.

Mitigation: Store the input and output in a private folder, avoid committing or syncing them unintentionally, and delete the raw captured JSON when it is no longer needed.

Risk: The skill depends on user-captured X/Twitter API responses from the browser Network tab, which may be incomplete or malformed.

Mitigation: Scroll through all bookmarks before copying responses and verify that output/bookmarks contains the expected exported files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/twitter-bookmarks-exporter)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [X bookmarks page](https://x.com/i/bookmarks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter and human-facing status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one Markdown file per exported bookmark under output/bookmarks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
