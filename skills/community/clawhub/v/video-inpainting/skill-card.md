## Description: <br>
Provides agent guidance and RunComfy CLI commands for region edits across video frames, including object removal, watermark cleanup, and region replacement using RunComfy video-editing models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-editing agents use this skill to choose an appropriate RunComfy video inpainting route and produce CLI or GUI workflow guidance for editing a target region across frames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video inputs and prompts are submitted to RunComfy cloud processing through a third-party CLI. <br>
Mitigation: Use only the official RunComfy CLI, keep RUNCOMFY_TOKEN private, and submit only videos the user is comfortable sending to RunComfy. <br>
Risk: Vague edit requests can target the wrong region or produce unintended visual changes. <br>
Mitigation: Confirm the source video URL, exact region, and desired edit before running the workflow. <br>
Risk: Prompt-driven region edits may not provide pixel-precise mask propagation or temporal consistency for all clips. <br>
Mitigation: Use the referenced RunComfy ComfyUI workflows for mask-driven or higher-precision video inpainting needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/video-inpainting) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting) <br>
- [Wan 2-7 Edit-Video model](https://www.runcomfy.com/models/wan-ai/wan-2-7/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting) <br>
- [Seedream 4-0 Edit-Sequential model](https://www.runcomfy.com/models/bytedance/seedream-4-0/edit-sequential?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting) <br>
- [LTX 2-3 video inpaint ComfyUI workflow](https://www.runcomfy.com/comfyui-workflows/ltx-2-3-inpaint-in-comfyui-targeted-video-frame-editing?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting) <br>
- [RunComfy video model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting) <br>
- [RunComfy Wan models collection](https://www.runcomfy.com/models/collections/wan-models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-inpainting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces RunComfy CLI examples and routing guidance; requires runcomfy, RUNCOMFY_TOKEN, and ~/.config/runcomfy.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
