## Description: <br>
Community-maintained browser automation for QQ Music's web player (y.qq.com). Supports play/pause/next/prev, search songs/artists/albums, play liked songs, random play, like/unlike, playlist management, and browser-target discovery across platforms. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[ddd1988](https://clawhub.ai/user/ddd1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this community skill to control a logged-in QQ Music web-player session through local browser automation. It supports playback, search, liked songs, playlists, play mode, status checks, browser target discovery, and screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local DevTools connection can affect a logged-in QQ Music account. <br>
Mitigation: Use a dedicated browser profile for QQ Music and connect only to the local 127.0.0.1 DevTools endpoint. <br>
Risk: The tabs diagnostic can expose information about private or unrelated browser tabs. <br>
Mitigation: Avoid running diagnostics in a browser with private tabs open; prefer an isolated QQ Music profile. <br>
Risk: Screenshots are local file writes and may capture visible account or listening information. <br>
Mitigation: Write screenshots only to intended local paths and review them before sharing. <br>


## Reference(s): <br>
- [QQ Music Web Player](https://y.qq.com/) <br>
- [QQ Music Browser Control on ClawHub](https://clawhub.ai/ddd1988/qq-music-control) <br>
- [ddd1988 ClawHub Publisher Profile](https://clawhub.ai/user/ddd1988) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the controller emits JSON on stdout and can write PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, a Chromium-based browser with remote debugging enabled, and a local .cdp-port cache file for the DevTools port.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
