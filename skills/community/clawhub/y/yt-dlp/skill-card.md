## Description: <br>
A robust CLI wrapper for yt-dlp to download videos, playlists, and audio from YouTube and thousands of other sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to download or archive videos, playlists, channels, and audio with yt-dlp while applying quality, metadata, subtitle, thumbnail, and cookie options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-cookie use can expose an active session when used on an untrusted or shared machine. <br>
Mitigation: Use --cookies-from-browser only when authenticated access is intentional on a trusted machine; prefer a separate browser profile or a site-specific cookies file. <br>
Risk: Installing yt-dlp or ffmpeg from untrusted sources can introduce unsafe binaries or scripts. <br>
Mitigation: Install yt-dlp and ffmpeg from trusted package managers or official project sources, and run downloads in a dedicated folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1999AZZAR/yt-dlp) <br>
- [yt-dlp comprehensive usage guide](references/guide.md) <br>
- [yt-dlp usage reference](references/usage.md) <br>
- [yt-dlp latest release downloads](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands; downloaded media files are written by yt-dlp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp and ffmpeg on the host system; optional browser-cookie access can be passed through to yt-dlp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
