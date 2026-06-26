## Description: <br>
Use when subtitles or the spoken text of a YouTube video is needed: pasted video links or IDs, requests to translate a video, read along, follow foreign-language content, or extract what was said. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch YouTube subtitles or spoken transcript text for reading, translation, language learning, accessibility, or extracting what was said in a video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can let an agent create a TranscriptAPI account and persist a long-lived API key. <br>
Mitigation: Confirm where the key will be stored before setup, prefer a platform secret store, and keep the revocation or deletion path available. <br>
Risk: YouTube links submitted for transcription may disclose private or sensitive viewing material to TranscriptAPI. <br>
Mitigation: Use the skill only with videos appropriate to share with the external provider, and avoid private or sensitive links unless you trust that provider. <br>


## Reference(s): <br>
- [TranscriptAPI](https://transcriptapi.com) <br>
- [TranscriptAPI Auth Setup](references/auth-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash examples and TranscriptAPI text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to transcriptapi.com and a TRANSCRIPT_API_KEY credential.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
