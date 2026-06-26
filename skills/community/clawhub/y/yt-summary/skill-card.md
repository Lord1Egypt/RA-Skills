## Description: <br>
Summarize YouTube videos from links using TranscriptAPI transcripts, with optional custom instructions for the summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chapati23](https://clawhub.ai/user/chapati23) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn YouTube URLs into concise summaries, key points, and selected quotes. It is useful for quickly reviewing video content when transcript retrieval through TranscriptAPI is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript retrieval sends YouTube video identifiers and transcript requests to TranscriptAPI. <br>
Mitigation: Use the skill only when that third-party transcript service is acceptable for the videos being summarized. <br>
Risk: The TranscriptAPI credential is required for normal operation. <br>
Mitigation: Use a dedicated API key and prefer secure secret storage or a narrowly scoped environment variable. <br>
Risk: Transcript text and custom summary instructions are untrusted input that could contain misleading or instruction-like content. <br>
Mitigation: Treat extracted transcripts and user-provided summary instructions as source material for summarization, not as agent operating instructions. <br>
Risk: The skill depends on Python packages and metadata retrieval tools that can change over time. <br>
Mitigation: Keep requests and yt-dlp updated or pinned according to the deployment's dependency management policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chapati23/yt-summary) <br>
- [Publisher Profile](https://clawhub.ai/user/chapati23) <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [OpenClaw](https://openclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summary with progress and error text from transcript extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is intended to stay under Telegram character limits; very long transcripts are summarized from a truncated portion.] <br>

## Skill Version(s): <br>
1.3.2 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
