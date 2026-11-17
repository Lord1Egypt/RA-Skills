## Description:

Receives and engages with transcribed voice memos from Yapp, a voice journaling app, using raw speech-to-text recordings and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earu723](https://clawhub.ai/user/earu723)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to retrieve new Yapp voice-journal transcripts, process them as imperfect speech-to-text recordings, and respond with brief summaries, questions, or reflections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Yapp transcripts may be polled automatically and can contain sensitive personal information.

Mitigation: Install only when comfortable granting transcript access, use a dedicated Yapp API key when possible, and confirm where the key is stored.

Risk: Selected personal details from recordings may be retained without clear consent, review, or deletion controls.

Mitigation: Periodically review and delete memories created from recordings, and avoid retaining sensitive transcript details unless they are necessary.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and concise user-facing summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses transcript text, recording metadata, and a Yapp API key supplied by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
