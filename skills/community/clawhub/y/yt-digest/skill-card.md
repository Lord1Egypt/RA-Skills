## Description: <br>
Extracts transcripts, summary previews, chapters, and key moments from public YouTube videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRaini](https://clawhub.ai/user/0xRaini) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to inspect public YouTube videos by retrieving transcripts, extracting chapters or key moments, and producing concise command-line analysis without a YouTube API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs yt-dlp locally on video URLs supplied by the user. <br>
Mitigation: Install only when local yt-dlp execution is expected, keep yt-dlp updated, and use reviewed versions that avoid shell-based URL handling. <br>
Risk: Transcript and chapter output depends on public video metadata, subtitles, and yt-dlp availability. <br>
Mitigation: Review generated summaries or key moments before relying on them and expect failures for videos without accessible subtitles or metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRaini/yt-digest) <br>
- [Publisher profile](https://clawhub.ai/user/0xRaini) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Command-line text with Markdown-style headings, timestamped transcript lines, and bullet lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript commands may be limited by character count; summary and analysis commands include transcript previews and derived chapter lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
