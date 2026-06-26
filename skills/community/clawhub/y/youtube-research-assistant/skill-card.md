## Description: <br>
Fetch transcripts from YouTube videos to provide structured multilingual summaries, Q&A, and deep dives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaheshMuke](https://clawhub.ai/user/MaheshMuke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill in OpenClaw to fetch YouTube captions, store local transcripts, and generate summaries, Q&A, deep dives, and action points from transcript text only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: yt-dlp contacts YouTube to fetch caption files for requested videos. <br>
Mitigation: Use the skill only for intentional YouTube transcript requests and expect that the requested video URL or ID is used for the caption fetch. <br>
Risk: Transcript text, YouTube URLs, and active-video history are stored locally in the skill data folder. <br>
Mitigation: Clear the skill data folder when transcript content or viewing history should not remain on the machine. <br>
Risk: Videos without captions or failed caption retrieval can leave the agent without grounded source text. <br>
Mitigation: Stop on transcript fetch errors or missing captions, and answer only from returned timestamped transcript chunks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MaheshMuke/youtube-research-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with transcript-grounded bullets, timestamps, Q&A, deep dives, and action points.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local transcript files and session state; default summaries target exactly five key points and three to five timestamps.] <br>

## Skill Version(s): <br>
5.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
