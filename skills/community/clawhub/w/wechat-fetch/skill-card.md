## Description:

Fetches WeChat public-account articles with Lite and Playwright modes, including no-login public fetching, batch downloads, image downloads, and Markdown, HTML, JSON, or text output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyfan01](https://clawhub.ai/user/jackyfan01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to fetch one or many WeChat article URLs, save article content and images locally, and choose an output format suitable for reading, archiving, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and download many images.

Mitigation: Use trusted mp.weixin.qq.com URLs, prefer Lite mode when possible, and run with limited network and filesystem access.

Risk: The Playwright mode may store and reuse browser cookies and runs Chromium with weakened security settings.

Mitigation: Use a contained browser profile or sandboxed environment, avoid sensitive accounts, and review whether Cookie mode is necessary before use.

Risk: Generated HTML can contain content from fetched pages.

Mitigation: Avoid opening generated HTML from untrusted pages outside a contained or disposable browser environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackyfan01/skills/wechat-fetch)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated article files may be Markdown, HTML, JSON, or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write article files, downloaded images, and batch reports to local output directories.]

## Skill Version(s):

3.0.0 (source: frontmatter, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
