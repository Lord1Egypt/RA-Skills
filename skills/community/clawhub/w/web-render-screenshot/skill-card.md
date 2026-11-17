## Description:

Generate ultra-high-resolution PNG or JPEG screenshots from HTML files or URLs using Playwright headless Chromium.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to render readable screenshots of webpages, UI mockups, dashboards, data visualizations, and other text-heavy HTML content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can open arbitrary HTTP, HTTPS, and file URLs in Chromium.

Mitigation: Use the skill only with trusted HTML and trusted URLs, preferably in an isolated browser or container with network restrictions.

Risk: Rendering untrusted pages can expose private networks, local admin consoles, metadata services, or sensitive local files.

Mitigation: Review inputs before execution and avoid running the skill in environments with access to sensitive local files or internal services.

Risk: Browser and Playwright dependency behavior can change over time.

Mitigation: Pin Playwright dependencies when adopting the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/web-render-screenshot)
- [Publisher profile](https://clawhub.ai/user/wujiaming88)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for creating HTML and invoking the bundled screenshot script; the script writes PNG or JPEG image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
