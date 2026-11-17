## Description:

微信读书 AI 阅读助手支持扫码登录、阅读进度跟踪、章节内容存档、AI 对话以及标注和笔记拉取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[colorlessboy](https://clawhub.ai/user/colorlessboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate WeRead login, list books, extract reading progress, archive chapter content, screenshots, notes, and chat records, and discuss current reading context with an AI assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable WeRead login cookies are stored locally and can grant account access if exposed.

Mitigation: Treat profile/weread-cookies.json like a password and avoid storing it in shared, synced, backed-up, or source-controlled workspaces.

Risk: The skill writes private reading exports, screenshots, notes, metadata, and chat records to local folders.

Mitigation: Keep books/, output/, screenshots, notes, metadata, and chat files private and review them before sharing or committing workspace contents.

Risk: QR-code download during login uses a shell command and was flagged by ClawScan as risky for higher-risk environments.

Mitigation: Review the login workflow before installation and replace QR download with a shell-free, host-validated implementation before higher-risk use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colorlessboy/skills/weread-dl)
- [Playwright documentation](https://playwright.dev)
- [WeRead web application](https://weread.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-oriented guidance; generated local artifacts can include JSON metadata, Markdown notes and chat logs, chapter files, and screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Playwright, a browser session, and local storage for cookies and private reading exports.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
