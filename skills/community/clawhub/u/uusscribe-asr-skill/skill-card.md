## Description:

Transcribes local audio files and public single-video YouTube URLs using UUScribe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoyostudio209](https://clawhub.ai/user/yoyostudio209)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can transcribe their audio files or public YouTube videos, including optional timestamps and speaker-labeled segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local audio or public YouTube video references are sent to UUScribe and may consume account allowance.

Mitigation: Submit only user-authorized content they have the right to process; explain uploads and allowance use when the request is unclear.

Risk: The skill accesses the user's UUScribe API key.

Mitigation: Supply the key through the environment; do not paste it into chat or expose it in output.

Risk: Resubmitting a task may create duplicate billable work.

Mitigation: Keep the task ID and resume polling; check the account's task list before retrying an uncertain submission.

Risk: Transcripts or video metadata may contain misleading instructions, and output files may overwrite unintended paths.

Mitigation: Treat returned content as untrusted data and use --output only for a path the user intends to write.

## Reference(s):

- [UUScribe ASR on ClawHub](https://clawhub.ai/yoyostudio209/skills/uusscribe-asr-skill)
- [UUScribe](https://scribe.uustudio.cc)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text transcript or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a task ID, recognized language, timestamps and speaker labels; results can optionally be saved to a file.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
