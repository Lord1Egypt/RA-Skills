## Description: <br>
Manage YouTube Music library, playlists, and discovery via ytmusicapi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gentrycopsy](https://clawhub.ai/user/gentrycopsy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and YouTube Music users use this skill to configure ytmusicapi access and manage songs, albums, playlists, lyrics, and related music discovery through an authenticated YouTube Music account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local YouTube Music authentication files that should be treated like credentials. <br>
Mitigation: Keep browser.json private, delete headers.txt after setup, and do not commit either file to source control. <br>
Risk: Authenticated operations can change a user's YouTube Music library and playlists. <br>
Mitigation: Ask the agent to confirm before making playlist or library changes. <br>


## Reference(s): <br>
- [YouTube Music](https://music.youtube.com) <br>
- [ClawHub skill page](https://clawhub.ai/gentrycopsy/ytmusic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated YouTube Music library and playlist operations for user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
