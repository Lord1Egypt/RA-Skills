## Description: <br>
Use when the user wants to find YouTube content on any topic: searching for videos or channels, finding creators who cover a subject, discovering tutorials, talks, or expert discussions, or looking up a channel by name or handle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search YouTube for videos, channels, creators, tutorials, talks, and expert discussions, then fetch transcripts through TranscriptAPI when useful for research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TranscriptAPI receives YouTube searches and transcript requests made through this skill. <br>
Mitigation: Install only when that data sharing is acceptable for the intended use case. <br>
Risk: The skill requires an agent to store TRANSCRIPT_API_KEY for later sessions. <br>
Mitigation: Use a platform secret store where available, monitor API credit usage, and revoke or rotate the key when it is no longer needed. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI authentication setup](references/auth-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/therohitdas/youtube-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com for API requests.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
