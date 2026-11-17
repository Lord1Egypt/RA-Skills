## Description:

Song Creation coordinates lyric writing, music arrangement, and ComfyUI AceStep audio synthesis for Chinese-language song requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingshihuan](https://clawhub.ai/user/qingshihuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a song request into lyrics, an arrangement plan, synthesis parameters, and an audio-generation handoff. It is aimed at OpenClaw deployments with local ComfyUI AceStep support and suitable GPU hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs mutable third-party components, Python dependencies, and large model files.

Mitigation: Review the setup script before installation, run it in an isolated account, VM, or container, and pin and verify ComfyUI, custom nodes, dependencies, and model downloads.

Risk: Local output movement can be unsafe when song names or paths are not validated.

Mitigation: Avoid untrusted song names and add path validation before allowing automated output moves.

Risk: The local ComfyUI startup enables broad CORS behavior.

Mitigation: Remove broad CORS unless it is required and keep the service bound to localhost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingshihuan/skills/song-creation)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
- [AceStep v1.5 model files](https://huggingface.co/Looky916/AceStep-v1.5)
- [ROCm documentation](https://rocm.docs.amd.com/)
- [CUDA downloads](https://developer.nvidia.com/cuda-downloads)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with song lyrics, arrangement parameters, command guidance, and a MEDIA path when audio is generated]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an MP3 file through ComfyUI AceStep when local dependencies, workflow files, models, and GPU resources are available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
