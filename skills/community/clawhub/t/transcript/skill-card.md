## Description: <br>
Fetches spoken content from YouTube videos through TranscriptAPI for transcription, summarization, quoting, translation, fact-checking, and research tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill when a YouTube video is the source material and they need transcript text, timestamps, or metadata for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can give an agent access to account signup, OTP handling, API-key storage, and future TranscriptAPI requests. <br>
Mitigation: Create and store the TranscriptAPI key yourself through an approved secret manager when possible, and rotate or remove the key when the skill is no longer needed. <br>
Risk: Using the skill sends YouTube video identifiers and related request data to TranscriptAPI. <br>
Mitigation: Use the skill only for videos and request data that are acceptable to send to TranscriptAPI. <br>


## Reference(s): <br>
- [Authentication setup](references/auth-setup.md) <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [ClawHub skill page](https://clawhub.ai/therohitdas/transcript) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
