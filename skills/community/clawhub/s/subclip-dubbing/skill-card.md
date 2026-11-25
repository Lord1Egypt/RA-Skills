## Description:

Translate and dub an existing Subclip timeline audio/video item under assistant control using exact captions, speaker-aware temporary voices, bounded TTS retries, duration-fit review, atomic timeline placement, and translated visual-caption replacement when captions were already shown. Use for translated voice replacement or multilingual dubbing; do not route this workflow through the separate Dub Studio/Dubbing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and editors use this skill to translate and dub one exact audio or video item in a Subclip timeline. It supports speaker-aware voice selection and translated captions when visible captions already exist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Three local path-like references could not be resolved, leaving their purpose uncertain.

Mitigation: Review the unresolved references in the source package and decide whether they matter before installing or relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/prosamik/skills/subclip-dubbing)
- [Publisher profile](https://clawhub.ai/user/prosamik)

## Skill Output:

**Output Type(s):** [Audio, Translated text, Captions, Timeline edits]

**Output Format:** [Dubbed audio and translated captions in the Subclip timeline]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice cloning requires explicit authorization; speech generation uses bounded retries, attempt limits, and credit limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
