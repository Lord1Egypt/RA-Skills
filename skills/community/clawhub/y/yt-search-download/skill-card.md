## Description: <br>
Helps agents search YouTube videos and channels, inspect video metadata, and run yt-dlp workflows for video, audio, and subtitle downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joppyao-bit](https://clawhub.ai/user/joppyao-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill in Claude Code or OpenClaw to search video metadata, browse channels, download selected media, extract audio, and obtain subtitle files for review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: yt-dlp download workflows may use local browser login cookies. <br>
Mitigation: Prefer unauthenticated downloads and require explicit user approval before any browser-cookie use. <br>
Risk: Downloads can write media, audio, and subtitle files to local directories. <br>
Mitigation: Confirm the output directory before running download commands, especially when using custom paths. <br>
Risk: Publisher claims for Bilibili and subtitle support may exceed the implemented behavior. <br>
Mitigation: Treat those capabilities as limited unless the publisher supplies updated implementation evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joppyao-bit/yt-search-download) <br>
- [Publisher profile](https://clawhub.ai/user/joppyao-bit) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [YouTube Data API v3 endpoint](https://www.googleapis.com/youtube/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown tables, JSON search results, shell commands, and downloaded media or subtitle files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YouTube API key for search and yt-dlp for download workflows; downloads normally write to ~/Downloads or a user-selected directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
