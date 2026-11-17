## Description:

Generates PNG cover images, posters, and social-media graphics from a user-supplied topic by filling HTML templates and rendering them locally with Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoyuhyy](https://clawhub.ai/user/luoyuhyy)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate local PNG image assets for covers, posters, social posts, greetings, horoscope content, and other promotional or visual materials without a paid image-generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text may be rendered into local HTML templates.

Mitigation: Escape HTML-sensitive characters, set content length limits, and avoid untrusted raw HTML input before rendering.

Risk: Browser rendering can load or execute active content if templates or inputs are expanded unsafely.

Mitigation: Render with JavaScript disabled where practical and block network requests when processing arbitrary third-party content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoyuhyy/skills/xhs-html-cover)
- [Publisher profile](https://clawhub.ai/user/luoyuhyy)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML template variables and Playwright screenshot commands that produce PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated image assets are PNG files; artifact documentation describes 1x1, 4x5, 9x16, 16x9, and 4x3 sizes.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
