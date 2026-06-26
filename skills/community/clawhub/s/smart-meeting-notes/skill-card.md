## Description: <br>
Turn meeting transcripts or voice recordings into structured notes with action items, decisions, and owners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to convert meeting transcripts or recordings into concise notes, decisions, action-item tables, standup updates, and follow-up summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes may contain confidential or regulated information and are saved locally under ~/.openclaw/meetings/. <br>
Mitigation: Use the skill only where local retention is acceptable, review saved files after use, and delete or restrict access to notes that contain sensitive content. <br>
Risk: Audio recordings may be transcribed through local Whisper or an external API. <br>
Mitigation: Confirm the transcription path before processing recordings and avoid external transcription for confidential meetings unless the provider and retention controls are approved. <br>


## Reference(s): <br>
- [Smart Meeting Notes on ClawHub](https://clawhub.ai/vanthienha199/smart-meeting-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown notes with tables, summaries, quotes, and optional shell commands for audio transcription] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save meeting notes to ~/.openclaw/meetings/ and may guide use of local Whisper or the OpenAI Whisper API for audio transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
