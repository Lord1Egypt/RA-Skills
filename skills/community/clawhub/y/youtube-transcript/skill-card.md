## Description: <br>
Fetch and summarize YouTube video transcripts. Use when asked to summarize, transcribe, or extract content from YouTube videos. Handles transcript fetching via residential IP proxy to bypass YouTube's cloud IP blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xthezealot](https://clawhub.ai/user/xthezealot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch YouTube transcript data for summarization, transcription, or content extraction workflows. It is intended for videos where transcript access is available and the operator accepts the network routing requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use can automatically change the host's VPN and routing settings. <br>
Mitigation: Install only when this routing behavior is intended; use a dedicated, tightly scoped WireGuard configuration and run in an isolated environment without unnecessary privileges where possible. <br>
Risk: Video IDs may be sent to YouTube-related services and noembed.com during transcript and metadata retrieval. <br>
Mitigation: Avoid sensitive or unlisted videos unless this disclosure is acceptable for the workflow. <br>


## Reference(s): <br>
- [YouTube Transcript setup guide](references/SETUP.md) <br>
- [noembed oEmbed endpoint used for video metadata](https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON from the transcript script, with text or Markdown summaries produced by the agent as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes video ID, title, author, full transcript text, and timestamped transcript entries when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
