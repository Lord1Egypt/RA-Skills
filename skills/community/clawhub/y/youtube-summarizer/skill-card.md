## Description: <br>
Automatically fetch YouTube video transcripts, generate structured summaries, and send full transcripts to messaging platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abe238](https://clawhub.ai/user/abe238) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to summarize or transcribe YouTube videos from shared URLs, with structured metadata and optional transcript delivery in Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external MCP server to fetch YouTube transcripts. <br>
Mitigation: Review and pin the mcp-server-youtube-transcript dependency before installation when supply-chain control matters. <br>
Risk: The skill may save full transcripts locally and attach transcript files to Telegram chats. <br>
Mitigation: Use it only where local transcript storage and Telegram file delivery are acceptable for the video content and chat audience. <br>
Risk: Transcript availability and quality depend on YouTube captions. <br>
Mitigation: Treat summaries as transcript-derived and verify important conclusions against the saved transcript or the source video. <br>


## Reference(s): <br>
- [YouTube Summarizer on ClawHub](https://clawhub.ai/abe238/youtube-summarizer) <br>
- [MCP YouTube Transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary with video metadata, local transcript text file, and optional Telegram file attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save full transcripts under /root/clawd/transcripts and attach the transcript file in Telegram contexts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
