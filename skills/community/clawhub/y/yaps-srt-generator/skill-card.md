## Description:

Creates timed SRT subtitle files from audio or video with Yaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People creating accessible media use this skill to generate a separate, timed subtitle file from a selected audio or video recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime can expose Yaps commands and transcription workflows beyond subtitle creation.

Mitigation: Prefer the documented SRT-file workflow and review any broader command before approval.

Risk: Account or credential prompts may arise while preparing Yaps.

Mitigation: Do not approve Keychain prompts or reconnect accounts at this skill's request; sign in through the Yaps app when needed.

Risk: Subtitle timing checks cannot establish that the words are accurate.

Mitigation: Inspect generated cues and compare them with the source recording when accuracy matters.

## Reference(s):

- [Yaps runtime guide](references/runtime.md)
- [Yaps download](https://yaps.ai/download)
- [ClawHub skill listing](https://clawhub.ai/yaps/skills/yaps-srt-generator)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [SRT plain-text subtitle file with a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate subtitle file; reports engine, duration, and word count when available]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
