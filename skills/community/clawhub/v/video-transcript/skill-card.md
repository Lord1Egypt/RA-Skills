## Description: <br>
Extracts YouTube video transcripts through TranscriptAPI.com so agents can transcribe, summarize, quote, translate, or inspect video content from links or video IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a YouTube URL or video ID and needs the video converted into transcript text, timestamps, metadata, summaries, quotes, or translations. It is not intended for video uploads or TranscriptAPI account management beyond key setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TranscriptAPI receives the video URLs or IDs submitted through this skill. <br>
Mitigation: Use the skill only when sharing those URLs or IDs with TranscriptAPI is acceptable. <br>
Risk: The setup flow handles and persistently stores TranscriptAPI credentials. <br>
Mitigation: Use a dedicated key stored through a secure secret mechanism, avoid sharing OTPs in chat when possible, and keep a rotation or removal path available. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI auth setup](references/auth-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples and transcript text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
