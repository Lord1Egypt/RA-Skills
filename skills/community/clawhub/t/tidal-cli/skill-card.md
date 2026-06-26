## Description: <br>
Control Tidal music streaming from the terminal for catalog search, playlist management, library updates, playback, recommendations, and user profile lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucaperret](https://clawhub.ai/user/lucaperret) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate Tidal from a terminal, including searching catalog content, managing playlists and favorites, playing tracks, and retrieving recommendations or account profile details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change a user's Tidal account, including playlist and library items. <br>
Mitigation: Ask for confirmation before deleting, renaming, adding, or removing playlist or library items. <br>
Risk: The Tidal session is stored at ~/.tidal-cli/session.json and may expose account access on shared or untrusted devices. <br>
Mitigation: Protect or remove ~/.tidal-cli/session.json on shared or untrusted devices. <br>
Risk: The skill depends on an external npm package to perform Tidal operations. <br>
Mitigation: Install only if the publisher and external npm package are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lucaperret/tidal-cli) <br>
- [Publisher profile](https://clawhub.ai/user/lucaperret) <br>
- [npm package: @lucaperret/tidal-cli](https://www.npmjs.com/package/@lucaperret/tidal-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline tidal-cli commands and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses tidal-cli --json for programmatic command output when available.] <br>

## Skill Version(s): <br>
1.2.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
