## Description: <br>
Audio2Text transcribes local audio files with Tinrec's cloud API and returns summaries, key points, to-dos, transcripts, and speaker information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinrec-com](https://clawhub.ai/user/tinrec-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they have a local audio file and want Tinrec to produce a transcript, summary, meeting notes, key points, to-dos, and speaker labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local audio files are uploaded to Tinrec for cloud transcription and analysis. <br>
Mitigation: Use the skill only for recordings that are appropriate to send to Tinrec, and confirm Tinrec's privacy terms before processing confidential audio. <br>
Risk: The Tinrec API key can be provided directly, through an environment variable, or from a local api-keys file. <br>
Mitigation: Use a dedicated or rotatable API key, prefer environment variables or a protected key file, and delete local key files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Audio2Text skill page](https://clawhub.ai/tinrec-com/tinrec-audio2text) <br>
- [Tinrec API keys](https://tinrec.com/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable text or JSON from the Tinrec CLI, with setup guidance that may include shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local audio file and a Tinrec API key; selected audio is uploaded to Tinrec for cloud processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
