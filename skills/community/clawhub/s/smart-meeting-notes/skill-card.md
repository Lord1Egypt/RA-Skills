## Description:

Turn meeting transcripts or voice recordings into structured notes with action items, decisions, and owners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and teams use this skill to convert meeting transcripts or recordings into concise meeting notes, action items, decisions, discussion summaries, open questions, and follow-up views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes may contain confidential, HR, legal, customer, or personal information and the skill saves notes locally under ~/.openclaw/meetings/.

Mitigation: Review the skill before installing, confirm that local storage is acceptable, and require explicit user confirmation before saving or reading meeting history.

Risk: Audio transcription may require installing Whisper or sending audio to an external API.

Mitigation: Confirm transcription tooling and data-handling expectations before installing Whisper or using an external transcription API.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown notes, tables, short summaries, and occasional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save meeting notes under ~/.openclaw/meetings/ and can suggest Whisper CLI or API transcription when audio is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
