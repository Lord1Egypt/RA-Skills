## Description:

Helps users set up and troubleshoot Yaps desktop voice typing and recover a requested recent dictation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

Desktop users and support agents use this skill to set up voice typing, diagnose capture or insertion problems, and recover a specifically requested dictation through a local Yaps installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Yaps command interface supports meeting transcription and project creation beyond dictation.

Mitigation: Limit use to the user's explicit dictation, recovery, or selected-file request; do not run exploratory commands.

Risk: Recovered history, transcripts, and captions may expose sensitive content to the agent host and remain in Yaps.

Mitigation: Access only requested items, show minimal identifying context, and confirm before saving recovered text.

## Reference(s):

- [Yaps Dictation on ClawHub](https://clawhub.ai/yaps/skills/yaps-dictation)
- [Yaps download](https://yaps.ai/download)
- [Yaps local runtime guide](references/runtime.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include limited excerpts from a specifically requested recovered dictation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
