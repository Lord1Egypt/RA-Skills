## Description: <br>
Fetch and read transcripts from YouTube videos. Use when you need to summarize a video, answer questions about its content, or extract information from it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naliehu](https://clawhub.ai/user/naliehu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to fetch YouTube transcripts, summarize video content, answer questions about a video, and extract transcript-based information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic triggers may activate this skill for broader video requests beyond YouTube transcript work. <br>
Mitigation: Use the skill only for YouTube transcript tasks and confirm the requested video workflow before relying on its output. <br>
Risk: The referenced get_transcript.py helper is not included in the package evidence. <br>
Mitigation: Verify any separately obtained transcript helper before use and ensure it matches the expected yt-dlp transcript workflow. <br>


## Reference(s): <br>
- [YouTube Watcher on ClawHub](https://clawhub.ai/naliehu/youtube-watcherkx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and transcript-derived text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp in PATH and depends on videos having closed captions or auto-generated subtitles.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
