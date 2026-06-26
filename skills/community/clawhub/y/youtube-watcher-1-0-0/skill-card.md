## Description: <br>
Fetch and read transcripts from YouTube videos. Use when you need to summarize a video, answer questions about its content, or extract information from it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xvolica](https://clawhub.ai/user/xvolica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve YouTube captions so an agent can summarize videos, answer content questions, or extract information from transcript text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts YouTube or other yt-dlp-supported endpoints when given a supported URL. <br>
Mitigation: Use it only for explicit YouTube URLs or clear YouTube transcript requests, and review URLs before execution. <br>
Risk: Trigger phrases are broader than the YouTube-only workflow and may be invoked for non-YouTube video requests. <br>
Mitigation: Confirm that the requested input is a YouTube transcript task before running the transcript script. <br>
Risk: Transcript retrieval fails when yt-dlp is unavailable or the video has no captions or auto-generated subtitles. <br>
Mitigation: Install yt-dlp before use and surface subtitle availability errors to the user without fabricating transcript content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xvolica/youtube-watcher-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/xvolica) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp in PATH; transcript retrieval depends on available English captions or auto-generated subtitles.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, release metadata, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
