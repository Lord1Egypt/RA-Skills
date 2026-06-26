## Description: <br>
Extract and analyze YouTube video transcripts without watching the video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XanderRey](https://clawhub.ai/user/XanderRey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, researchers, and developers use this skill to extract YouTube transcripts and turn them into concise summaries, key takeaways, notable quotes, and action items without watching the video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled shell script may download yt-dlp from GitHub into the user's home directory if yt-dlp is not already installed. <br>
Mitigation: Review the script before use and prefer installing a trusted, pinned yt-dlp version yourself before running transcript extraction. <br>
Risk: Transcript extraction contacts YouTube and may fail for unavailable, private, restricted, or captionless videos. <br>
Mitigation: Use the skill's fallback guidance to explain transcript limitations and rely only on available video metadata when transcripts cannot be extracted. <br>


## Reference(s): <br>
- [Analysis Patterns](references/analysis-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/XanderRey/youtube-transcript-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and transcript text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a cleaned transcript file through the bundled shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
