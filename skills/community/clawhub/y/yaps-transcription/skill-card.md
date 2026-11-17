## Description:

Turn audio or video files into plain-text transcripts using the local Yaps desktop engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People transcribing interviews, podcasts, or voice memos can use this skill to turn local audio or video into a text transcript with Yaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate more of the local Yaps desktop app than transcription alone.

Mitigation: Review requested Yaps actions and grant only the access needed for transcription.

Risk: Account refreshes or unexpected credential prompts may occur when checking Yaps access.

Mitigation: Do not approve unexpected Keychain prompts; verify account state directly in Yaps.

Risk: Transcription and related workflows can create local files or meeting projects.

Mitigation: Confirm output destinations and review created files or projects before sharing them.

## Reference(s):

- [Yaps runtime guide](references/runtime.md)
- [Yaps download](https://yaps.ai/download)
- [Yaps Transcription on ClawHub](https://clawhub.ai/yaps/skills/yaps-transcription)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text (.txt)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports output path, engine, duration, and word count; rejects blank transcripts and does not replace existing files.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
