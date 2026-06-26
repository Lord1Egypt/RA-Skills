## Description: <br>
Helps agents browse YouTube playlists and fetch related transcripts through TranscriptAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list videos in a YouTube playlist, page through playlist contents, and retrieve transcripts for research or content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube playlist and transcript requests to TranscriptAPI. <br>
Mitigation: Install only if you are comfortable using TranscriptAPI for those requests and avoid sending content you do not want handled by that service. <br>
Risk: The skill requires a TRANSCRIPT_API_KEY and includes guidance for persistent API-key storage. <br>
Mitigation: Store the key through a secure secret mechanism, avoid shell-profile or long-term storage unless necessary, and keep revocation and cleanup steps available. <br>
Risk: The auth setup can ask an agent to create a TranscriptAPI account and handle email verification. <br>
Mitigation: Prefer creating the account yourself or supervise the signup flow closely, including the email and OTP exchange. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI auth setup](references/auth-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/therohitdas/youtube-playlist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
