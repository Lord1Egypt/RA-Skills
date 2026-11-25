## Description:

Creates 60–120 second promotional videos for skills or products, combining a talking digital presenter, example charts, narration, subtitles, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to turn a skill or product into a narrated showcase video, with scenes and examples driven by a reusable configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible unrestricted network destinations and shell command handling; its scan coverage is partial.

Mitigation: Review shell and file access before use, and keep execution limited to a dedicated project workspace.

Risk: A configured service URL could send job details outside the local machine.

Mitigation: Use a trusted endpoint you control, preferably a local service, and avoid sending sensitive job details.

Risk: Scripts may overwrite files or clear the current Blender scene.

Mitigation: Use a dedicated output directory and save a copy of any Blender scene before running the workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/docsor1212/skills/skill-promo-video)
- [Production pipeline guide](artifact/references/pipeline.md)
- [Digital presenter engine guide](artifact/references/digital-human.md)
- [Production pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Video files, Configuration files, Shell commands, Guidance]

**Output Format:** [MP4 promotional video with narration, subtitles, charts, and scene graphics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 16:9 and 60–120 seconds. Full generation uses a local GPU, local inference and TTS services, Blender, and FFmpeg.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
