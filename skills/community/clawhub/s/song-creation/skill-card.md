## Description: <br>
Song Creation coordinates lyrics, arrangement planning, and ComfyUI AceStep audio synthesis through a multi-agent OpenClaw workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingshihuan](https://clawhub.ai/user/qingshihuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn a song request into lyrics, a music design plan, ComfyUI AceStep synthesis parameters, and an MP3 output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can install and run a local ComfyUI/AceStep AI stack with large model downloads and Python package installation. <br>
Mitigation: Review setup.sh before running it, use a dedicated environment when possible, and confirm the host has the intended GPU, disk, and network capacity. <br>
Risk: The skill writes persistent files under ~/ai and ~/.openclaw/workspace/output. <br>
Mitigation: Run it under an account and workspace where those paths are expected, and review generated files before reuse or sharing. <br>
Risk: Weak file-path safeguards can be affected by song names containing slashes or '..'. <br>
Mitigation: Use sanitized song names without path separators or traversal segments before submitting generation jobs. <br>
Risk: Prompts and lyrics may be sent to external models or local model tooling during the workflow. <br>
Mitigation: Avoid sensitive or restricted content in prompts and inspect the local operation manual before allowing the agent to follow it. <br>


## Reference(s): <br>
- [Song Creation on ClawHub](https://clawhub.ai/qingshihuan/song-creation) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) <br>
- [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager) <br>
- [AceStep v1.5 models](https://huggingface.co/Looky916/AceStep-v1.5) <br>
- [ROCm documentation](https://rocm.docs.amd.com/) <br>
- [CUDA downloads](https://developer.nvidia.com/cuda-downloads) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Media file paths] <br>
**Output Format:** [Markdown with lyrics, arrangement parameters, shell commands, Python API output, and a MEDIA path for generated audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create MP3 files under ~/.openclaw/workspace/output/YYYYMMDD/audio/ after local ComfyUI generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
