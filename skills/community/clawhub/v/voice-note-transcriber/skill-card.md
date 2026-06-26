## Description: <br>
Fetches voice-note emails via IMAP, transcribes audio attachments with OpenAI Whisper, and saves transcripts to an Obsidian vault's fleeting notes folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users who keep voice notes in email can use this skill to pull matching unread messages, transcribe attached audio, and create Markdown transcript notes in an Obsidian fleeting-notes folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox credentials and sends matching audio attachments to OpenAI for transcription. <br>
Mitigation: Use an app-specific email password, a dedicated mailbox or narrow subject keyword, and install only when those data flows are acceptable. <br>
Risk: Generated Obsidian transcripts may contain transcription errors or sensitive content from source audio. <br>
Mitigation: Review generated notes before relying on or sharing them, and treat transcripts as unreviewed content. <br>
Risk: Processed emails are marked as read by default. <br>
Mitigation: Set MARK_EMAIL_READ=false for the first run or until the mailbox filtering behavior is confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/voice-note-transcriber) <br>
- [OpenAI audio transcriptions endpoint](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown transcript files with YAML frontmatter, plus console status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EMAIL_ADDRESS, EMAIL_PASSWORD, OPENAI_API_KEY, and OBSIDIAN_VAULT_PATH; filters unread email by subject keyword and supported audio attachment extensions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
