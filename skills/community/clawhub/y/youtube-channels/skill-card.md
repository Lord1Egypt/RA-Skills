## Description: <br>
Helps agents resolve YouTube channel handles or URLs, browse recent uploads, search within a channel, and monitor creator uploads through TranscriptAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when a YouTube creator or channel is the focus and they need an agent to inspect recent uploads, search a channel, resolve handles, or retrieve channel-oriented video metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill setup flow requires an agent to handle and persist a TranscriptAPI credential. <br>
Mitigation: Create the TranscriptAPI account yourself when possible, store the key through a platform secret manager instead of chat, confirm where it is persisted, and rotate or revoke the key when it is no longer needed. <br>


## Reference(s): <br>
- [TranscriptAPI homepage](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI auth setup](references/auth-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown instructions with curl examples and JSON API response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access, TRANSCRIPT_API_KEY, and a User-Agent header for TranscriptAPI requests.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
