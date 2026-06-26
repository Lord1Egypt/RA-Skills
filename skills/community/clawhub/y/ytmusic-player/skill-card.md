## Description: <br>
Operates YouTube Music through natural language to search music, browse library content, manage playlists, inspect lyrics and account information, and control playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadaliao](https://clawhub.ai/user/kadaliao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate YouTube Music from chat, including search, playback, playlist management, lyrics lookup, library browsing, ratings, and account inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles YouTube Music cookies and local session files that can act like login credentials. <br>
Mitigation: Use only on trusted machines, avoid sharing cookies in persistent or shared chat contexts, and remove .ytmusic/auth.json and .ytmusic/playwright-profile when access is no longer needed. <br>
Risk: Authenticated commands can change account state, including playlist edits, ratings, history removal, uploads, and deletes. <br>
Mitigation: Review and confirm account-changing or destructive actions before execution, especially target playlist, upload, history, and rating identifiers. <br>
Risk: Playback depends on a persistent local Playwright browser profile and daemon. <br>
Mitigation: Stop the daemon after use and protect the local profile directory because it may retain signed-in session state. <br>


## Reference(s): <br>
- [YouTube Music Command Reference](references/commands.md) <br>
- [Project homepage](https://github.com/kadaliao/ytmusic-skill) <br>
- [ClawHub release page](https://clawhub.ai/kadaliao/ytmusic-player) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, plain text lyrics, JSON command results, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local Playwright browser daemon and store YouTube Music session state under .ytmusic/.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
