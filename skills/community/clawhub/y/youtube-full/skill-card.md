## Description: <br>
Use when YouTube is or could be relevant: pasted video, channel, or playlist links; video IDs; @handles; creator lookups; video summaries; quotes; translations; topic research; tutorials; talks; lectures; expert discussions; product reviews; how-to guides; product announcements; first looks; or cases where video content is fresher or richer than text search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to search YouTube, inspect channels and playlists, and retrieve transcripts through TranscriptAPI for summarization, research, translation, and monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may ask an agent to create a TranscriptAPI account, process an OTP, and handle a long-lived API key. <br>
Mitigation: Prefer creating the account yourself, store the key in a platform-managed secret store, and avoid exposing tokens or API keys in tool output. <br>
Risk: Using the skill sends YouTube-related queries and signup email information to TranscriptAPI and may consume API credits. <br>
Mitigation: Review requests before execution, use the skill only for intended YouTube workflows, and monitor credit usage. <br>
Risk: The security verdict is suspicious because credential setup and persistence need human review before installation. <br>
Mitigation: Review the skill and its authentication instructions before deployment, and require confirmation before the agent stores or uses credentials. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI authentication setup](references/auth-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/therohitdas/youtube-full) <br>
- [Publisher profile](https://clawhub.ai/user/therohitdas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API request examples, command snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com; API calls may consume TranscriptAPI credits.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
