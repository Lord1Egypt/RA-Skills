## Description: <br>
Turn raw transcripts into structured summaries, meeting minutes, decisions, and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yvette1226](https://clawhub.ai/user/yvette1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to convert provided meeting, interview, lecture, podcast, or call transcripts into readable summaries, key discussion points, decisions, action items, and cleaned notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release title may suggest direct audio transcription, but the artifact operates on already-transcribed text. <br>
Mitigation: Provide transcript text as input and evaluate any separate speech-to-text service before uploading recordings. <br>
Risk: Transcripts may contain confidential, personal, health, financial, or credential data. <br>
Mitigation: Redact sensitive content unless authorized to process it, and follow the applicable data-handling policy before sharing transcripts. <br>
Risk: Summaries, decisions, and action items may misrepresent unclear or ambiguous transcript content. <br>
Mitigation: Review generated notes against the source transcript, and keep uncertain owners, deadlines, or facts marked as unspecified or uncertain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yvette1226/whisper-audio-transcription) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with headings, bullet lists, and an action-item table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces summaries from user-provided transcript text; it does not transcribe audio directly.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
