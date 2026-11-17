## Description:

Generates Simplified Chinese Tibetan Buddhist product articles from local Markdown drafts, with web-verified product research and matching Tibetan-style PNG images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn Tibetan Buddhist product drafts into concise Simplified Chinese articles with researched background, product details, cultural usage, and supporting images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafts and product details may be used during web verification or image prompting.

Mitigation: Avoid unpublished or sensitive drafts unless network and tool use are controlled.

Risk: The --output-dir option can place generated files outside the default processing folder.

Mitigation: Review custom output paths before running and keep generated files in a scoped workspace.

Risk: Generated religious, cultural, or product claims may remain incomplete when research or image generation fails.

Mitigation: Review the article, warnings, logs, and cited research before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/tibetan-buddhist-product-article-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [markdown, images, json, text]

**Output Format:** [Markdown article with PNG image files, optional JSON run metadata, and text warning or log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs use timestamp-based filenames and are written to the default Tibetan processing workspace or a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
