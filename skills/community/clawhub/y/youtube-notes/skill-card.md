## Description: <br>
Convert YouTube videos into structured markdown notes with tools, steps, timestamps, and parts lists using TranscriptAPI.com transcript data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welbinator](https://clawhub.ai/user/welbinator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they have a YouTube link and need concise reference notes, tutorial steps, key points, timestamps, tools, materials, or parts lists without rewatching the video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube video identifiers or URLs to TranscriptAPI.com and fetches the YouTube page from the agent environment. <br>
Mitigation: Use it only when that disclosure is acceptable, especially for private-context or unlisted videos. <br>
Risk: Generated notes may be saved to another destination after they are shown to the user. <br>
Mitigation: Confirm the destination before allowing another tool or skill to store the notes. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI YouTube transcript endpoint](https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_ID&format=json&include_timestamp=true&send_metadata=true) <br>
- [ClawHub skill page](https://clawhub.ai/welbinator/youtube-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown with timestamped YouTube links and optional save guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY; may call TranscriptAPI.com and fetch the YouTube page; saving notes is optional and should follow user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
