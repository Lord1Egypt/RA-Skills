## Description: <br>
Download videos from YouTube, Bilibili, Twitter, and thousands of other sites using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatelei](https://clawhub.ai/user/fatelei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to prepare or run yt-dlp commands for downloading videos, extracting MP3 audio, downloading subtitles, selecting quality, and handling common download errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes browser-cookie access for some downloads, which can expose authenticated session data. <br>
Mitigation: Try cookie-free downloads first, require explicit user approval before any --cookies-from-browser use, and prefer a separate limited browser profile. <br>
Risk: Download commands write files to the local filesystem and can use broad shell and network permissions. <br>
Mitigation: Confirm the exact output directory before execution and use the narrowest available command workflow instead of blanket shell permissions. <br>
Risk: User-provided URLs are passed to a network downloader. <br>
Mitigation: Accept only http:// or https:// URLs, reject whitespace and unsupported shell metacharacters, and build commands as argument arrays. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fatelei/yt-dlp-download-skill) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [Cursor](https://cursor.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded media files through yt-dlp when commands are executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
