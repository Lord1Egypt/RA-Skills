## Description:

Generate images from tables for better readability in messaging apps like Telegram. Use when displaying tabular data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joargp](https://clawhub.ai/user/joargp)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn Markdown tables into PNG images for messaging platforms that do not display Markdown tables well.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing tablesnap with @latest or a moving default branch can pull unreviewed dependency changes.

Mitigation: Install a pinned, reviewed tablesnap release or commit before using the skill.

Risk: Table content passed to the renderer may be written into image files intended for messaging platforms.

Mitigation: Only pass table content that is approved for rendering and sharing, and run the tool as an unprivileged user.

## Reference(s):

- [tablesnap repository](https://github.com/joargp/tablesnap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell commands and media output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for creating PNG table images, typically written to a local file such as /tmp/table.png.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
