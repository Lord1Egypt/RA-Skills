## Description: <br>
Control YouTube Music with natural language commands for playback, search, queue, playlist, and browser-based music controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oki3505F](https://clawhub.ai/user/oki3505F) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and end users use this skill to let an agent control YouTube Music through OpenClaw browser automation, including playing tracks, opening direct video IDs, searching, adjusting playback, and managing queue-oriented music workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-controlled music queries, URLs, or video IDs can reach shell-string execution paths. <br>
Mitigation: Review before installing and avoid untrusted inputs until the helpers use argument-array execution plus strict URL and video-ID validation. <br>
Risk: Browser automation can affect a signed-in YouTube Music session and perform playback or queue actions. <br>
Mitigation: Use a dedicated browser profile and require explicit confirmation for playlist, like, queue, and autoplay actions. <br>
Risk: Search and playback cache files under /tmp may expose listening queries or video identifiers. <br>
Mitigation: Clear the /tmp cache files when privacy matters and avoid sharing the browser profile or cache directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oki3505F/youtube-music) <br>
- [Publisher Profile](https://clawhub.ai/user/oki3505F) <br>
- [YouTube Music](https://music.youtube.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance with shell command snippets and browser-control commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an OpenClaw browser profile and may write local cache files under /tmp.] <br>

## Skill Version(s): <br>
3.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
