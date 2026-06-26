## Description: <br>
Generates precise, multi-size social media images from text or URLs using HTML templates, extracted brand assets, and platform-specific layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyuanfang](https://clawhub.ai/user/iyuanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developer-agents use this skill to turn source text, URLs, or content JSON into branded social media covers and post images across multiple platform sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch user-provided URLs and referenced brand images. <br>
Mitigation: Use public URLs unless the user explicitly intends the agent to access and process private or authenticated content. <br>
Risk: Brand metadata and logo data may be saved in the local project cache. <br>
Mitigation: Review the .yuanfang cache before committing, copying, or sharing the project directory. <br>
Risk: Automatically extracted titles, body text, logos, colors, badges, or QR content can be incorrect for the intended publication. <br>
Mitigation: Confirm extracted content and visual choices with the user before rendering and review generated images before use. <br>


## Reference(s): <br>
- [CLI Reference](references/cli.md) <br>
- [Content Extraction API](references/extract-api.md) <br>
- [Platform Size Reference](references/platforms.md) <br>
- [Template Variables](references/template-vars.md) <br>
- [Theme Catalog](references/themes-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Images, HTML, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG image files with optional HTML previews and JSON content or brand specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multiple platform sizes, selectable visual themes, brand logo/color inputs, optional badge and QR content, and local project cache files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
