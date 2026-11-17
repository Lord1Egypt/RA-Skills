## Description:

Transcribe Telegram voice notes to text before the assistant replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aditya0320](https://clawhub.ai/user/aditya0320)

### License/Terms of Use:

MIT-0

## Use Case:

External Telegram assistant users and operators use this skill to turn Telegram voice notes into text before an agent responds. It helps the assistant answer the transcribed request directly, including Hindi and English mixed speech when transcription is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram voice audio or transcripts may be processed through the configured Google Cloud Speech-to-Text flow.

Mitigation: Deploy only where users and operators accept that processing path, and manage the required Google Cloud credentials according to the deployment's data handling policy.

Risk: Broad trigger wording could activate the skill outside actual Telegram voice-note or transcript contexts.

Mitigation: Narrow activation wording to inbound Telegram voice-note or available-transcript scenarios before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aditya0320/skills/telegram-voice-stt)
- [Publisher profile](https://clawhub.ai/user/aditya0320)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to treat a transcript as the user's message and depends on configured Google Cloud Speech-to-Text credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
