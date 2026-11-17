## Description:

Turns a Chinese song into an English cover with singable lyrics, synthesized vocals, a finished mix, and an optional lyric video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-shuanglin](https://clawhub.ai/user/wang-shuanglin)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers can use this skill to turn a Chinese song into an English-language cover, including singable lyrics, generated vocals, a mixed audio track, and an optional lyric video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags reported unsafe checkpoint loading.

Mitigation: Consider the suspicious verdict before installing and verify the source of model checkpoints before use.

Risk: The security review reports a possible write outside the output directory.

Mitigation: Review file access and run the skill with write permissions limited to its designated working and output directories.

Risk: The scan was partial: demo binaries were outside analyzer coverage, some local paths were unresolved, and external model files could not be established as safe.

Mitigation: Review the unscanned binaries, unresolved paths, and external model files before use; the partial review does not establish that these parts are safe.

## Reference(s):

- [Lyrics guide](references/lyrics-guide.md)
- [Model contracts](references/model-contracts.md)
- [Pipeline guide (v2)](references/pipeline-v2.md)
- [SoulX-Singer](https://github.com/Soul-AILab/SoulX-Singer)
- [RMVPE](https://github.com/yxlllc/RMVPE)
- [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

## Skill Output:

**Output Type(s):** [Audio, Video, Text, JSON, Shell commands]

**Output Format:** [Mixed audio files, English lyric text and JSON, and optional MP4 lyric video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Python 3.12 environment, ffmpeg, an NVIDIA GPU with at least 6 GB VRAM, and separately downloaded model weights; ComfyUI is needed for artwork and video generation.]

## Skill Version(s):

2.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
