## Description:

Guides users through creating reusable, mobile-friendly HTML layout templates for WeChat public-account articles, using industry presets or custom styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weikion](https://clawhub.ai/user/weikion)

### License/Terms of Use:

Apache 2.0

## Use Case:

WeChat public-account editors and content creators can use the skill to create reusable article layout templates. It offers seven industry styles or guided customization and leaves content placeholders for a later writing step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README's clone command uses a placeholder GitHub URL, so it does not identify a verified installation source.

Mitigation: Install from a verified release or source.

Risk: Generating a template can replace outputs/wechat-template.html.

Mitigation: Preserve any existing template before generating a new one.

Risk: Generated HTML and image URLs affect what readers see when an article is published; populated content from downstream writing skills is outside this review.

Mitigation: Review the finished HTML and image URLs, and review populated article content before publishing.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/weikion/wechat-template-creator)
- [ClawHub release](https://clawhub.ai/weikion/skills/wechat-template-creator)
- [WeChat HTML specification](references/wechat-html-spec.md)
- [Custom layout configuration guide](references/custom-config.md)

## Skill Output:

**Output Type(s):** [HTML, Files, Guidance]

**Output Format:** [Reusable inline-styled HTML template with content placeholders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves placeholders for a downstream article-writing step.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
