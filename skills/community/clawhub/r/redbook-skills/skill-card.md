## Description:

将图文/视频内容自动发布到小红书（XHS），并支持登录检查、内容检索与互动操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to prepare, preview, publish, search, and interact with Xiaohongshu content through a Chrome-based automation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Xiaohongshu browser session and can publish, comment, like, bookmark, or collect account-related content data.

Mitigation: Use a dedicated test account and isolated Chrome profile, require human confirmation before publishing or interaction actions, and review results after execution.

Risk: Remote CDP access can expose or modify an authenticated browser session if pointed at an untrusted host.

Mitigation: Prefer local CDP, connect only to hosts you control, and avoid sharing debugging ports outside a trusted environment.

Risk: URL-based media handling and account/profile options can create unsafe local or network behavior.

Mitigation: Use trusted media URLs or local files, avoid account names containing path characters, and keep Chrome profiles isolated from personal browsing data.

Risk: The artifact includes avoid-detection guidance and browser selectors that may be brittle as Xiaohongshu changes.

Mitigation: Review or patch avoid-detection guidance before production use, and revalidate selectors, upload waits, and publish-button handling after site changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/redbook-skills)
- [README.md](artifact/README.md)
- [Claude Code integration guide](artifact/docs/claude-code-integration.md)
- [Quick start guide](artifact/快速上手指南.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON-like command results, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate drafts, tags, content calendars, browser automation commands, and structured summaries of Xiaohongshu content or account state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
