## Description:

Search, preview, download, and process GIFs from Tenor and Giphy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search GIF providers, retrieve GIF URLs, download GIF files, and create derived image outputs such as static frames or frame sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries to external GIF services such as Tenor or Giphy.

Mitigation: Use only queries appropriate for those services and provide only the provider API key needed for the selected provider.

Risk: The skill can write downloaded or generated media files to caller-selected output paths.

Mitigation: Use explicit workspace-scoped output paths and review generated files before reusing or distributing them.

Risk: The skill depends on a third-party local gifgrep CLI.

Mitigation: Install only a reviewed gifgrep version, and prefer a pinned version when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terrycarter1985-gifgrep)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, shell command guidance, and file path parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return GIF URLs, downloaded GIF files, extracted image frames, or generated frame sheets through the gifgrep CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
