## Description: <br>
transcriptapi helps agents retrieve YouTube transcripts, search videos, channels, and playlists, browse channel uploads, and use caption-backed video content in research or summarization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill when YouTube content is relevant to a task, including transcript retrieval, video search, channel or playlist browsing, summaries, quotes, translations, tutorials, talks, reviews, and topic research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guide can put the agent in charge of account signup, OTP handling, credential capture, and persistent secret storage. <br>
Mitigation: Prefer creating the account yourself, storing TRANSCRIPT_API_KEY through the platform-approved secret manager, and avoiding credential values in prompts, logs, or shell output. <br>
Risk: Using the skill sends YouTube-related queries, identifiers, and API requests to transcriptapi.com. <br>
Mitigation: Use the skill only when that third-party data flow is acceptable for the task and avoid sending private or sensitive video research queries. <br>


## Reference(s): <br>
- [TranscriptAPI homepage](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI authentication setup](references/auth-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/therohitdas/transcriptapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require outbound HTTPS requests to transcriptapi.com and a TRANSCRIPT_API_KEY secret.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
