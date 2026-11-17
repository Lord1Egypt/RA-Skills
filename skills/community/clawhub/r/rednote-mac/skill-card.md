## Description:

Control the RedNote (Xiaohongshu) Mac app via macOS Accessibility API for workflows such as reading and replying to video comments, sending DMs, and getting author stats without browser automation or API tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangrh99](https://clawhub.ai/user/huangrh99)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to automate RedNote Mac workflows that require the native app, including navigation, feed browsing, comments, direct messages, and author profile stats. It is intended for supervised use on macOS with the RedNote app visible on screen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Accessibility-backed control of a live RedNote account and perform social actions such as DMs, comments, deletes, likes, collects, and follows.

Mitigation: Use a dedicated macOS user or test account, keep the app supervised, and require human confirmation before DM, comment, delete, follow, like, or collect actions.

Risk: Screenshots and OCR workflows can expose private RedNote UI content, including direct messages or private conversations.

Mitigation: Avoid screenshot or OCR analysis on private conversations unless necessary, and keep unrelated sensitive windows out of view.

Risk: The skill received a Review verdict because it can take live social-account actions and capture private UI content with limited built-in confirmation or scoping.

Mitigation: Install only when the user accepts this risk, supervise runs, and follow the scanner guidance for account isolation and action confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huangrh99/skills/rednote-mac)
- [README](README.md)
- [Navigation & Search](docs/ref-navigation.md)
- [Feed Browsing & Note Opening](docs/ref-feed.md)
- [Note Interactions](docs/ref-note.md)
- [Direct Messages](docs/ref-dm.md)
- [Profile & Author Stats](docs/ref-profile.md)
- [Known Limitations & Workarounds](docs/ref-limits.md)
- [RedNote](https://www.rednote.app)
- [cliclick](https://github.com/BlueM/cliclick)
- [uv](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [Text, JSON, Screenshots, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline tool calls; tool results may include screenshots, short URLs, comment metadata, and profile stats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, the RedNote app, Terminal Accessibility permission, cliclick, and python3.]

## Skill Version(s):

1.3.7 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
