## Description:

Skywork Music Maker helps agents turn multilingual music descriptions into structured Mureka API prompts and generate songs, instrumentals, lyrics, and uploaded-reference music workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxcun17](https://clawhub.ai/user/gxcun17)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through music prompt shaping, lyrics creation, Mureka API calls, reference uploads, vocal cloning workflows, and local audio-file output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vocal cloning and reference-track workflows can upload voice samples or copyrighted audio without clear consent safeguards.

Mitigation: Use only voice samples and reference audio that the user owns or has documented permission to use, and review vocal-cloning requests before running upload commands.

Risk: Prompts, lyrics, and uploaded audio are transmitted to the Mureka API for generation.

Mitigation: Tell users what data will be sent before generation or upload, and avoid sending confidential or sensitive content.

Risk: The documented billing curl pattern can expose MUREKA_API_KEY locally on shared or monitored machines.

Mitigation: Prefer commands or clients that read MUREKA_API_KEY from the process environment without placing the token directly in shell history or process listings.

Risk: Unpinned dependency installation can reduce reproducibility.

Mitigation: Pin the requests dependency in controlled deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gxcun17/skills/skywork-music-maker)
- [OpenClaw Homepage](https://clawhub.ai/gxcun17/skywork-music-maker)
- [Music Prompt Crafting Guide](references/prompt_guide.md)
- [Mureka API Endpoint](https://api.mureka.ai)
- [Mureka Platform](https://platform.mureka.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and local audio or lyrics files produced by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MUREKA_API_KEY and sends prompts, lyrics, and uploaded audio to the Mureka API when generation or upload commands are run.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
