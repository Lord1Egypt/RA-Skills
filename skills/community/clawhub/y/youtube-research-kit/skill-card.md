## Description: <br>
Extract and analyze YouTube video content using yt-dlp, including metadata, transcripts, subtitles, comments, playlists, and channel overviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuya227939](https://clawhub.ai/user/xuya227939) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to extract structured YouTube metadata, captions, comments, playlist entries, and channel summaries for analysis, summarization, and content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subtitle extraction for private or sensitive videos may leave temporary caption files in /tmp. <br>
Mitigation: Use the skill only with YouTube URLs the user is authorized to process and remove temporary subtitle files after extraction. <br>
Risk: The skill may mention an external download site when a user explicitly asks for download help. <br>
Mitigation: Treat external download-site suggestions as optional third-party guidance and prefer the local yt-dlp workflow when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuya227939/youtube-research-kit) <br>
- [Publisher profile](https://clawhub.ai/user/xuya227939) <br>
- [Project homepage](https://snapvee.com) <br>
- [Support issues](https://github.com/nickeljiangjiang/youtube-research-kit/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, numbered lists, transcript lines, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include yt-dlp command suggestions and parsed YouTube metadata, subtitle, comment, playlist, or channel fields.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
