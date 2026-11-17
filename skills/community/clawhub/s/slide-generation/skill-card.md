## Description:

Generate Marp teaching slides from one or more source Markdown files, including course decks with AM Blue Course theming, presenter metadata, image handling, and unified synthesis across sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hh23333](https://clawhub.ai/user/hh23333)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, course authors, and presentation builders use this skill to convert source Markdown notes or folders into Marp-compatible teaching slide decks. It is intended for source-grounded deck synthesis with required theme, cover, table-of-contents, image-copying, and layout rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendered slides may contact external font or CSS providers through Marp theme assets.

Mitigation: Vendor remote CSS and font assets locally or disable outbound network access during rendering in sensitive or offline environments.

Risk: Generated decks can be incomplete or misleading if source files are missing, stale, or internally inconsistent.

Mitigation: Review the generated slide deck against the source Markdown, including table-of-contents links, copied images, section structure, and required Marp headers before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hh23333/skills/slide-generation)
- [Slide Generation Rules](artifact/references/rules.md)
- [Marp Guide](artifact/references/marp-guide.md)
- [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
- [Awesome Marp Template](https://github.com/favourhong/Awesome-Marp)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Marp-compatible Markdown slide deck with YAML front matter, Marp class comments, and local image references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is constrained to user-provided source material; source images are copied and relinked into an output images/ folder.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
