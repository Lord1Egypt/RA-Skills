## Description: <br>
Control the RedNote (Xiaohongshu) Mac app via macOS Accessibility API. Fills the gap headless tools can't: read/reply to comments on video posts, send DMs, get author stats. No browser, no API tokens. macOS only - requires Terminal accessibility permission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangrh99](https://clawhub.ai/user/huangrh99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent control the RedNote Mac app for feed navigation, search, likes, collections, comment workflows, direct messages, and profile statistics. It is intended for macOS environments where the RedNote app is visible and Terminal has Accessibility permission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live RedNote account and perform account actions such as sending direct messages, posting or replying to comments, following accounts, and deleting comments. <br>
Mitigation: Keep tool approval enabled and verify the visible target before allowing account-changing actions. <br>
Risk: Terminal Accessibility permission grants broad macOS UI control, not just RedNote control. <br>
Mitigation: Install only in a trusted environment and consider using a dedicated macOS and RedNote account for automation. <br>
Risk: Screenshots and clipboard interactions may expose sensitive on-screen or copied content. <br>
Mitigation: Treat screenshots and clipboard data as sensitive and avoid unattended runs. <br>
Risk: The skill depends on visible macOS UI state, so actions can target the wrong visible element if the app state is unexpected. <br>
Mitigation: Verify screenshots after navigation and before sending messages, posting comments, following accounts, or deleting comments. <br>


## Reference(s): <br>
- [RedNote](https://www.rednote.app) <br>
- [cliclick](https://github.com/BlueM/cliclick) <br>
- [uv](https://github.com/astral-sh/uv) <br>
- [Navigation & Search](artifact/docs/ref-navigation.md) <br>
- [Feed Browsing & Note Opening](artifact/docs/ref-feed.md) <br>
- [Note Interactions](artifact/docs/ref-note.md) <br>
- [Direct Messages](artifact/docs/ref-dm.md) <br>
- [Profile & Author Stats](artifact/docs/ref-profile.md) <br>
- [Known Limitations & Workarounds](artifact/docs/ref-limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with tool calls, JSON-like tool results, shell commands, and screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return screenshots, screen coordinates, short RedNote share URLs, comment metadata, and profile statistics.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
