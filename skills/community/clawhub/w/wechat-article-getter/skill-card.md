## Description:

Extracts full text and metadata from WeChat Official Account article URLs using headless Chromium, with a mirror-search fallback when browser extraction is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppppanda](https://clawhub.ai/user/ppppanda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to read, summarize, analyze, or archive content from a shared mp.weixin.qq.com article link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned Playwright browser tooling and Python packages.

Mitigation: Preinstall reviewed and pinned dependencies through a controlled process, and avoid running setup as root or with sudo.

Risk: The skill renders caller-supplied URLs in a browser configuration that the security evidence identifies as unsafe.

Mitigation: Run the skill only in an isolated, unprivileged environment with outbound network restrictions.

Risk: URL and redirect validation is not fixed in the supplied security guidance.

Mitigation: Only pass exact https://mp.weixin.qq.com article URLs until URL and redirect validation are corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppppanda/skills/wechat-article-getter)
- [Publisher profile](https://clawhub.ai/user/ppppanda)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON by default, with optional Markdown or plain text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns title, author, publish time, article content, word count, source, URL, and error status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
