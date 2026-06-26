## Description: <br>
Use when YouTube is relevant: pasted video links or IDs, @handles, quick video lookups, summaries, channel latest uploads, topic search, or any request involving YouTube content, even if YouTube is not mentioned explicitly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up YouTube videos, retrieve transcripts, search topics, resolve channels, and inspect a channel's latest uploads through TranscriptAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TranscriptAPI receives YouTube queries, video URLs, channel identifiers, and related lookup requests made through this skill. <br>
Mitigation: Use the skill only for lookups you are comfortable sending to TranscriptAPI, and avoid submitting sensitive or private search terms. <br>
Risk: The setup guide can involve sensitive account signup, OTP handling, token extraction, and persistent API key storage by the agent. <br>
Mitigation: Prefer creating the account yourself, using a dedicated TranscriptAPI key, and storing it in a platform-managed secret store rather than exposing OTPs or raw credentials to the agent. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI auth setup](references/auth-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/therohitdas/yt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
