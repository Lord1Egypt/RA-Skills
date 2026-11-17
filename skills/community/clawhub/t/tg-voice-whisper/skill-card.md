## Description:

Auto-transcribes Telegram voice messages in .ogg Opus format to text using a local OpenAI Whisper tiny model, replies with the transcription, and deletes processed files for privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drones277](https://clawhub.ai/user/drones277)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure an agent that locally transcribes inbound Telegram voice files and replies with text while avoiding external transcription APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an always-on watcher over private voice files.

Mitigation: Enable it only when continuous monitoring is intended, prefer one-shot or explicitly time-limited workers, and run it under a least-privileged account.

Risk: Shell and wildcard file handling can process or delete unintended files.

Mitigation: Use pinned dependencies in an isolated environment and replace wildcard shell commands with validated per-file processing before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Whisper transcription guidance and command snippets; configured workflows may remove processed local audio and temporary transcript files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
