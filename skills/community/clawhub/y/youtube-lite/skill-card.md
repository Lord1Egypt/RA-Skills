## Description: <br>
Youtube Lite helps agents use TranscriptAPI.com to retrieve YouTube transcripts, search videos and channels, browse channel and playlist content, and inspect metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liliangjie91](https://clawhub.ai/user/liliangjie91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to gather YouTube transcripts, search YouTube content, browse channels and playlists, and support research or channel-monitoring workflows through TranscriptAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a TranscriptAPI API key for requests. <br>
Mitigation: Use a dedicated API key where possible and avoid exposing it in shared terminals, logs, or transcripts. <br>
Risk: Several endpoints consume TranscriptAPI credits, including transcript, search, channel videos, channel search, and playlist video calls. <br>
Mitigation: Confirm paid or paginated requests before use and prefer free endpoints such as channel resolve or latest videos when they satisfy the task. <br>
Risk: Search terms, video identifiers, channel identifiers, and playlist identifiers are sent to TranscriptAPI. <br>
Mitigation: Avoid sending private or sensitive search terms unless the user is comfortable sharing them with TranscriptAPI. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liliangjie91/youtube-lite) <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI Specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI Signup](https://transcriptapi.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY; some TranscriptAPI endpoints consume credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
