## Description: <br>
Provides a ComfyUI image-generation helper that updates workflow prompt text, avoids duplicate generation, validates required workflow nodes, and returns structured generation results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[admirobot](https://clawhub.ai/user/admirobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to call a configured ComfyUI server for image generation from prompts while reusing validated workflow files and explicit output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text and workflow requests are sent to the configured ComfyUI server. <br>
Mitigation: Set COMFYUI_SERVER only to a trusted server and avoid sensitive prompts on shared or untrusted networks. <br>
Risk: Generated files are written or copied to caller-provided output paths. <br>
Mitigation: Choose explicit output directories where overwriting or creating image files would not affect important data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/admirobot/tvdr-comfyui-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Configuration instructions, Code] <br>
**Output Format:** [Python functions returning dictionaries and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted COMFYUI_SERVER and workflow JSON with CLIPTextEncode and SaveImage nodes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
