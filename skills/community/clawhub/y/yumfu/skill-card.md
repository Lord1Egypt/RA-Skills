## Description: <br>
Yumfu is a chat-native multiplayer text RPG that lets agents run persistent adventures across multiple worlds with natural-language turns, generated scene art, voice narration, and storybook exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumyumtum](https://clawhub.ai/user/yumyumtum) <br>

### License/Terms of Use: <br>
GPL-3.0-or-later <br>


## Use Case: <br>
External users and chat communities use Yumfu to run solo or multiplayer role-playing sessions in group chat, with persistent saves, natural-language actions, generated media, and optional storybook exports. Agents use the skill to manage gameplay turns, character creation, save/load flows, and content delivery for ongoing campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad chat triggers can continue gameplay in group chats when a participant sends natural-language game actions. <br>
Mitigation: Use an explicit /yumfu session boundary in group chats and make clear when Yumfu is active. <br>
Risk: Persistent saves, generated media, and default-on storybook logs may retain gameplay conversation content locally. <br>
Mitigation: Warn participants before group play, disable storybook tracking when privacy matters, or set YUMFU_NO_LOGGING=1. <br>
Risk: Optional daily evolution can send scheduled background updates after setup. <br>
Mitigation: Enable daily evolution only for users who want scheduled updates and review the target chat before enabling it. <br>
Risk: Generated art and voice narration may expose private or unwanted story content in shared chat surfaces. <br>
Mitigation: Confirm group expectations for images and TTS, and turn those features off per save when the session should remain text-only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yumyumtum/yumfu) <br>
- [Publisher profile](https://clawhub.ai/user/yumyumtum) <br>
- [GitHub repository](https://github.com/yumyumtum/yumfu) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Storybook System](STORYBOOK_SYSTEM.md) <br>
- [Release Notes v1.7.11](RELEASE_NOTES_v1.7.11.md) <br>
- [Canon Reference File Guide](worlds/canon/README.md) <br>
- [Storybook demos](https://yumyumtum.github.io/yumfu/storybooks/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and chat text, with optional JSON helper results, shell command snippets, generated media paths, and HTML storybook files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local saves, session logs, generated media, and storybook exports; optional daily evolution can produce scheduled background messages when enabled.] <br>

## Skill Version(s): <br>
1.7.11 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
