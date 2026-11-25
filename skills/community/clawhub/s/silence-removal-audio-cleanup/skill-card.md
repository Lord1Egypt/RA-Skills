## Description:

Remove silences, dead air, pauses, and filler words (um, uh) on word boundaries, clean audio noise, generate AI voiceovers and TTS, add background music and sound effects (SFX), and auto-duck music under speech (-18 LUFS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editors use the skill to tighten spoken-word audio or video, remove pauses and filler words, balance dialogue, and add music or sound effects through the Levea editing service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and media are sent to the Levea editing service, which creates a privacy consideration for sensitive recordings.

Mitigation: Review whether you are comfortable sending the prompts and media to Levea, and avoid making sensitive recordings publicly accessible.

Risk: One scanner's analysis was partial because a local reference was missing, so the security evidence is incomplete.

Mitigation: Review the skill and its dependencies before installation and use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/brajendrak00068/skills/silence-removal-audio-cleanup)
- [Levea editing service](https://livecore.ai/)
- [Levea API endpoint](https://api.livecore.ai)

## Skill Output:

**Output Type(s):** [API Calls, Media edits, Text]

**Output Format:** [Editing project status and identifiers, with an exported MP4 URL when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media exports may be asynchronous; the skill can return a waiting status or job identifier.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
