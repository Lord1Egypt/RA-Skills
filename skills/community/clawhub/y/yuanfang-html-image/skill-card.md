## Description:

Yuanfang HTML Image generates precise, multi-size social media images from text or URLs using HTML templates, extracted brand assets, selectable themes, and platform-specific dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyuanfang](https://clawhub.ai/user/iyuanfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content operators use this skill to turn article URLs, text, or content JSON into branded social media cover images and posters across multiple platform sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted content or URLs could cause the skill to run local commands.

Mitigation: Use trusted inputs, review commands before execution, and update the skill to use argument-array process execution before broad deployment.

Risk: URL fetching could reach internal network resources.

Mitigation: Avoid untrusted URLs and validate or limit allowed URL targets before installing the skill in sensitive environments.

Risk: Unescaped image or CSS values could affect rendered output or execution behavior.

Mitigation: Review generated content and require safe escaping for image and CSS values before using externally supplied assets.

Risk: Browser automation and cache behavior may be harder to audit without pinned dependencies and explicit cache controls.

Mitigation: Pin Playwright and related dependencies in a manifest and lockfile, and document cache refresh or clearing controls.

## Reference(s):

- [CLI Reference](references/cli.md)
- [Content Extraction API](references/extract-api.md)
- [Platform IDs](references/platforms.md)
- [Template Variables](references/template-vars.md)
- [Themes Catalog](references/themes-catalog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON content examples, and generated image files from HTML rendering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports multiple platform dimensions, theme selection, brand assets, badges, QR inputs, and preview output.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
