## Description:

Social media cover image generator. Generates HTML pages based on title content and automatically converts them to PNG images, suitable for creating cover images and graphics for platforms such as Xiaohongshu, WeChat Official Accounts, Weibo, Douyin, Bilibili, Zhihu, Twitter/X, Instagram, and LinkedIn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to create platform-sized social media cover images from a title and convert the generated HTML design into a PNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion workflow renders active HTML in a headless browser.

Mitigation: Run the skill only in an isolated workspace or container and avoid rendering untrusted HTML.

Risk: The HTML template loads snapdom from an unpinned remote URL.

Mitigation: Vendor or pin snapdom locally before deployment and block unexpected network requests during rendering.

Risk: The browser launch configuration disables Chromium sandbox protections.

Mitigation: Prefer a reviewed version that removes sandbox-disabling flags or run it inside an additional container sandbox.

Risk: Dependencies are not locked in the artifact.

Mitigation: Pin dependencies with a lockfile and review dependency updates before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/openlark/skills/social-media-cover-generator)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)
- [snapdom browser renderer](https://unpkg.com/@zumer/snapdom/dist/snapdom.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with HTML, CSS, shell commands, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces HTML cover designs and PNG image files sized for selected social media platforms.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
