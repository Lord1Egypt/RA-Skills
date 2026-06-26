## Description: <br>
Control YouTube Music with natural language to play, pause, skip, search, manage playlists, and queue tracks through browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oki3505F](https://clawhub.ai/user/oki3505F) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to control YouTube Music playback from an OpenClaw agent, including search, direct playback, queue actions, playlist actions, and volume controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted music queries, YouTube URLs, or video IDs may be passed into shell command strings by the command scripts. <br>
Mitigation: Review inputs before execution, use only trusted queries or video IDs, and prefer a patched version that validates input and uses structured argument calls. <br>
Risk: The skill can act through a logged-in YouTube or Google browser session. <br>
Mitigation: Run it in an isolated browser profile and review commands before actions that affect playback, playlists, likes, or account state. <br>
Risk: The skill stores local playback cache data. <br>
Mitigation: Document cache behavior for users and clear local cache files when the skill is removed or when shared machines are used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oki3505F/youtube-music-ultra) <br>
- [Publisher profile](https://clawhub.ai/user/oki3505F) <br>
- [YouTube Music](https://music.youtube.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open YouTube Music in an OpenClaw browser session, use a Node.js runtime, and read or write local playback cache files.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and package.json; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
