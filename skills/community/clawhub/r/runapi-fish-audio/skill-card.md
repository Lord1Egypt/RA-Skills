## Description:

Creates account-owned Fish Audio voice resources and generates MP3/WAV speech through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other RunAPI users can create or look up voice resources, generate speech, and integrate Fish Audio into applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting requests may upload local audio and incur charges on the user's RunAPI account.

Mitigation: Review local audio paths and request JSON before submission; use only an account the user intends to use.

## Reference(s):

- [Fish Audio model documentation](https://runapi.ai/models/fish-audio.md)
- [Fish Audio provider overview](https://runapi.ai/providers/fish-audio.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Fish Audio model page](https://runapi.ai/models/fish-audio)
- [Fish Audio SDK integration reference](https://github.com/runapi-ai/fish-audio-sdk)

## Skill Output:

**Output Type(s):** [Audio files, Text, Code, Shell commands, Configuration instructions]

**Output Format:** [MP3/WAV audio, JSON or text results, and Markdown guidance or code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice resource identifiers may cease to work; verify downloaded audio files before delivery.]

## Skill Version(s):

0.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
