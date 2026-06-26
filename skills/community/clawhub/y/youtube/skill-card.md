## Description: <br>
Search YouTube videos, get channel info, fetch video details and transcripts using YouTube Data API v3 via MCP server or yt-dlp fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grpaiva](https://clawhub.ai/user/grpaiva) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent search YouTube, inspect videos and channels, and retrieve transcripts for research, summarization, and content analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party MCP server package or repository. <br>
Mitigation: Install only if you trust zubeid-youtube-mcp-server, and prefer pinned or reviewed versions. <br>
Risk: A YouTube API key can be exposed or over-permissioned. <br>
Mitigation: Restrict the key to YouTube Data API v3, keep it out of source control and shared files, and provide it through local configuration or the environment. <br>
Risk: YouTube search and video detail calls can consume API quota. <br>
Mitigation: Use search calls deliberately, set small result limits when possible, and prefer transcript lookups when they meet the task. <br>
Risk: Transcripts may be unavailable, incomplete, or auto-generated. <br>
Mitigation: Check transcript availability and verify important quotes against the source video before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grpaiva/youtube) <br>
- [YouTube MCP server](https://github.com/ZubeidHendricks/youtube-mcp-server) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets; YouTube and transcript results may be plain text or structured command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOUTUBE_API_KEY, the zubeid-youtube-mcp-server package, and yt-dlp for fallback transcript extraction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
