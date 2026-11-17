## Description:

SenseAudio-Let-Claw-Talk v1 launches an always-listening local voice assistant on macOS or Windows that captures speech, transcribes it with SenseAudio ASR, sends the text to the AudioClaw agent, and reads responses through SenseAudio TTS or system speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run hands-free desktop voice conversations with AudioClaw, including wake and sleep phrases, spoken responses, runtime tuning, and optional WeSpeaker voiceprint filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-running microphone workflows can capture speech continuously and send speech data to SenseAudio.

Mitigation: Review carefully before installing and run the assistant only when the user intends active microphone capture.

Risk: The skill stores local secrets, conversation state, and logs.

Mitigation: Avoid putting API keys on the command line, restrict credential file permissions, and review or disable transcript logging where appropriate.

Risk: The optional WeSpeaker service is flagged as unsafe by the security evidence.

Mitigation: Keep WeSpeaker disabled until its local HTTP service has authentication and path validation, and pin its dependency installation to reviewed versions or commits.

## Reference(s):

- [Runtime Tuning](artifact/references/runtime_tuning.md)
- [WeSpeaker User Environment Guide](artifact/references/wespeaker_user_setup.md)
- [WeSpeaker Repository](https://github.com/wenet-e2e/wespeaker.git)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise spoken-response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch a long-running local microphone workflow and write user-level state, logs, and credentials outside the skill directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
