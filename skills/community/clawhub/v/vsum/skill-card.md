## Description: <br>
Vsum helps agents fetch subtitles from YouTube and Bilibili videos with yt-dlp and summarize them into Markdown using an AI provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chrischaan](https://clawhub.ai/user/Chrischaan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn a YouTube or Bilibili video link into a concise Markdown summary based on available subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bilibili workflow reads Chrome browser cookies through yt-dlp. <br>
Mitigation: Use a dedicated browser profile or a site-specific exported cookie file, and install only if that browser access is acceptable. <br>
Risk: Video subtitles and generated summaries may include private or sensitive content sent to the chosen AI provider. <br>
Mitigation: Avoid private videos or sensitive transcripts unless the AI provider is trusted for that data. <br>
Risk: The workflow depends on yt-dlp for subtitle retrieval. <br>
Mitigation: Verify yt-dlp comes from a trusted source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chrischaan/vsum) <br>
- [Publisher profile](https://clawhub.ai/user/Chrischaan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with shell command guidance and generated summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write subtitle files to the user's Downloads directory before AI summarization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
