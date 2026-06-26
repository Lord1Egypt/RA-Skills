## Description: <br>
Use when structured YouTube data is needed: pasted video/channel/playlist links, transcripts for analysis, video metadata, channel upload history, search results, or playlist contents, without Google API quotas or OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to retrieve structured YouTube transcripts, metadata, search results, channel uploads, and playlist contents through TranscriptAPI. It is intended for YouTube data lookup and analysis, not uploads, account management, or written-source-only research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can let the agent create a TranscriptAPI account, handle OTPs and tokens, and persist an API key. <br>
Mitigation: Prefer creating the account yourself, provide the key through a secure secret store, and confirm exactly where the key is saved. <br>
Risk: The TRANSCRIPT_API_KEY is a sensitive credential that could be exposed through prompts, logs, temporary files, or persistent environment configuration. <br>
Mitigation: Keep the key out of chat transcripts and command output, clean up temporary files after setup, and rotate the key if exposure is suspected. <br>
Risk: YouTube URLs, creator names, and search terms sent to TranscriptAPI may reveal sensitive or private research interests. <br>
Mitigation: Avoid using the skill with sensitive or private YouTube URLs, search terms, or channel investigations unless the user accepts that disclosure. <br>
Risk: TranscriptAPI requests depend on an external service and require the correct User-Agent and Authorization headers. <br>
Mitigation: Verify request headers before use, handle 401, 402, 403, 408, and 422 responses explicitly, and do not treat failed or partial responses as complete data. <br>


## Reference(s): <br>
- [TranscriptAPI homepage](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI auth setup](references/auth-setup.md) <br>
- [ClawHub release page](https://clawhub.ai/therohitdas/youtube-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with curl commands, configuration guidance, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to transcriptapi.com and a TRANSCRIPT_API_KEY for API requests; setup may persist the key for future agent sessions.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
