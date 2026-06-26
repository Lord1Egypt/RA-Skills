## Description: <br>
Fetch and read transcripts from YouTube videos. Use when you need to summarize a video, answer questions about its content, or extract information from it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Michaelgathara](https://clawhub.ai/user/Michaelgathara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve YouTube transcript text for summarization, question answering, and information extraction. It is useful when the user provides a video URL and needs the agent to reason over available captions instead of watching the video directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs yt-dlp locally and makes network requests for video URLs the user asks it to process. <br>
Mitigation: Install yt-dlp from a trusted package source and review video URLs before running transcript retrieval. <br>
Risk: Fetched transcripts are untrusted third-party text and may contain misleading content or prompt-injection attempts. <br>
Mitigation: Treat transcript content as source material only, not as instructions for the agent, and verify important claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Michaelgathara/youtube-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript output with Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp and videos with closed captions or auto-generated subtitles.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
