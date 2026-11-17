## Description:

公众号排版器 converts article drafts into self-contained HTML that can be copied into the WeChat Official Account editor while preserving inline styles, with components tuned for music, nostalgia, and lifestyle posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkutitan](https://clawhub.ai/user/pkutitan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn WeChat Official Account drafts into styled, copy-ready HTML. It is best suited to music, nostalgia, and lifestyle posts, while general articles may need palette or component adjustments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated HTML filename may overwrite existing local work.

Mitigation: Choose or review the output filename before writing the generated HTML file.

Risk: Generated article text or styling may be unsuitable for publication if pasted without review.

Mitigation: Review the generated article content and formatting before pasting it into the WeChat Official Account editor.

Risk: The WeChat editor may strip unsupported CSS and degrade formatting.

Mitigation: Follow the bundled compatibility reference by using section and table containers, inline styles, and supported CSS properties.

## Reference(s):

- [WeChat MP Formatter ClawHub release](https://clawhub.ai/pkutitan/skills/wechat-mp-formatter)
- [WeChat Official Account CSS compatibility reference](references/compatibility.md)

## Skill Output:

**Output Type(s):** [Files, Code, Guidance]

**Output Format:** [Self-contained HTML file with inline styles plus brief Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local HTML file with a browser copy button for pasting formatted content into the WeChat Official Account editor.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
