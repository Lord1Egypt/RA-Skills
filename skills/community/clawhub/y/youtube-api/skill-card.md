## Description: <br>
Use when YouTube data is needed without Google API quotas or OAuth setup: transcripts, video metadata, channel info, search results, playlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve YouTube transcripts, video metadata, channel information, search results, and playlist data through TranscriptAPI. It is intended for YouTube research and summarization workflows, not uploads, account management, or written-source-only research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an agent to handle and persist a TranscriptAPI credential. <br>
Mitigation: Use a dedicated TranscriptAPI key stored through the agent or platform secret manager, confirm where it is persisted, and rotate or revoke it when no longer needed. <br>
Risk: YouTube queries, URLs, channel handles, and account setup data may be sent to TranscriptAPI. <br>
Mitigation: Use the skill only when sharing that data with TranscriptAPI is acceptable, and avoid sending sensitive or private research inputs. <br>
Risk: The account setup workflow includes handling short-lived tokens and API keys that may be redacted or exposed if printed. <br>
Mitigation: Follow the bundled setup guide's file-based handling pattern and avoid displaying access tokens or API keys in standalone output. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI OpenAPI Specification](https://transcriptapi.com/openapi.json) <br>
- [TranscriptAPI Auth Setup](references/auth-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/therohitdas/youtube-api) <br>
- [Publisher Profile](https://clawhub.ai/user/therohitdas) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Text, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
