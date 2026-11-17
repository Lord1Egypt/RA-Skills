## Description:

PureVocals-UVR-Automator helps an agent run local UVR/audio-separator workflows to extract vocal-only WAV stems from single audio files or folders while preserving folder structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and audio engineers use this skill to remove accompaniment or background music from audio and batch-produce clean vocal tracks for covers, karaoke, music production, and audio cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First run can download packages, FFmpeg, and model files and can change Python packaging tools in a persistent shared virtual environment.

Mitigation: Install and run in an isolated environment where network package installation and dependency changes are acceptable.

Risk: Executable dependencies and model assets are downloaded without tight pinning or verification.

Mitigation: Review dependency sources, restrict network access as appropriate, and pre-stage trusted packages, FFmpeg, and model files when operating in controlled environments.

Risk: The skill processes local audio files and writes generated audio, cached models, and logs to disk.

Mitigation: Use non-sensitive test files first, choose an explicit output directory, and review generated files, model cache, and logs after execution.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wangminrui2022/skills/purevocals-uvr-automator)
- [TRvlvr public UVR model releases](https://github.com/TRvlvr/model_repo/releases/tag/all_public_uvr_models)
- [Kim_Vocal_2 model file](https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/Kim_Vocal_2.onnx)
- [UVR_MDXNET_KARA_2 model file](https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR_MDXNET_KARA_2.onnx)
- [6_HP-Karaoke-UVR model file](https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/6_HP-Karaoke-UVR.pth)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples; generated audio output is WAV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates vocal-only WAV files in the requested output directory, can preserve directory structure for batches, and writes rolling local logs.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
