## Description: <br>
Summarizes YouTube videos from a provided link by fetching Vietnamese or English transcripts and identifying the main points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaskies](https://clawhub.ai/user/Jaskies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract available YouTube subtitles and receive a concise, structured summary of a video. It is useful when a user wants the main ideas of a video without manually reading the full transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on locally installed yt-dlp and ffmpeg. <br>
Mitigation: Install these tools from trusted sources and keep them updated before running transcript extraction. <br>
Risk: Running the skill contacts YouTube for the user-provided video URL. <br>
Mitigation: Use only URLs the user is authorized to process and avoid sending sensitive or private video content unless permitted. <br>
Risk: Fetched subtitle text is exposed to the assistant for summarization. <br>
Mitigation: Review whether the transcript contains confidential or sensitive information before summarizing it. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/Jaskies/tomtat-video-jaskies) <br>
- [Publisher profile](https://clawhub.ai/user/Jaskies) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional shell command output from transcript extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The transcript fetch prefers Vietnamese subtitles and falls back to English when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
