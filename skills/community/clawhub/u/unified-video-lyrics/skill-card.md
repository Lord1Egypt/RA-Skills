## Description:

A Chinese-language short-video creation skill for drafting scripts and lyrics, preserving character and visual style across generated video scenes, and planning music, platform formatting, and FFmpeg-based assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jean5773](https://clawhub.ai/user/jean5773)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to produce short-video concepts, six-shot scripts, structured lyrics, style-consistent video prompts, music direction, and assembly commands for social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to upload or analyze reference videos or call external music and video services.

Mitigation: Require explicit user confirmation before uploading media or using external services, and avoid private, sensitive, or unlicensed content unless the user confirms they have the rights to use it.

Risk: The skill includes FFmpeg command examples for merging videos and adding audio.

Mitigation: Review generated shell commands, inputs, outputs, and working directory before execution.

Risk: Broad trigger phrases can overlap with other creative-writing or video-generation skills.

Mitigation: Confirm the intended workflow when multiple installed skills match script, lyrics, short-video, or anime-style creation requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jean5773/skills/unified-video-lyrics)
- [Character templates](artifact/references/characters.md)
- [Lyrics writing techniques](artifact/references/lyrics.md)
- [Music guide](artifact/references/music.md)
- [Platform script guide](artifact/references/platforms.md)
- [Character consistency guide](artifact/references/character-consistency.md)
- [Anime style guide](artifact/references/anime-style.md)
- [Video prompt guide](artifact/references/prompt-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured scripts, lyrics, prompts, checklists, and inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language creative guidance with optional video-analysis, external media-service, and FFmpeg execution steps that should require user confirmation.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
